const assert = require('node:assert/strict');
const fs = require('fs/promises');
const os = require('os');
const path = require('path');
const test = require('node:test');
const { bar, loadJson, saveJson } = require('./utils');

test('bar draws a 10-cell meter', () => {
  assert.equal(bar(5, 10), '█████░░░░░');
});

test('saveJson and loadJson round-trip state', async () => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'neon-alley-'));
  const file = path.join(dir, 'save.json');
  const state = { player: { name: 'Ace', hp: 91, battery: 7 } };

  await saveJson(file, state);
  assert.deepEqual(await loadJson(file), state);
});
