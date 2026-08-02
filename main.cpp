// ============================================================
// NEON ALLEY — Drone Runner v1.0 (MVP)
// CSC 134 Sample Project: Arrays & File I/O
//
// A text-based cyberpunk dungeon crawl. Your surveillance
// drone threads through the neon-soaked back alleys of the
// Sprawl. Fight hostiles, scavenge loot, and reach the data
// drop before your battery dies.
//
// Build: g++ -o neon_alley main.cpp
// Run:   ./neon_alley
// ============================================================

#include <iostream>
#include <fstream>
#include <limits>
#include <string>
#include <cstdlib>
#include <ctime>

using namespace std;

// ============================================================
// DESIGN NOTE: These are global variables. That means any
// function can read or change them. This works for a small
// program, but gets dangerous fast. When we learn about
// passing parameters and returning values, we'll refactor
// this so each function only touches what it needs.
// ============================================================

// --- Enemy Roster (loaded from enemies.txt) ---
const int MAX_ENEMIES = 10;
string enemyName[MAX_ENEMIES];
int    enemyHP[MAX_ENEMIES];
int    enemyDamage[MAX_ENEMIES];
int    enemyXP[MAX_ENEMIES];
int    enemyCount = 0;

// --- Loot Table (loaded from loot.txt) ---
const int MAX_LOOT = 10;
string lootName[MAX_LOOT];
string lootType[MAX_LOOT];
int    lootValue[MAX_LOOT];
int    lootCount = 0;

// --- Alley Map (loaded from alley.txt) ---
const int MAX_SEGMENTS = 20;
string segType[MAX_SEGMENTS];
int    segIndex[MAX_SEGMENTS];
string segExtra[MAX_SEGMENTS];
string segDescription[MAX_SEGMENTS];
int    segmentCount = 0;

// --- Player State ---
const int MAX_BATTERY = 15;
string playerName;
int    playerHP;
int    playerMaxHP    = 100;
int    battery        = MAX_BATTERY;
int    currentSegment = 0;
int    playerXP       = 0;

const int MAX_INVENTORY = 10;
string inventory[MAX_INVENTORY];
int    inventoryCount = 0;

// ============================================================
// PARSING HELPER
// Splits a pipe-delimited line into tokens.
// Students see: one function, used by three loaders.
// ============================================================
void splitLine(string line, string tokens[], int maxTokens, int &count) {
    count = 0;
    while (line.length() > 0 && count < maxTokens) {
        int pos = line.find('|');
        if (pos == (int)string::npos) {
            tokens[count] = line;
            count++;
            break;
        }
        tokens[count] = line.substr(0, pos);
        count++;
        line = line.substr(pos + 1);
    }
}

bool tryParseInt(const string &text, int &value) {
    try {
        size_t pos = 0;
        value = stoi(text, &pos);
        return pos == text.length();
    } catch (...) {
        return false;
    }
}

void warnBadDataRow(const string &filename, int lineNumber, const string &line) {
    cout << "WARNING: Skipping bad data in " << filename
         << " at line " << lineNumber << ": " << line << endl;
}

