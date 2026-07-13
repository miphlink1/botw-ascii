# The Legend of Zelda: Breath of the Wild in ASCII

An attempt to recreate BotW's Great Plateau as a 2.5D, top-down ASCII renderer in Python

## Status
**Work in Progress (WIP) Phase 2**
```
╔╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╤╗
╟┼┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┼╢
╟┤---db---d8b---db------d888888b------d8888b.---├╢
╟┤---88---I8I---88--------`88'--------88--`8D---├╢
╟┤---88---I8I---88---------88---------88oodD'---├╢
╟┤---Y8---I8I---88---------88---------88~~~-----├╢
╟┤---`8b-d8'8b-d8'--------.88.--------88--------├╢
╟┤----`8b8'-`8d8'-------Y888888P------88--------├╢
╟┼┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┼╢
╚╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╧╝
```
## Overview
I'm finally making the project I always wanted to do in Python!!!
I've wanted to do since I realised input() existed and so I thought, 'okay Zelda time.'

The Legend of Zelda, Breath of the Wild in ASCII will include:

- a 2.5D 176x300 custom surface map of the Great Plateau (uhoh)
- accurate-ish text art physics???!
- 9 enemy types with accurate-ish AI!
- Master Mode and DLC chests!!!
- 4 shrines and abilities!
- Eight 100% accurate preloaded cutscenes!
- Accurate ASCII UI/inventory and attack/enemy animations!

All on any potatoe Python terminal, even those online ones!

Note: All world design, map layout, characters, names and specific creative content is owned by Nintendo Co., Ltd. I hope I'm not breaking any laws but honestly it won't be amazing, it will look completely different, and obviously it can't be monetized and will get no audience.


## Pipeline status
[X] **Phase 1 — datamining**: raw extraction from Minecraft world (raw_scan, symbol map, air detection, underhangs, openings). Complete. Should no longer need the Minecraft world reloaded for normal work.

[:] **Phase 2 — data polishing**: normalization, translation key, symbol remap, opening→entrance grouping. Mostly done — only trees still in progress.

[ ] **Phase 3 — rendering**: rendering the world. includes map data, underhangs, custom overlays, and entities. yay i finally get to touch an if statement

[ ] **Phase 4 — the player**: Player class, HP, stamina, climbing. inventory and attack animation and hitbox. abilities, bow+shield.

[ ] **Phase 5 — other entities**: Enemy behavior, NPCs, wild animals, fish.

[ ] **Phase 6 — shrines and interiors**: redoing Phase 1 for scraping base data from shrines and then hand-authoring details, fixing interior of Shrine of Resurrection, Old Man's Cabin and Temple of Time.

[ ] **Phase 7 — gameplay and content**: preloading cutscenes and adding dialogue, progression and unlocks. UI/HUD, settings, main menu, world+save states.

## Contributing

Unless you're @Katsugachi or myself, please, just don't. 

## Resources
https://grazzy.sae.sh is Grazzy's MC world which I stole map data from.
https://github.com/MrCheeze/botw-tools/blob/master/heightmap.py is some random heightmap data I used early on.


