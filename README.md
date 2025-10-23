# quakeless ii

can i get... uhhh quake ii, but ummmm, hold the quake?

what if quake ii but it doesn't need the pak0.pak, but what if the game dll was written in odin? and also what if it had no features and no expectations of support for anything from the base game?

welcome to quakeless ii

state:

- quake ii pak0 required _partially_ at the moment, there are still a few files (like main menu graphics, conchars.pcx) that are copied over
  - the goal is to one day remove this requirement and have everything for the game to boot just in the repo
- no sounds / models, just _some_ custom images for the map / _some_ main menu elements
- odin code has a working player that can move around and _not_ crash... but that's about it, not even disconnect logic currently

goals:

- blank canvas for a prospective quake engineer
- copyright free base that boots Yamagi Quake II with a modified game dll, that throws little to no errors about missing files
- game dll written in odin
- player, in a box, running around
- dedicated server works
- work well on linux/macos/windows
- target opengl 3.2 renderer for visual consistency, and support (thanks macos)
- possible to create something epic with this as its base
- just because its an old engine, it should not feel old / low quality
- easy to run build script that works multiplatform, shell would be fine if not for windows, python is a perfectly fine choice

non goals:

- work well on old computers
- graphics anything more complex than default dev textures
- telling you how to structure your game, just giving you a starting point on how to produce a game dll that _works_, with the basics you expect (physics, networking, etc.)

---

`game-c` is based off of [yquake2/ctf](https://github.com/yquake2/ctf/tree/c7a4b27bf67c9b09fe906bfb2263ff9f66fb57b6)

it was used as a test to see _how much_ you can rip away from the game until it stops compiling / working.

its (mostly) surved its purpose, but it was _very_ useful for getting the odin code started!

---

while this minimal base isn't supposed to contain much graphics / vibes, I still want some level of art direction for _some_ vibes.

color scheme: https://lospec.com/palette-list/endesga-32

- backdrop: #181425
- menu backdrop: #3a4466

font: https://fonts.google.com/specimen/DynaPuff
