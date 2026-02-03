# Minecraft RL Agent - Action Guide

This guide lists all available actions for the Minecraft RL agent.

## Quick Reference

### Movement Actions
- `0` - No-op / Idle
- `1` - Move Forward
- `2` - Move Backward
- `3` - Move Left
- `4` - Move Right
- `5` - Jump

### Combat & Mining
- `6` - Attack (left-click)
- `7` - Use Item (right-click)
- `8` - Mine Block (hold left-click)

### Inventory Management
- `9-17` - Select hotbar slot 1-9
- `18` - Drop Item

### Crafting & Building
- `19` - Place Block
- `20` - Craft Recipe
- `21` - Smelt Recipe

### Vision
- `22` - Look Up
- `23` - Look Down
- `24` - Look Left
- `25` - Look Right
- `26` - Look Behind
- `27` - Look Around
- `28` - Look At (specific coordinates)

### Advanced Actions
- `29-35` - Sneak, Sprint, Walk, etc.
- `36-40` - Equipment management
- `41-49` - Various specialized actions
- `50` - EAT

---

## Detailed Action List

```
ID  | Action Name        | Description                      | Usage
----|-------------------|-----------------------------------|------------------------------
0   | NO_OP            | Do nothing                         | Wait/Idle
1   | MOVE_FORWARD     | Move forward                        | Basic movement
2   | MOVE_BACKWARD    | Move backward                       | Basic movement
3   | MOVE_LEFT        | Move left                           | Basic movement
4   | MOVE_RIGHT       | Move right                          | Basic movement
5   | JUMP             | Jump                                | Parkour
6   | ATTACK           | Attack (left-click)                   | Combat, break blocks
7   | USE_ITEM         | Use item (right-click)               | Place blocks, eat food
8   | MINE_BLOCK       | Mine block (hold click)              | Mining
9   | SELECT_SLOT_1    | Select hotbar slot 1                 | Switch tool
10  | SELECT_SLOT_2    | Select hotbar slot 2                 | Switch tool
11  | SELECT_SLOT_3    | Select hotbar slot 3                 | Switch tool
12  | SELECT_SLOT_4    | Select hotbar slot 4                 | Switch tool
13  | SELECT_SLOT_5    | Select hotbar slot 5                 | Switch tool
14  | SELECT_SLOT_6    | Select hotbar slot 6                 | Switch tool
15  | SELECT_SLOT_7    | Select hotbar slot 7                 | Switch tool
16  | SELECT_SLOT_8    | Select hotbar slot 8                 | Switch tool
17  | SELECT_SLOT_9    | Select hotbar slot 9                 | Switch tool
18  | DROP_ITEM        | Drop held item                      | Clear inventory
19  | PLACE_BLOCK      | Place block                         | Building
20  | CRAFT_RECIPE     | Craft recipe                        | Crafting
21  | SMELT_RECIPE     | Smelt recipe                        | Smelting
22  | LOOK_UP          | Look up                             | Vision
23  | LOOK_DOWN        | Look down                           | Vision
24  | LOOK_LEFT        | Look left                           | Vision
25  | LOOK_RIGHT       | Look right                          | Vision
26  | LOOK_BEHIND      | Look behind                         | Vision
27  | LOOK_AROUND      | Look around (360°)                  | Vision
28  | LOOK_AT          | Look at specific coordinates          | Vision
29  | SNEAK            | Sneak (shift)                        | Stealth
30  | SPRINT           | Sprint (run fast)                   | Speed
31  | WALK             | Walk (slow)                         | Precision
32  | EQUIP_ARMOR_1    | Equip armor slot 1                  | Equipment
33  | EQUIP_ARMOR_2    | Equip armor slot 2                  | Equipment
34  | EQUIP_ARMOR_3    | Equip armor slot 3                  | Equipment
35  | EQUIP_ARMOR_4    | Equip armor slot 4                  | Equipment
36  | DROP_SLOT_1      | Drop item from slot 1               | Inventory
37  | DROP_SLOT_2      | Drop item from slot 2               | Inventory
38  | DROP_SLOT_3      | Drop item from slot 3               | Inventory
39  | DROP_SLOT_4      | Drop item from slot 4               | Inventory
40  | DROP_SLOT_5      | Drop item from slot 5               | Inventory
41  | INTERACT_ENTITY  | Interact with entity                | Trading, animals
42  | PICKUP_ITEM      | Pickup item                         | Collecting
43  | OPEN_INVENTORY   | Open inventory                      | Management
44  | CLOSE_INVENTORY  | Close inventory                     | Management
45  | SWAP_HANDS       | Swap hands (off-hand ↔ main)      | Combat
46  | START_SNEAKING   | Start sneaking                      | Stealth
    | STOP_SNEAKING    | Stop sneaking                       | Stealth
    | TOGGLE_SNEAK     | Toggle sneak                         | Stealth
47  | DROP_ALL         | Drop all items                      | Clear inventory
48  | SORT_INVENTORY   | Sort inventory                      | Organization
49  | CUSTOM_ACTION_1  | Custom action                       | Future use
    | CUSTOM_ACTION_2  | Custom action                       | Future use
50  | EAT              | Eat food                            | Survival
```

---

## Recording Good Demonstrations

### DO Show the Bot:
1. **Basic Movement** - Walk in different directions
2. **Mining** - Mine dirt, stone, ores (several examples)
3. **Crafting** - Craft planks, sticks, tools
4. **Building** - Place blocks to make simple structures
5. **Survival** - Eat when hungry, avoid danger

### DON'T Show:
- Getting stuck in loops
- Dying repeatedly
- Doing useless actions
- Very long activities (like building a castle - keep it simple)

### Tips for Good Demos:
- **Keep episodes short** (50-200 steps each)
- **Focus on ONE skill at a time**
- **Show variations** (mine dirt, then stone, then coal)
- **Include failures** (try, fail, try again)
- **Show context** (look at block, approach it, mine it)

---

## Example Recording Session

```
Episode 1: Mining Basics
- Look around → Find dirt → Approach → Mine (x5)

Episode 2: Movement
- Walk forward → Turn left → Walk → Jump → Turn right

Episode 3: Crafting
- Open inventory → Select logs → Craft planks

Episode 4: Building
- Place block → Move → Place another → Place another
```

**The more varied your demonstrations, the better the bot will learn!** 🎓
