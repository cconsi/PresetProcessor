# Arma 3 Mod Preset Command Line Generator

A small script and windows .exe that makes setting custom command line presets easier by utilizing the Arma 3 Launcher's mod preset HTMLs. The idea was to make it easy to generate server presets for various modlists.

## Installation

Download the [distribution for Windows](https://github.com/cconsi/PresetProcessor/releases/download/v1.0/preset_processor.zip) and extract the compressed files. Run `preset_processor.exe` in the extracted folder.

...or clone the repository and run `pip install -r requirements.txt` and `python preset_processor.py` to start the script with your Python 3 installation.

## Instructions

1. Using the Arma 3 Launcher export and save a mod preset to a file.
2. Double-click on `process_preset.exe`.
3. Enter your server's information in the fields.
4. Click "Process" and your command line arguments will be written to a text file.
5. You now have a command line string for startup use on an Arma 3 game server that will load your mod preset.

##### All mods must already be installed on your server.
##### Default command line arguments are geared for ServerBlend hosted game servers, but should apply to all Arma 3 game servers. Check your server's specs.
