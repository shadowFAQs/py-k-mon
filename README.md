# Py-k-mon: Very much a WIP

It's **Pokémon Fire Red** but completely built from scratch in Pygame!

![pallet_town_2](https://github.com/shadowFAQs/py-k-mon/assets/36905164/543799ed-3b21-4d6d-9906-4b9741fc8df8)

### Why though?

Pokémon presents a lot of interesting data structure problems. Also Gen 1 (Blue, specifically) was a very formative game during my childhood, so there's that too. And FRLG combines the nostalgia of Gen 1 with the GBA, my favorite handheld platform.

### State of the game

So far all you can do is walk around Pallet Town! But it's a good proof-of-concept.

**Currently working:**
- Map generation, sprite sheets, tile grids & animation
- WASD controls (U = "B" button; H = "A" button; SPACE = "Start")
- Walking and running
- Grid based movement with collision detection
- Map transitions
- "Passive" map events (e.g. entering a house or a stepping on a warp tile)
- "Active" map events, like reading a sign or picking up an item
- Dialog modals

**Next up:**
- A pause/menu system
- Battle system
- Pokédex
- Tall grass encounters
- Pokéballs and capturing wild Pokémon
- A map editor
- NPCs

### Notes

Py-k-mon was built and tested with Pygame 2.5.1, Python 3.10, and Ubuntu 22.04.3. Thanks to [Spriters Resource](https://www.spriters-resource.com/game_boy_advance/pokemonfireredleafgreen/) for the images!

Requires [pygame](https://pypi.org/project/pygame/) and [numpy](https://pypi.org/project/numpy/).