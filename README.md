![GitHub release (latest by date)](https://img.shields.io/github/v/release/Skipper93653/SM3DW-BF-Randomizer)

# Super Mario 3D World (+ Bowser's Fury) Randomizer

Super Mario 3D World Randomizer is a stage randomizer for Super Mario 3D World (Switch)!<br>
Bowser's Fury and Wii U support are planned for a later time.

## Usage

### Generating the randomized files

Select a valid RomFS dump (the root of the RomFS directory - contains folders such as SoundData, StageData, etc.) of Super Mario 3D World + Bowser's Fury, enable any additional options and then hit the 'Randomize' button and wait for the pop-up window to tell you the process has finished, this should generate a folder called ```SM3DWR-seed``` (with 'seed' being the seed used by the random number generator). All green star locks are removed except from the levels with star locks from Bowser-Castle onwards and all collectables and gold goal poles for World Crown.

### Playing with the newly generated files

### Console (UNSUPPORTED)

If you have Atmosphere CFW - on the root of your SD card, create a folder within the ```atmosphere\contents``` (or ```atmosphere\titles``` on Atmosphere CFW versions 0.9.4 and below) folder named ```010028600EBDA000``` (The ID for Super Mario 3D World + Bowser's Fury) and copy your ```romfs``` folder (from inside the generated ```SM3DWR-seed``` folder) into it and rename it to just 'romfs' then you're free to play!

### Emulators

#### yuzu

For usage with yuzu - open yuzu, right click 'Super Mario 3D World + Bowser's Fury' and click on 'Open Mod Data Location', this should open a new window within the mod folder. From there, copy the newly generated ```SM3DWR-seed``` folder into said mod folder. To check whether it is enabled in yuzu, right click 'Super Mario 3D World + Bowser's Fury' and click 'Properties'. Go to the 'Add-Ons' tab and tick your mod folder if it isn't already. Disable other mods that may cause confliction with the randomizer, then you're free to play!

#### [Ryujinx](https://ryujinx.org) (UNSUPPORTED)

For usage with Ryujinx - open Ryujinx, right click 'Super Mario 3D World + Bowser's Fury' and click on 'Open Mods Directory', this should open a new window within the mod folder. From there, copy the newly generated ```SM3DWR-seed``` folder into said mod folder, then you're free to play!

## Known Issues

* Stamps do not randomize with stage so the stamp screen is not fully functional.
* Sometimes the course list screen freezes the game.
* Some stage numbers are glitched.
* Warp Pipes which should take you to the next world do not work and just kick you out of the stage.
* Sometimes, with randomized music, the music may sometimes cut out abruptly.

## Potential future features in no particular order

* Console support
* Ryujinx support
* Bowser's Fury island randomizer
* Wii U support
* Character statistics randomizer

## Building

To build this software, run ```setup.py``` which requires to have the [PyInstaller](https://github.com/pyinstaller/pyinstaller) module installed along with the [oead](https://github.com/zeldamods/oead) module which is used for working with Nintendo file formats.<br>
```pip install pyinstaller```<br>
```pip install oead```<br>
This builds an executable based on the operating system you used to compile the program (Windows, Mac OS X, and GNU/Linux) in ```dist```.

## Support

If you need help with the randomizer in any way, be sure to try and get in touch with me via my [Discord](https://discord.gg/NCKtWuJUcC).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.