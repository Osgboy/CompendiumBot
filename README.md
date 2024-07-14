# CompendiumBot
A Discord bot for the [Proxy Studios Discord](https://discord.gg/proxystudios) that acts as a substitute for the in game compendium for users who can't/don't feel like opening the game itself.

## Commands
As of now, the bot supports 10 slash commands: 5 object types (item, unit, weapon, trait, and action) for each of Proxy's 2 games, Gladius and Zephon.

## Structure
`main.py` contains all the Discord API code and is responsible for creating and formatting the message embeds.
The `json` folder contains the code used for converting the raw XML data into JSON, as well as the JSON files themselves. `xml2json.py` imports modules (`item.py`, `unit.py`, etc.) that define classes that contain the methods for extracting data and storing it in attributes. These attributes are then converted to dictionaries that get dumped into the JSON files. The `Obj` class in `obj.py` contains methods common to each object type that are inherited by all modules.
All of the raw XML data and icon PNGs can be found in the `Gladius` and `Zephon` folders. `scratch/` contains some random stuff I use for testing as well as scripts for updating the `Gladius` and `Zephon` folders that are used whenever the game updates.
