![GitHub release (latest by date)](https://img.shields.io/github/v/release/Skipper93653/SuperMario3DWorld-Randomizer)

# Super Mario 3D World (+ Bowser's Fury) Randomizer

Super Mario 3D World Randomizer is a stage randomizer for Super Mario 3D World (Switch)!<br>
Bowser's Fury and Wii U support are planned for a later time.

## Usage

### Generating the randomized files

Select a valid RomFS dump of Super Mario 3D World + Bowser's Fury, enable any additional options and then hit the 'Randomize' button, your file should be outputted in the same directory in a folder called ```romfs-datetime``` (with 'datetime' being the date and time you initiated the randomizing process).

### Playing with the newly generated files

### Console

If you have Atmosphere CFW - on the root of your SD card, create a folder within the ```atmosphere\contents``` folder named ```010028600EBDA000``` (The ID for Super Mario 3D World + Bowser's Fury) and copy your ```romfs-datetime``` folder into it and rename it to just 'romfs' then you're free to play!

### Emulators

#### [yuzu](https://yuzu-emu.org)

For usage with yuzu - open yuzu, right click 'Super Mario 3D World + Bowser's Fury' and click on 'Open Mod Data Location', this should open a new window within the mod folder. From there, create a new folder with a name of your choice and copy the newly generated ```romfs-datetime``` into your newly created mod folder and rename it to just 'romfs'. To check whether it is enabled in yuzu, right click 'Super Mario 3D World + Bowser's Fury' and click 'Properties'. Go to the 'Add-Ons' tab and tick your mod folder if it isn't already. Disable other mods that may cause confliction with the randomizer and then you're free to play!

#### [Ryujinx](https://ryujinx.org)

For usage with Ryujinx - open Ryujinx, right click 'Super Mario 3D World + Bowser's Fury' and click on 'Open Mods Directory', this should open a new window within the mod folder. From there, create a new folder with a name of your choice and copy the newly generated ```romfs-datetime``` into your newly created mod folder and rename it to just 'romfs' then you're free to play!

## Potential future features

* Music randomizer
* Bowser's Fury island randomizer
* Seed input
* Wii U support

## Building

To build this software, run ```setup.py``` which requires to have the [PyInstaller](https://github.com/pyinstaller/pyinstaller) module installed along with the [oead](https://github.com/zeldamods/oead) module which is used for working with Nintendo file formats.<br>
```pip install pyinstaller```<br>
```pip install oead```<br>
This builds a Windows Executable in ```dist```.

## Support

If you need help with the randomizer in anyway, be sure to try and get in touch with me via my [Discord](https://discord.gg/NCKtWuJUcC).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.