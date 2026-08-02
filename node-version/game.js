const path = require('path');
const { ask, bar, createInterface, loadJson, roll, saveJson } = require('./utils');

const DATA_DIR = path.join(__dirname, 'data');
const SAVE_FILE = path.join(__dirname, 'saves', 'savegame.json');

function newPlayer(name) {
  // One plain object is easier to read than several parallel arrays.
  return { name, hp: 100, maxHp: 100, battery: 8, shield: 0, segment: 0, inventory: ['Repair Kit'] };
}

function showStatus(player, enemy) {
  console.log(`\n${player.name} HP [${bar(player.hp, player.maxHp)}] ${player.hp}/${player.maxHp}`);
  console.log(`Battery   [${bar(player.battery, 8)}] ${player.battery}/8`);
  if (player.shield > 0) console.log(`Shield: next hit reduced by ${player.shield}`);
  if (enemy) console.log(`${enemy.name} HP [${bar(enemy.hp, enemy.maxHp)}] ${enemy.hp}/${enemy.maxHp}`);
}

function addLoot(player, item) {
  if (player.inventory.length >= 10) {
    console.log(`Inventory full. You leave the ${item.name} behind.`);
    return;
  }
  player.inventory.push(item.name);
  console.log(`Picked up ${item.name}.`);
}

async function useItem(rl, player, enemy, loot) {
  if (!player.inventory.length) {
    console.log('No items to use.');
    return 'cancel';
  }

  console.log('\nInventory:');
  player.inventory.forEach((item, index) => console.log(`${index + 1}. ${item}`));
  console.log('0. Cancel');
  const choice = Number(await ask(rl, '> '));
  if (!choice) return 'cancel';

  const itemName = player.inventory[choice - 1];
  const item = loot.find((entry) => entry.name === itemName);
  if (!item) return 'cancel';

  player.inventory.splice(choice - 1, 1);
  if (item.type === 'heal') {
    player.hp = Math.min(player.maxHp, player.hp + item.value);
    console.log(`${item.name} restores ${item.value} HP.`);
    return 'used';
  }
  if (item.type === 'damage') {
    enemy.hp = Math.max(0, enemy.hp - item.value);
    console.log(`${item.name} hits for ${item.value} damage.`);
    return 'used';
  }
  if (item.type === 'shield') {
    player.shield = Math.max(player.shield, item.value);
    console.log(`${item.name} will block ${item.value} damage from the next hit.`);
    return 'used';
  }
  if (item.type === 'battery') {
    player.battery = Math.min(8, player.battery + item.value);
    console.log(`${item.name} restores ${item.value} battery.`);
    return 'used';
  }
  console.log(`${item.name} covers your escape.`);
  return 'fled';
}

async function combat(rl, player, template, loot) {
  const enemy = { ...template, maxHp: template.hp };

  while (player.hp > 0 && enemy.hp > 0) {
    showStatus(player, enemy);
    console.log('\n1. Attack\n2. Use item\n3. Flee');
    const choice = await ask(rl, '> ');

    if (choice === '1') {
      const damage = roll(10, 18);
      enemy.hp = Math.max(0, enemy.hp - damage);
      console.log(`You deal ${damage} damage.`);
    } else if (choice === '2') {
      const result = await useItem(rl, player, enemy, loot);
      if (result === 'cancel') continue;
      if (result === 'fled') return 'fled';
    } else if (choice === '3') {
      if (roll(1, 100) <= 40) {
        console.log('You slip away into the rain.');
        return 'fled';
      }
      console.log('You fail to escape.');
    } else {
      console.log('Choose 1, 2, or 3.');
      continue;
    }

    if (enemy.hp <= 0) {
      console.log(`You defeat ${enemy.name}.`);
      return 'win';
    }

    const rawHit = Math.max(1, template.damage + roll(-2, 2));
    const blocked = Math.min(rawHit, player.shield);
    const damage = rawHit - blocked;
    player.shield = 0;
    player.hp = Math.max(0, player.hp - damage);
    console.log(`${enemy.name} hits for ${damage} damage${blocked ? ` (${blocked} blocked)` : ''}.`);
  }

  return player.hp > 0 ? 'win' : 'lose';
}

async function saveGame(state) {
  await saveJson(SAVE_FILE, state);
  console.log(`Game saved to ${SAVE_FILE}.`);
}

async function loadGame() {
  try {
    // Save files are normal JSON, so loading is one await + one parse.
    return await loadJson(SAVE_FILE);
  } catch (error) {
    if (error.code === 'ENOENT') return null;
    throw error;
  }
}

async function runAlley(rl, state, data) {
  // Each segment resolves once, then the battery drops and the player moves on.
  while (state.player.hp > 0 && state.player.battery > 0 && state.player.segment < data.segments.length) {
    const segment = data.segments[state.player.segment];
    console.log(`\n=== Segment ${state.player.segment + 1} of ${data.segments.length} ===`);
    console.log(segment.text);

    if (segment.type === 'enemy') {
      const result = await combat(rl, state.player, data.enemies[segment.enemy], data.loot);
      if (result === 'lose') break;
    } else if (segment.type === 'loot') {
      addLoot(state.player, data.loot[segment.loot]);
    } else if (segment.type === 'event') {
      state.player[segment.stat] = Math.max(0, Math.min(segment.stat === 'battery' ? 8 : state.player.maxHp, state.player[segment.stat] + segment.value));
      console.log(`${segment.stat} changes by ${segment.value}.`);
    } else if (segment.type === 'finish') {
      console.log(`\n${state.player.name} reaches the glowing data drop and escapes with the payload.`);
      return;
    }

    state.player.segment += 1;
    state.player.battery -= 1;
    if (state.player.hp <= 0 || state.player.battery <= 0) break;

    const next = await ask(rl, 'Press Enter to continue, or type s to save and quit: ');
    if (next.toLowerCase() === 's') {
      await saveGame(state);
      return;
    }
  }

  console.log(state.player.hp <= 0 ? '\nYour drone is scrap metal. Game over.' : '\nBattery empty. The alley goes dark.');
}

async function loadData() {
  // Promise.all keeps the startup code short while loading three JSON files.
  const [enemies, loot, segments] = await Promise.all([
    loadJson(path.join(DATA_DIR, 'enemies.json')),
    loadJson(path.join(DATA_DIR, 'loot.json')),
    loadJson(path.join(DATA_DIR, 'segments.json'))
  ]);
  return { enemies, loot, segments };
}

function showHelp() {
  console.log('\nHow to play:');
  console.log('- Attack, use items, or flee during combat.');
  console.log('- Battery drops after each alley segment, so keep moving.');
  console.log('- Save after a segment, then reload from the main menu.');
}

async function main() {
  const data = await loadData();
  const rl = createInterface();

  console.log('NEON ALLEY - Node.js Spike');
  console.log('Run it with: node game.js');

  while (true) {
    console.log('\n1. New run\n2. Load run\n3. How to play\n4. Quit');
    const choice = await ask(rl, '> ');

    if (choice === '1') {
      const name = (await ask(rl, 'Enter your drone name: ')) || 'Phantom';
      await runAlley(rl, { player: newPlayer(name) }, data);
    } else if (choice === '2') {
      const state = await loadGame();
      if (!state) console.log('No save file found yet.');
      else await runAlley(rl, state, data);
    } else if (choice === '3') {
      showHelp();
    } else if (choice === '4') {
      break;
    } else {
      console.log('Choose 1, 2, 3, or 4.');
    }
  }

  rl.close();
}

main().catch((error) => {
  console.error('Game failed to start:', error.message);
  process.exitCode = 1;
});