int readIntChoice(const string &prompt) {
    int choice;
    while (true) {
        cout << prompt;
        if (cin >> choice) {
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            return choice;
        }

        cout << "  Invalid choice." << endl;
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
}

bool readSaveInt(ifstream &fin, const string &fieldName, int &value) {
    string line;
    if (!getline(fin, line) || !tryParseInt(line, value)) {
        cout << "  ERROR: Save file has invalid " << fieldName << "." << endl;
        return false;
    }
    return true;
}

// ============================================================
// DATA LOADING
// ============================================================

bool loadEnemies(string filename) {
    ifstream fin(filename.c_str());
    if (!fin.is_open()) {
        cout << "ERROR: Could not open " << filename << endl;
        return false;
    }
    enemyCount = 0;
    string line;
    int lineNumber = 0;
    while (getline(fin, line) && enemyCount < MAX_ENEMIES) {
        lineNumber++;
        if (line.length() == 0) continue;
        string tokens[4];
        int tokenCount = 0;
        int hp = 0;
        int damage = 0;
        int xp = 0;
        splitLine(line, tokens, 4, tokenCount);
        if (tokenCount != 4 ||
            !tryParseInt(tokens[1], hp) ||
            !tryParseInt(tokens[2], damage) ||
            !tryParseInt(tokens[3], xp)) {
            warnBadDataRow(filename, lineNumber, line);
            continue;
        }
        enemyName[enemyCount]   = tokens[0];
        enemyHP[enemyCount]     = hp;
        enemyDamage[enemyCount] = damage;
        enemyXP[enemyCount]     = xp;
        enemyCount++;
    }
    fin.close();
    cout << "  Loaded " << enemyCount << " enemies." << endl;
    return true;
}

bool loadLoot(string filename) {
    ifstream fin(filename.c_str());
    if (!fin.is_open()) {
        cout << "ERROR: Could not open " << filename << endl;
        return false;
    }
    lootCount = 0;
    string line;
    int lineNumber = 0;
    while (getline(fin, line) && lootCount < MAX_LOOT) {
        lineNumber++;
        if (line.length() == 0) continue;
        string tokens[3];
        int tokenCount = 0;
        int value = 0;
        splitLine(line, tokens, 3, tokenCount);
        if (tokenCount != 3 || !tryParseInt(tokens[2], value)) {
            warnBadDataRow(filename, lineNumber, line);
            continue;
        }
        lootName[lootCount]  = tokens[0];
        lootType[lootCount]  = tokens[1];
        lootValue[lootCount] = value;
        lootCount++;
    }
    fin.close();
    cout << "  Loaded " << lootCount << " loot items." << endl;
    return true;
}

bool loadAlley(string filename) {
    ifstream fin(filename.c_str());
    if (!fin.is_open()) {
        cout << "ERROR: Could not open " << filename << endl;
        return false;
    }
    segmentCount = 0;
    string line;
    int lineNumber = 0;
    while (getline(fin, line) && segmentCount < MAX_SEGMENTS) {
        lineNumber++;
        if (line.length() == 0) continue;
        string tokens[4];
        int tokenCount = 0;
        int value = 0;
        splitLine(line, tokens, 4, tokenCount);

        if (tokenCount < 3) {
            warnBadDataRow(filename, lineNumber, line);
            continue;
        }

        segType[segmentCount] = tokens[0];

        if (tokens[0] == "event") {
            // event|stat|value|description
            if (tokenCount < 4 || !tryParseInt(tokens[2], value)) {
                warnBadDataRow(filename, lineNumber, line);
                continue;
            }
            segExtra[segmentCount]      = tokens[1];
            segIndex[segmentCount]      = value;
            segDescription[segmentCount] = tokens[3];
        } else {
            // enemy|index|description  or  loot|index|description  or  finish|index|description
            if (!tryParseInt(tokens[1], value)) {
                warnBadDataRow(filename, lineNumber, line);
                continue;
            }
            segIndex[segmentCount]       = value;
            segDescription[segmentCount] = tokens[2];
            segExtra[segmentCount]       = "";
        }
        segmentCount++;
    }
    fin.close();
    cout << "  Loaded " << segmentCount << " alley segments." << endl;
    return true;
}

// ============================================================
// SAVE / LOAD GAME
// ============================================================

void saveGame(string filename) {
    ofstream fout(filename.c_str());
    if (!fout.is_open()) {
        cout << "ERROR: Could not save game." << endl;
        return;
    }
    fout << "NEON_ALLEY_SAVE_V1" << endl;
    fout << playerName << endl;
    fout << playerHP << endl;
    fout << playerMaxHP << endl;
    fout << battery << endl;
    fout << currentSegment << endl;
    fout << playerXP << endl;
    fout << inventoryCount << endl;
    for (int i = 0; i < inventoryCount; i++) {
        fout << inventory[i] << endl;
    }
    fout.close();
    cout << "\n  >> Game saved. Stay sharp, " << playerName << ".\n" << endl;
}

bool loadGame(string filename) {
    ifstream fin(filename.c_str());
    if (!fin.is_open()) {
        cout << "  No saved run found." << endl;
        return false;
    }
    string header;
    getline(fin, header);
    if (header != "NEON_ALLEY_SAVE_V1") {
        cout << "  ERROR: Save file is corrupt or wrong version." << endl;
        fin.close();
        return false;
    }
    string loadedPlayerName;
    int loadedPlayerHP = 0;
    int loadedPlayerMaxHP = 0;
    int loadedBattery = 0;
    int loadedCurrentSegment = 0;
    int loadedPlayerXP = 0;
    int savedInventoryCount = 0;
    int loadedInventoryCount = 0;
    string loadedInventory[MAX_INVENTORY];

    if (!getline(fin, loadedPlayerName)) {
        cout << "  ERROR: Save file is missing player name." << endl;
        return false;
    }
    if (!readSaveInt(fin, "player HP", loadedPlayerHP)) return false;
    if (!readSaveInt(fin, "player max HP", loadedPlayerMaxHP)) return false;
    if (!readSaveInt(fin, "battery", loadedBattery)) return false;
    if (!readSaveInt(fin, "current segment", loadedCurrentSegment)) return false;
    if (!readSaveInt(fin, "player XP", loadedPlayerXP)) return false;
    if (!readSaveInt(fin, "inventory count", savedInventoryCount)) return false;

    if (loadedCurrentSegment < 0 || loadedCurrentSegment > segmentCount) {
        cout << "  ERROR: Save file has invalid current segment." << endl;
        return false;
    }
    if (loadedPlayerMaxHP < 1) {
        cout << "  ERROR: Save file has invalid max HP." << endl;
        return false;
    }
    if (loadedPlayerHP < 0 || loadedPlayerHP > loadedPlayerMaxHP) {
        cout << "  ERROR: Save file has invalid current HP." << endl;
        return false;
    }
    if (loadedBattery < 0) {
        cout << "  ERROR: Save file has invalid battery level." << endl;
        return false;
    }

    int inventoryLinesToRead = savedInventoryCount;
    if (inventoryLinesToRead < 0) inventoryLinesToRead = 0;
    loadedInventoryCount = inventoryLinesToRead;
    if (loadedInventoryCount > MAX_INVENTORY) loadedInventoryCount = MAX_INVENTORY;

    for (int i = 0; i < inventoryLinesToRead; i++) {
        string itemName;
        if (!getline(fin, itemName)) {
            cout << "  ERROR: Save file is missing inventory data." << endl;
            return false;
        }
        if (i < MAX_INVENTORY) {
            loadedInventory[i] = itemName;
        }
    }

    playerName = loadedPlayerName;
    playerHP = loadedPlayerHP;
    playerMaxHP = loadedPlayerMaxHP;
    battery = loadedBattery;
    currentSegment = loadedCurrentSegment;
    playerXP = loadedPlayerXP;
    inventoryCount = loadedInventoryCount;
    for (int i = 0; i < MAX_INVENTORY; i++) {
        inventory[i] = (i < inventoryCount) ? loadedInventory[i] : "";
    }
    fin.close();
    cout << "\n  >> Run restored. Welcome back, " << playerName << ".\n" << endl;
    return true;
}

// ============================================================
// DISPLAY HELPERS
// ============================================================

void displayHPBar(string label, int current, int maximum) {
    if (maximum <= 0) maximum = 1;
    int barWidth = 10;
    int filled = (current * barWidth) / maximum;
    if (filled < 0) filled = 0;
    if (filled > barWidth) filled = barWidth;

    cout << label << ": [";
    for (int i = 0; i < barWidth; i++) {
        if (i < filled)
            cout << "#";
        else
            cout << ".";
    }
    cout << "] " << current << "/" << maximum;
}

void displayStatus() {
    cout << "\n=== SEGMENT " << (currentSegment + 1) << " of " << segmentCount << " ===" << endl;
    cout << "Battery: [";
    int batBar = 10;
    int batFill = (battery * batBar) / MAX_BATTERY;
    if (batFill < 0) batFill = 0;
    if (batFill > batBar) batFill = batBar;
    for (int i = 0; i < batBar; i++) {
        if (i < batFill) cout << "|";
        else cout << " ";
    }
    cout << "] " << battery << "    ";
    displayHPBar("HP", playerHP, playerMaxHP);
    cout << "    XP: " << playerXP << endl;
}

// ============================================================
// INVENTORY
// ============================================================

void showInventory() {
    if (inventoryCount == 0) {
        cout << "  Inventory is empty." << endl;
        return;
    }
    cout << "  --- Inventory ---" << endl;
    for (int i = 0; i < inventoryCount; i++) {
        cout << "  " << (i + 1) << ". " << inventory[i] << endl;
    }
}

void removeInventoryItem(int index) {
    for (int i = index; i < inventoryCount - 1; i++) {
        inventory[i] = inventory[i + 1];
    }
    inventory[inventoryCount - 1] = "";
    inventoryCount--;
}

// Find a loot item's index in the loot table by name
int findLootIndex(string itemName) {
    for (int i = 0; i < lootCount; i++) {
        if (lootName[i] == itemName) {
            return i;
        }
    }
    return -1;
}

// Use an item from inventory. Returns bonus damage dealt (for combat).
int useItem() {
    if (inventoryCount == 0) {
        cout << "  No items to use!" << endl;
        return 0;
    }
    showInventory();
    int choice = readIntChoice("  Use which item? (0 = cancel): ");

    if (choice < 1 || choice > inventoryCount) {
        cout << "  Cancelled." << endl;
        return 0;
    }

    int invIdx = choice - 1;
    string itemName = inventory[invIdx];
    int lootIdx = findLootIndex(itemName);

    if (lootIdx == -1) {
        cout << "  ERROR: Item data not found for " << itemName << "." << endl;
        return 0;
    }

    string type = lootType[lootIdx];
    int value   = lootValue[lootIdx];
    int bonusDamage = 0;

    if (type == "heal") {
        playerHP += value;
        if (playerHP > playerMaxHP) playerHP = playerMaxHP;
        cout << "  Used " << itemName << ": restored " << value << " HP. (HP: " << playerHP << ")" << endl;
    } else if (type == "damage") {
        bonusDamage = value;
        cout << "  Used " << itemName << ": +" << value << " bonus damage this turn!" << endl;
    } else if (type == "shield") {
        playerHP += value;  // shield acts as temp HP for simplicity
        cout << "  Used " << itemName << ": shield absorbs " << value << " damage. (HP: " << playerHP << ")" << endl;
    } else if (type == "battery") {
        battery += value;
        cout << "  Used " << itemName << ": +" << value << " battery charge. (Battery: " << battery << ")" << endl;
    } else if (type == "escape") {
        bonusDamage = -1;  // special signal: guaranteed escape
        cout << "  Used " << itemName << ": smoke fills the alley!" << endl;
    }

    removeInventoryItem(invIdx);
    return bonusDamage;
}

// ============================================================
// COMBAT
// ============================================================

// Returns true if player survived, false if dead
bool combat(int enemyIdx) {
    if (enemyIdx < 0 || enemyIdx >= enemyCount) {
        cout << "  ERROR: Invalid enemy index." << endl;
        return true;
    }

    string eName = enemyName[enemyIdx];
    int eHP      = enemyHP[enemyIdx];
    int eDmg     = enemyDamage[enemyIdx];
    int eXP      = enemyXP[enemyIdx];

    cout << "\n  !! HOSTILE CONTACT: " << eName << " (HP: " << eHP << ") !!\n" << endl;

    while (eHP > 0 && playerHP > 0) {
        cout << "  1. Attack" << endl;
        cout << "  2. Use Item (" << inventoryCount << " items)" << endl;
        cout << "  3. Try to Flee" << endl;
        int choice = readIntChoice("> ");

        if (choice == 1) {
            // Player attacks
            int dmg = 10 + rand() % 11;  // 10-20
            eHP -= dmg;
            if (eHP <= 0) {
                cout << "\n  You fire: " << dmg << " damage! " << eName << " DESTROYED." << endl;
                cout << "  +" << eXP << " XP" << endl;
                playerXP += eXP;
                return true;
            }
            cout << "\n  You fire: " << dmg << " damage! " << eName << " HP: " << eHP << endl;

            // Enemy attacks
            int eDmgRoll = eDmg + (rand() % 5 - 2);  // base +/- 2
            if (eDmgRoll < 1) eDmgRoll = 1;
            playerHP -= eDmgRoll;
            cout << "  " << eName << " strikes: " << eDmgRoll << " damage! Your HP: " << playerHP << endl;

            if (playerHP <= 0) {
                return false;
            }
            cout << endl;

        } else if (choice == 2) {
            int result = useItem();
            if (result == -1) {
                // Smoke bomb — guaranteed escape
                cout << "  You vanish into the smoke!" << endl;
                return true;
            } else if (result > 0) {
                // Bonus damage item
                eHP -= result;
                cout << "  Bonus hit: " << result << " damage!";
                if (eHP <= 0) {
                    cout << " " << eName << " DESTROYED." << endl;
                    cout << "  +" << eXP << " XP" << endl;
                    playerXP += eXP;
                    return true;
                }
                cout << " " << eName << " HP: " << eHP << endl;
            }
            // Enemy still attacks after item use
            int eDmgRoll = eDmg + (rand() % 5 - 2);
            if (eDmgRoll < 1) eDmgRoll = 1;
            playerHP -= eDmgRoll;
            cout << "  " << eName << " strikes: " << eDmgRoll << " damage! Your HP: " << playerHP << endl;
            if (playerHP <= 0) return false;
            cout << endl;

        } else if (choice == 3) {
            // Flee attempt: 40% success
            int roll = rand() % 100;
            if (roll < 40) {
                cout << "\n  You disengage and slip away!" << endl;
                return true;
            } else {
                cout << "\n  Escape failed!" << endl;
                // Enemy gets a free hit
                int eDmgRoll = eDmg + (rand() % 5 - 2);
                if (eDmgRoll < 1) eDmgRoll = 1;
                playerHP -= eDmgRoll;
                cout << "  " << eName << " strikes: " << eDmgRoll << " damage! Your HP: " << playerHP << endl;
                if (playerHP <= 0) return false;
                cout << endl;
            }
        } else {
            cout << "  Invalid choice." << endl;
        }
    }
    return playerHP > 0;
}

// ============================================================
// ENCOUNTER HANDLERS
// ============================================================

void findLoot(int lootIdx) {
    if (lootIdx < 0 || lootIdx >= lootCount) {
        cout << "  ERROR: Invalid loot index." << endl;
        return;
    }
    cout << "\n  Found: " << lootName[lootIdx] << " (" << lootType[lootIdx] << ")" << endl;
    if (inventoryCount < MAX_INVENTORY) {
        inventory[inventoryCount] = lootName[lootIdx];
        inventoryCount++;
        cout << "  Added to inventory. (" << inventoryCount << "/" << MAX_INVENTORY << " slots used)" << endl;
    } else {
        cout << "  Inventory full! Leave the " << lootName[lootIdx] << " behind." << endl;
    }
}

void applyEvent(string stat, int value) {
    if (stat == "battery") {
        battery += value;
        cout << "\n  Battery +" << value << "! (Battery: " << battery << ")" << endl;
    } else if (stat == "hp") {
        playerHP += value;
        if (playerHP > playerMaxHP) playerHP = playerMaxHP;
        cout << "\n  HP +" << value << "! (HP: " << playerHP << ")" << endl;
    } else {
        cout << "\n  [Event effect: " << stat << " +" << value << "]" << endl;
    }
}

// ============================================================
// CORE GAME LOOP
// ============================================================

void runAlley() {
    while (currentSegment < segmentCount && playerHP > 0 && battery > 0) {
        displayStatus();
        cout << segDescription[currentSegment] << endl;

        string type = segType[currentSegment];

        if (type == "enemy") {
            bool survived = combat(segIndex[currentSegment]);
            if (!survived) {
                playerHP = 0;
                break;
            }
        } else if (type == "loot") {
            findLoot(segIndex[currentSegment]);
        } else if (type == "event") {
            applyEvent(segExtra[currentSegment], segIndex[currentSegment]);
        } else if (type == "finish") {
            cout << "\n  ============================================" << endl;
            cout << "  = = =  DATA DROP REACHED  = = =" << endl;
            cout << "  ============================================" << endl;
            cout << "  Mission complete, " << playerName << "!" << endl;
            cout << "  Final HP: " << playerHP << "/" << playerMaxHP << endl;
            cout << "  Battery remaining: " << battery << endl;
            cout << "  Total XP: " << playerXP << endl;
            cout << "  Items carried: " << inventoryCount << endl;
            cout << "  ============================================\n" << endl;
            return;
        }

        battery--;
        if (battery <= 0) {
            cout << "\n  !! BATTERY DEPLETED !! Signal lost..." << endl;
            break;
        }

        if (battery <= 3) {
            cout << "\n  ** WARNING: Battery critical! " << battery << " moves remaining **" << endl;
        }

        currentSegment++;

        // Offer save between segments
        if (currentSegment < segmentCount && playerHP > 0) {
            cout << "\n  Continue deeper? (s = save & quit, enter = continue): ";
            string input;
            getline(cin >> ws, input);
            if (input == "s" || input == "S") {
                saveGame("savegame.txt");
                return;
            }
        }
    }

    // End states
    if (playerHP <= 0) {
        cout << "\n  ============================================" << endl;
        cout << "  = = =  SIGNAL LOST  = = =" << endl;
        cout << "  ============================================" << endl;
        cout << "  Your drone goes dark in the alley." << endl;
        cout << "  Segments cleared: " << currentSegment << "/" << segmentCount << endl;
        cout << "  Total XP: " << playerXP << endl;
        cout << "  ============================================\n" << endl;
    } else if (battery <= 0) {
        cout << "\n  ============================================" << endl;
        cout << "  = = =  BATTERY DEAD  = = =" << endl;
        cout << "  ============================================" << endl;
        cout << "  Your drone powers down mid-alley." << endl;
        cout << "  Segments cleared: " << currentSegment << "/" << segmentCount << endl;
        cout << "  Total XP: " << playerXP << endl;
        cout << "  ============================================\n" << endl;
    }
}

// ============================================================
// MENU & SETUP
// ============================================================

void newRun() {
    cout << "\nEnter drone callsign: ";
    getline(cin >> ws, playerName);
    playerHP       = playerMaxHP;
    battery        = MAX_BATTERY;
    currentSegment = 0;
    playerXP       = 0;
    inventoryCount = 0;

    cout << "\n  Drone \"" << playerName << "\" online. Battery charged. Moving out.\n" << endl;
    runAlley();
}

void showHowToPlay() {
    cout << "\n============================================" << endl;
    cout << "            HOW TO PLAY" << endl;
    cout << "============================================" << endl;
    cout << "You pilot a surveillance drone through the" << endl;
    cout << "back alleys of the Sprawl. Each segment of" << endl;
    cout << "the alley holds an encounter:" << endl;
    cout << endl;
    cout << "  ENEMY - Fight or flee. Combat is turn-based." << endl;
    cout << "  LOOT  - Scavenge useful items." << endl;
    cout << "  EVENT - Something happens to your drone." << endl;
    cout << endl;
    cout << "Your drone has limited BATTERY (moves) and" << endl;
    cout << "HP (hull integrity). Reach the data drop at" << endl;
    cout << "the end of the alley to win." << endl;
    cout << endl;
    cout << "In combat:" << endl;
    cout << "  Attack     - Deal 10-20 damage" << endl;
    cout << "  Use Item   - Heal, deal bonus damage, etc." << endl;
    cout << "  Flee       - 40% chance to escape" << endl;
    cout << endl;
    cout << "You can save between segments and continue" << endl;
    cout << "your run later." << endl;
    cout << "============================================\n" << endl;
}

int showMainMenu() {
    cout << "======================================" << endl;
    cout << "       N E O N   A L L E Y" << endl;
    cout << "    Drone Runner v1.0 (MVP)" << endl;
    cout << "======================================" << endl;
    cout << "  1. New Run" << endl;
    cout << "  2. Continue Run" << endl;
    cout << "  3. How to Play" << endl;
    cout << "  4. Quit" << endl;
    cout << "======================================" << endl;
    return readIntChoice("> ");
}

// ============================================================
// MAIN
// ============================================================

int main() {
    srand(time(0));

    cout << "\nLoading game data..." << endl;
    if (!loadEnemies("data/enemies.txt")) return 1;
    if (!loadLoot("data/loot.txt"))       return 1;
    if (!loadAlley("data/alley.txt"))     return 1;
    cout << "Ready.\n" << endl;

    bool running = true;
    while (running) {
        int choice = showMainMenu();
        switch (choice) {
            case 1:
                newRun();
                break;
            case 2:
                if (loadGame("savegame.txt")) {
                    runAlley();
                }
                break;
            case 3:
                showHowToPlay();
                break;
            case 4:
                cout << "\n  Signal terminated. Stay in the shadows.\n" << endl;
                running = false;
                break;
            default:
                cout << "  Invalid choice." << endl;
                break;
        }
    }

    return 0;
}
