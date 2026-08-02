const fsSync = require('fs');
const fs = require('fs/promises');
const path = require('path');
const readline = require('readline');
const { stdin, stdout } = require('process');

function createInterface() {
  if (!stdin.isTTY) {
    return {
      index: 0,
      lines: fsSync.readFileSync(0, 'utf8').split(/\r?\n/),
      close() {}
    };
  }
  return readline.createInterface({ input: stdin, output: stdout });
}

async function ask(rl, prompt) {
  if (rl.lines) {
    stdout.write(prompt);
    return (rl.lines[rl.index++] || '').trim();
  }
  return new Promise((resolve) => rl.question(prompt, (answer) => resolve(answer.trim())));
}

function bar(value, max, width = 10) {
  const safeMax = Math.max(1, max);
  const filled = Math.max(0, Math.min(width, Math.round((value / safeMax) * width)));
  return `${'█'.repeat(filled)}${'░'.repeat(width - filled)}`;
}

function roll(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

async function loadJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, 'utf8'));
}

async function saveJson(filePath, data) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(data, null, 2)}\n`, 'utf8');
}

module.exports = { ask, bar, createInterface, loadJson, roll, saveJson };
