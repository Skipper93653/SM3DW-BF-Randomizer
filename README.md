# Super Mario 3D World (+ Bowser's Fury) Randomizer

Super Mario 3D World Randomizer is a stage randomizer for Super Mario 3D World (Switch)!<br>
Bowser's Fury and Wii U support are planned for a later time.<br>
The release executable is Windows only, to build for MacOS or Linux, see the Building section further down this README.

## Usage

### Generating the randomized files

Select a valid RomFS dump (the root of the RomFS directory - contains folders such as `StageData`, `SystemData`, etc.) of Super Mario 3D World + Bowser's Fury, enable any additional options and then hit the 'Randomize!' button and wait for the pop-up window to tell you the process has finished, this should generate a folder called `SM3DWR-seed` (with 'seed' being the seed used by the random number generator).

### Playing with the newly generated files

Note: enable with other mods at your own risk, as this mod is only designed to be compatible with the vanilla game.

### Console

With Atmosphere CFW and [SimpleModManager](https://github.com/nadrino/SimpleModManager) - on the root of your microSD card, go to `mods/Super Mario 3D World + Bowser's Fury/Randomizer/contents/010028600EBDA000` (create these folders if they don't exist) and copy the `romfs` folder from inside the newly generated `SM3DW-seed` folder to this location. Then, on console, make your way to SimpleModManager and enable the mod, then you're free to play!

### Emulators

#### yuzu

For usage with yuzu - open yuzu, right click 'Super Mario 3D World + Bowser's Fury' and click on 'Open Mod Data Location', this should open a new window within the mod folder. From there, copy the newly generated `SM3DWR-seed` folder into said mod folder (if you didn't select here as the output directory already). To check whether it is enabled, right click 'Super Mario 3D World + Bowser's Fury' and click 'Properties'. Go to the 'Add-Ons' tab and tick your mod folder if it isn't already, then you're free to play!

#### [Ryujinx](https://ryujinx.org)

For usage with Ryujinx - open Ryujinx, right click 'Super Mario 3D World + Bowser's Fury' and click on 'Open Mods Directory', this should open a new window within the mod folder. From there, copy the newly generated `SM3DWR-seed` folder into said mod folder (if you didn't select here as the output directory already). To check whether it is enabled, right click 'Super Mario 3D World + Bowser's Fury and click 'Manage Mods' and enable the mod folder if it isn't already, then you're free to play! 

## Known Issues

* Stamps do not randomize with stage so the stamp screen is not fully functional.
* The course list may crash the game.
* Some stage numbers are glitched.
* The World Warp Pipes which should take you to the next world do not work and just kick you out of the stage.
* Sometimes, with randomized music, the music may sometimes cut out abruptly.

## Potential future features in no particular order

* Wii U support
* Bowser's Fury island randomizer
* Character statistics randomizer
* Adjusting the end-of-level Goal Poles to properly represent the new location of the level e.g. Levels where a castle used to be will now have the castle Goal Pole.
* Doing something with the World Warp Pipes in Koopa Troopa Cave and Piranha Creeper Creek.

## Building

To build this software, open this project in PyCharm, and run `python -m nuitka main.py --standalone --include-data-files=ico.ico=ico.ico --windows-icon-from-ico=ico.ico` for Windows, `python -m nuitka main.py --standalone --include-data-files=ico.ico=ico.ico --macos-create-app-bundle --macos-app-icon=ico.ico` for MacOS, and `python -m nuitka main.py --standalone --include-data-files=ico.ico=ico.ico` for Linux in the built-in PowerShell terminal. The resulting output will be in a folder called `main.dist`

## Support

If you need help with the randomizer in any way, be sure to try and get in touch with me via my [Discord](https://discord.gg/NCKtWuJUcC).