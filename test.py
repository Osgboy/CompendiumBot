#!~/.venv/Scripts/python.exe
import discord
import os
import json
import embed
import objList
from thefuzz import fuzz
from typing import Callable
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

DLCS = {
    'None': 'None',
    'Supplement1': 'Reinforcement Pack',
    'Supplement2': 'Tyranids',
    'Supplement3': 'Chaos Space Marines',
    'Supplement4': 'Fortification Pack',
    'Supplement5': 'Tau',
    'Supplement6': 'Assault Pack',
    'Supplement7': 'Eldar',
    'Supplement8': 'Specialist Pack',
    'Supplement9': 'Adeptus Mechanicus',
    'Supplement10': 'Escalation Pack',
    'Supplement11': 'Adepta Sororitas',
    'Supplement12': 'Firepower Pack',
    'Supplement13': 'Drukhari',
    'Supplement14': 'Demolition Pack',
    'LordOfSkulls': 'Lord of Skulls'
}
GLADIUS_FACTIONS = {
    'Neutral': 'Neutral',
    'Adeptus Mechanicus': 'Adeptus Mechanicus',
    'Astra Militarum': 'Astra Militarum',
    'Chaos Space Marines': 'Chaos Space Marines',
    'Drukhari': 'Drukhari',
    'Eldar': 'Craftworld Aeldari',
    'Necrons': 'Necrons',
    'Orks': 'Orks',
    'Sisters Of Battle': 'Adepta Sororitas',
    'Space Marines': 'Space Marines',
    'Tau': "T'au",
    'Tyranids': 'Tyranids',
}
ZEPHON_FACTIONS = (
    'Anchorite',
    'Chieftess',
    'Emulated Mind',
    'Fallen Soldier',
    'Furtive Tribunal',
    'Heartless Artificer',
    'Honorable Aristocrat',
    'Neutral',
    'Practical Romantic',
    'Rogue Operative',
    'Untold Prophet',
    'Zephon',
)
ZEPHON_BRANCHES = (
    'Cyber',
    'Human',
    'Voice',
    'Zephon',
    'Reaver',
    'Acrin',
    'Neutral',
)
GLADIUS_RARITIES = (
    'Common',
    'Uncommon',
    'Artefact',
)
ZEPHON_RARITIES = (
    'Common',
    'Uncommon',
    'Rare',
)
ACTION_COOLDOWNS = (
    'Passive',
    '0',
    '1',
    '2',
    '3',
    '5',
    '10',
)
ACTION_CONDITIONS = {
    #'requiredUpgrade',
    'Requires action points': 'requiredActionPoints',
    'Requires movement': 'requiredMovement',
    'Usable in transport': 'usableInTransport',
    'Consumes action points': 'consumedActionPoints',
    'Consumes movement': 'consumedMovement',
}

load_dotenv()
TOKEN = os.getenv("TEST_TOKEN")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
dicts: dict[str, dict[str, dict]] = {}  # dict[objClass, dict[obj, objAttrs]]


class NotFoundError(Exception):
    def __init__(self, keyword: str, userInput: str, bestMatch: str):
        self.keyword = keyword
        self.userInput = userInput
        self.bestMatch = bestMatch


def fuzzy_match(keyword: str, name: str, classDict: dict) -> tuple[str, dict]:
    """Fuzzy match a given search term and raise an error if term isn't found.

    Args:
        keyword (str): Passed to the raised exception to know which argument to replace with its best match
        name (str): The search term
        classDict (dict): Dict of names:attributes whose keys are fuzzy matched against the search term

    Returns:
        objName (str): The dict key that was found to match the search term
        objAttrs (dict): Dict of attributes belonging to the key object
    """
    name = name.casefold()
    bestRatio = 0
    bestMatch = ''
    for key, val in classDict.items():
        compareStr = key.casefold()
        if compareStr == name:
            return key, val
        else:
            fuzzRatio = fuzz.token_sort_ratio(compareStr, name)
            for word in name.split():
                if word in compareStr:
                    fuzzRatio += 100
            if fuzzRatio > bestRatio:
                bestRatio = fuzzRatio
                bestMatch = key
    else:
        raise NotFoundError(keyword, name, bestMatch)


class ConfirmFuzzyMatch(discord.ui.View):
    def __init__(self, matchFunc: Callable[[], tuple[discord.Embed, str]], *args, **kwargs):
        super().__init__()
        self.matchFunc = matchFunc
        self.args = args
        self.kwargs = kwargs

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed, fullIconPath = self.matchFunc(
                *self.args, **self.kwargs)
        except NotFoundError as nf:
            await interaction.response.edit_message(content=f'**{nf.userInput}** not found. Did you mean **{nf.bestMatch}**?')
            self.kwargs[nf.keyword] = nf.bestMatch
            print(repr(nf))
        else:
            if fullIconPath is None:
                await interaction.response.edit_message(content=None, embed=embed, view=None)
                print('Successfully returned request without icon after editing.')
                return
            try:
                image = discord.File(fullIconPath, filename='icon.png')
                embed.set_thumbnail(url="attachment://icon.png")
                await interaction.response.edit_message(content=None, embed=embed, attachments=[image], view=None)
                print('Successfully returned request after editing.')
            except FileNotFoundError:
                await interaction.response.edit_message(content=None, embed=embed, view=None)
                print(
                    f'Icon {fullIconPath!r} was not found. Sending embed without icon')

    @discord.ui.button(label='No', style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()

def match_and_create_embed(verbose: bool, flavor: bool, objClass: str, embedFunc: Callable[[str, dict, bool, str], discord.Embed], unitClass: str,
                           *, name: str, unitName: str) -> tuple[discord.Embed, str]:
    if unitName:
        unitArgs = [*fuzzy_match('unitName', unitName, dicts[unitClass])]
    else:
        unitArgs = []
    objName, objDict = fuzzy_match('name', name, dicts[objClass])
    embed = embedFunc(objName, objDict, verbose, flavor, *unitArgs)
    fullIconPath = objDict['iconPath']
    return embed, fullIconPath


async def return_info(interaction: discord.Interaction, name: str, verbose: bool, flavor: bool, invisible: bool, objClass: str,
                      embedFunc: Callable[[dict, bool, str], discord.Embed], unitName: str = '', unitClass: str = ''):
    print(f'\nReceived request for:\n'
          f'- Class: {objClass}\n'
          f'- Name: {name}\n'
          f'- Unit Name: {unitName}\n')
    kwargs = {'name': name, 'unitName': unitName}
    try:
        embed, fullIconPath = match_and_create_embed(
            verbose, flavor, objClass, embedFunc, unitClass, **kwargs)
    except NotFoundError as nf:
        kwargs[nf.keyword] = nf.bestMatch
        await interaction.response.send_message(f'**{nf.userInput}** not found. Did you mean **{nf.bestMatch}**?', ephemeral=invisible,
                                                view=ConfirmFuzzyMatch(match_and_create_embed, verbose, flavor, objClass, embedFunc, unitClass, **kwargs))
        print(repr(nf))
    else:
        try:
            image = discord.File(fullIconPath, filename='icon.png')
            embed.set_thumbnail(url="attachment://icon.png")
            await interaction.response.send_message(embed=embed, file=image, ephemeral=invisible)
            print('Successfully returned request.')
        except FileNotFoundError:
            await interaction.response.send_message(embed=embed, ephemeral=invisible)
            print('Successfully returned request without icon.')


def match_and_create_list(objClass: str, embedFunc: Callable[[dict, any], discord.Embed],
                          **filters) -> tuple[discord.Embed, str]:
    kwargs = {}
    for filterClass, filterName in filters.items():
        if not filterName:
            continue
        if filterClass not in dicts.keys():
            kwargs[filterClass] = filterName
            continue
        name, _ = fuzzy_match(filterClass, filterName, dicts[filterClass])
        kwargs[filterClass] = name
    return embedFunc(dicts[objClass], **kwargs), None


async def return_list(interaction: discord.Interaction, invisible: bool, objClass: str,
                      embedFunc: Callable[[dict, bool, str], discord.Embed], **filters):
    print(f'\nReceived request to list:\n'
          f'- Class: {objClass}\n')
    try:
        embed, _ = match_and_create_list(objClass, embedFunc, **filters)
    except NotFoundError as nf:
        filters[nf.keyword] = nf.bestMatch
        await interaction.response.send_message(f'**{nf.userInput}** not found. Did you mean **{nf.bestMatch}**?', ephemeral=invisible,
                                                view=ConfirmFuzzyMatch(match_and_create_list, objClass, embedFunc, **filters))
        print(repr(nf))
    else:
        if len(embed) <= 6000:
            await interaction.response.send_message(embed=embed, ephemeral=invisible)
            print('Successfully returned request without icon.')
        else:
            await interaction.response.send_message('Embed size exceeds 6000 characters! Please limit your query and try again.', ephemeral=invisible)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("\nRunning on the following guilds:")
    for guild in bot.guilds:
        print('\t' + guild.name)

    listGroup = app_commands.Group(
        name='list', description='List names of objects of a certain type with optional filters.')
    listGladius = GladiusList(
        name='gladius', description='List names of Gladius objects of a certain type with optional filters.', parent=listGroup)
    listZephon = ZephonList(
        name='zephon', description='List names of Zephon objects of a certain type with optional filters.', parent=listGroup)
    bot.tree.add_command(listGroup)

    await bot.load_extension('cogs.roles')

    synced = await bot.tree.sync()
    print(f"\n# CMDs synced: {len(synced)}")

    JSON_DIR = os.path.join('json')
    for objClass in ('GAction', 'ZAction', 'GBuilding', 'ZBuilding', 'GFaction', 'ZFaction', 'GItem', 'ZItem', 'GUnit', 'ZUnit', 'GUpgrade', 'ZUpgrade', 'GTrait', 'ZTrait', 'GWeapon', 'ZWeapon'):
        with open(os.path.join(JSON_DIR, objClass + '.json'), 'r') as file:
            dicts[objClass] = json.load(file)
    print(f"\n# JSONs loaded: {len(dicts)}")


def docstring_defaults(func):
    doc = func.__doc__ or ''
    doc += "\tverbose (bool): Flag to include raw XML, flavor text, and footer text if applicable (default is False)" + \
        "\n\tflavor (bool): Flag to include only flavor text (default is False)" + \
        "\n\tinvisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)"
    func.__doc__ = doc
    return func


class GladiusList(app_commands.Group):
    @app_commands.command()
    @app_commands.choices(faction=[app_commands.Choice(name=f, value=f) for f in GLADIUS_FACTIONS])
    @app_commands.choices(cooldown=[app_commands.Choice(name=c, value=c) for c in ACTION_COOLDOWNS])
    @app_commands.choices(condition=[app_commands.Choice(name=k, value=v) for k, v in ACTION_CONDITIONS.items()])
    async def action(self, interaction: discord.Interaction, faction: app_commands.Choice[str] = '', cooldown: app_commands.Choice[str] = '',
                     condition: app_commands.Choice[str] = '', requiredupgrade: str = '', invisible: bool = False):
        """List Gladius actions according to given filters.

        Args:
            faction (str): Filter by faction
            cooldown (str): Filter by cooldown
            condition (str): Filter by condition
            requiredupgrade (str): Filter by required upgrade
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        # Add faction
        if faction:
            faction = faction.value
        if cooldown:
            cooldown = cooldown.value
        if condition:
            condition = condition.value
        await return_list(interaction, invisible, 'GAction', objList.create_gaction_list, faction=faction, cooldown=cooldown,
                          condition=condition, GUpgrade=requiredupgrade)

    @app_commands.command()
    @app_commands.choices(faction=[app_commands.Choice(name=f, value=f) for f in GLADIUS_FACTIONS])
    async def building(self, interaction: discord.Interaction, faction: app_commands.Choice[str] = '',
                       traitname: str = '', invisible: bool = False):
        """List Gladius buildings according to given filters.

        Args:
            faction (str): Filter by faction
            trait (str): Filter by trait
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        if faction:
            faction = faction.value
        await return_list(interaction, invisible, 'GBuilding', objList.create_gbuilding_list, faction=faction, GTrait=traitname)

    @app_commands.command()
    @app_commands.choices(rarity=[app_commands.Choice(name=r, value=r) for r in GLADIUS_RARITIES])
    async def item(self, interaction: discord.Interaction, rarity: app_commands.Choice[str] = '', invisible: bool = False):
        """List Gladius items according to given filters.

        Args:
            rarity (str): Filter by rarity
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        if rarity:
            rarity = rarity.value
        await return_list(interaction, invisible, 'GItem', objList.create_gitem_list, rarity=rarity)

    @app_commands.command()
    @app_commands.choices(faction=[app_commands.Choice(name=f, value=f) for f in GLADIUS_FACTIONS])
    async def trait(self, interaction: discord.Interaction, faction: app_commands.Choice[str] = '', invisible: bool = False):
        """List Gladius traits according to given filters.

        Args:
            faction (str): Filter by faction
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        # faction
        if faction:
            faction = faction.value
        await return_list(interaction, invisible, 'GTrait', objList.create_gtrait_list, faction=faction)

    @app_commands.command()
    @app_commands.choices(faction=[app_commands.Choice(name=f, value=f) for f in GLADIUS_FACTIONS])
    @app_commands.choices(dlc=[app_commands.Choice(name=v, value=k) for k, v in DLCS.items()])
    async def unit(self, interaction: discord.Interaction, faction: app_commands.Choice[str] = '', dlc: app_commands.Choice[str] = '',
                   weaponname: str = '', traitname: str = '', actionname: str = '', invisible: bool = False):
        """List Gladius units according to given filters.

        Args:
            faction (str): Filter by faction
            dlc (str): Filter by DLC
            weaponname (str): Filter by weapon
            traitname (str): Filter by trait
            actionname (str): Filter by action
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        # faction, combatStats, resourceStats, DLC, weapon, trait, action
        if faction:
            faction = faction.value
        if dlc:
            dlc = dlc.value
        await return_list(interaction, invisible, 'GUnit', objList.create_gunit_list, faction=faction, dlc=dlc, GWeapon=weaponname, GTrait=traitname, GAction=actionname)

    @app_commands.command()
    @app_commands.choices(faction=[app_commands.Choice(name=f, value=f) for f in GLADIUS_FACTIONS])
    @app_commands.choices(dlc=[app_commands.Choice(name=v, value=k) for k, v in DLCS.items()])
    @app_commands.choices(tier=[app_commands.Choice(name=t, value=t) for t in ['Not Researchable'] + [str(i) for i in range(1, 11)]])
    async def upgrade(self, interaction: discord.Interaction, faction: app_commands.Choice[str] = '', dlc: app_commands.Choice[str] = '',
                      tier: app_commands.Choice[str] = '', requiredupgrade: str = '', invisible: bool = False):
        """List Gladius upgrades according to given filters.

        Args:
            faction (str): Filter by faction
            dlc (str): Filter by DLC
            tier (str): Filter by tier
            requiredupgrade (str): Filter by prerequisite research
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        # faction, tier, required upgrade, unlocks
        if faction:
            faction = faction.value
        if dlc:
            dlc = dlc.value
        if tier:
            tier = tier.value
        await return_list(interaction, invisible, 'GUpgrade', objList.create_gupgrade_list, faction=faction, dlc=dlc, tier=tier, GUpgrade=requiredupgrade)

    @app_commands.command()
    @app_commands.choices(faction=[app_commands.Choice(name=f, value=f) for f in GLADIUS_FACTIONS])
    async def weapon(self, interaction: discord.Interaction, faction: app_commands.Choice[str] = '',
                     traitname: str = '', range: str = '', invisible: bool = False):
        """List Gladius weapons according to given filters.

        Args:
            faction (str): Filter by faction
            trait (str): Filter by trait
            range (str): Filter by weapon range. Use 'melee' for melee range.
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        if faction:
            faction = faction.value
        if range == 'melee':
            range = 'Melee'
        await return_list(interaction, invisible, 'GWeapon', objList.create_gweapon_list, faction=faction, GTrait=traitname, range=range)


class ZephonList(app_commands.Group):
    @app_commands.command()
    @app_commands.choices(branch=[app_commands.Choice(name=b, value=b) for b in ZEPHON_BRANCHES])
    @app_commands.choices(cooldown=[app_commands.Choice(name=c, value=c) for c in ACTION_COOLDOWNS])
    @app_commands.choices(condition=[app_commands.Choice(name=k, value=v) for k, v in ACTION_CONDITIONS.items()])
    async def action(self, interaction: discord.Interaction, branch: app_commands.Choice[str] = '', cooldown: app_commands.Choice[str] = '',
                     condition: app_commands.Choice[str] = '', requiredupgrade: str = '', invisible: bool = False):
        """List Zephon actions according to given filters.

        Args:
            branch (str): Filter by branch
            cooldown (str): Filter by cooldown
            condition (str): Filter by condition
            requiredupgrade (str): Filter by required upgrade
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        # Add faction
        if branch:
            branch = branch.value
        if cooldown:
            cooldown = cooldown.value
        if condition:
            condition = condition.value
        await return_list(interaction, invisible, 'ZAction', objList.create_zaction_list, branch=branch,
                          cooldown=cooldown, condition=condition, ZUpgrade=requiredupgrade)

    @app_commands.command()
    @app_commands.choices(branch=[app_commands.Choice(name=b, value=b) for b in ZEPHON_BRANCHES])
    async def building(self, interaction: discord.Interaction, branch: app_commands.Choice[str] = '',
                       traitname: str = '', invisible: bool = False):
        """List Zephon buildings according to given filters.

        Args:
            branch (str): Filter by branch
            trait (str): Filter by trait
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        if branch:
            branch = branch.value
        await return_list(interaction, invisible, 'ZBuilding', objList.create_zbuilding_list, branch=branch, ZTrait=traitname)


    @app_commands.command()
    @app_commands.choices(branch=[app_commands.Choice(name=b, value=b) for b in ZEPHON_BRANCHES])
    @app_commands.choices(rarity=[app_commands.Choice(name=r, value=r) for r in ZEPHON_RARITIES])
    async def item(self, interaction: discord.Interaction, branch: app_commands.Choice[str] = '', rarity: app_commands.Choice[str] = '',
                   buycondition: str = '', invisible: bool = False):
        """List Zephon items according to given filters.

        Args:
            branch (str): Filter by branch
            rarity (str): Filter by rarity
            buycondition (str): Filter by prerequisite research
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        if branch:
            branch = branch.value
        if rarity:
            rarity = rarity.value
        await return_list(interaction, invisible, 'ZItem', objList.create_zitem_list, branch=branch, rarity=rarity, ZTrait=buycondition)

    @app_commands.command()
    @app_commands.choices(branch=[app_commands.Choice(name=b, value=b) for b in ZEPHON_BRANCHES])
    async def trait(self, interaction: discord.Interaction, branch: app_commands.Choice[str] = '', invisible: bool = False):
        """List Zephon traits according to given filters.

        Args:
            branch (str): Filter by branch
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        # branch
        if branch:
            branch = branch.value
        await return_list(interaction, invisible, 'ZTrait', objList.create_ztrait_list, branch=branch)
    
    @app_commands.command()
    @app_commands.choices(branch=[app_commands.Choice(name=b, value=b) for b in ZEPHON_BRANCHES])
    async def unit(self, interaction: discord.Interaction, branch: app_commands.Choice[str] = '',
                   weaponname: str = '', traitname: str = '', actionname: str = '', invisible: bool = False):
        """List Zephon units according to given filters.

        Args:
            branch (str): Filter by branch
            weaponname (str): Filter by weapon
            traitname (str): Filter by trait
            actionname (str): Filter by action
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        # branch, combatStats, resourceStats, weapon, trait, action
        if branch:
            branch = branch.value
        await return_list(interaction, invisible, 'ZUnit', objList.create_zunit_list, branch=branch, ZWeapon=weaponname, ZTrait=traitname, ZAction=actionname)

    @app_commands.command()
    @app_commands.choices(branch=[app_commands.Choice(name=b, value=b) for b in ZEPHON_BRANCHES])
    @app_commands.choices(faction=[app_commands.Choice(name=f, value=f) for f in ZEPHON_FACTIONS])
    @app_commands.choices(tier=[app_commands.Choice(name=t, value=t) for t in ['Not Researchable'] + [str(i) for i in range(11)]])
    async def upgrade(self, interaction: discord.Interaction, branch: app_commands.Choice[str] = '', faction: app_commands.Choice[str] = '',
                      tier: app_commands.Choice[str] = '', requiredupgrade: str = '', invisible: bool = False):
        """List Zephon upgrades according to given filters.

        Args:
            branch (str): Filter by branch
            faction (str): Filter by faction
            tier (str): Filter by tier
            requiredupgrade (str): Filter by prerequisite research
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        # faction, tier, required upgrade, unlocks
        if branch:
            branch = branch.value
        if faction:
            faction = faction.value
        if tier:
            tier = tier.value
        await return_list(interaction, invisible, 'ZUpgrade', objList.create_zupgrade_list, branch=branch, faction=faction, tier=tier, ZUpgrade=requiredupgrade)

    @app_commands.command()
    @app_commands.choices(branch=[app_commands.Choice(name=b, value=b) for b in ZEPHON_BRANCHES])
    async def weapon(self, interaction: discord.Interaction, branch: app_commands.Choice[str] = '', traitname: str = '', range: str = '', invisible: bool = False):
        """List Zephon weapons according to given filters.

        Args:
            branch (str): Filter by branch
            trait (str): Filter by trait
            range (str): Filter by weapon range. Use 'melee' for melee range.
            invisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)
        """
        if branch:
            branch = branch.value
        if range == 'melee':
            range = 'Melee'
        await return_list(interaction, invisible, 'ZWeapon', objList.create_zweapon_list, branch=branch, ZTrait=traitname, range=range)


@bot.tree.command()
@docstring_defaults
async def gaction(interaction: discord.Interaction, actionname: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Gladius action.

    Args:
        actionname (str): Name of action to look up
    """
    await return_info(interaction, actionname, verbose, flavor, invisible, 'GAction', embed.create_gaction_embed)


@bot.tree.command()
@docstring_defaults
async def zaction(interaction: discord.Interaction, actionname: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Zephon action.

    Args:
        actionname (str): Name of action to look up
    """
    await return_info(interaction, actionname, verbose, flavor, invisible, 'ZAction', embed.create_zaction_embed)


@bot.tree.command()
@docstring_defaults
async def gbuilding(interaction: discord.Interaction, buildingname: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Gladius building.

    Args:
        buildingname (str): Name of building to look up
    """
    await return_info(interaction, buildingname, verbose, flavor, invisible, 'GBuilding', embed.create_gbuilding_embed)


@bot.tree.command()
@docstring_defaults
async def zbuilding(interaction: discord.Interaction, buildingname: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Zephon building.

    Args:
        buildingname (str): Name of building to look up
    """
    await return_info(interaction, buildingname, verbose, flavor, invisible, 'ZBuilding', embed.create_zbuilding_embed)


@bot.tree.command()
@app_commands.choices(factionname=[app_commands.Choice(name=k, value=v) for k,v in GLADIUS_FACTIONS.items()])
@docstring_defaults
async def gfaction(interaction: discord.Interaction, factionname: app_commands.Choice[str] = '', verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Gladius faction.

    Args:
        factionname (str): Name of faction to look up
    """
    await return_info(interaction, factionname.value, verbose, flavor, invisible, 'GFaction', embed.create_gfaction_embed)


@bot.tree.command()
@app_commands.choices(factionname=[app_commands.Choice(name=f, value=f) for f in ZEPHON_FACTIONS])
@docstring_defaults
async def zfaction(interaction: discord.Interaction, factionname: app_commands.Choice[str] = '', verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Zephon faction.

    Args:
        factionname (str): Name of faction to look up
    """
    await return_info(interaction, factionname.value, verbose, flavor, invisible, 'ZFaction', embed.create_zfaction_embed)


@bot.tree.command()
@docstring_defaults
async def gitem(interaction: discord.Interaction, itemname: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Gladius item.

    Args:
        itemname (str): Name of item to look up
    """
    await return_info(interaction, itemname, verbose, flavor, invisible, 'GItem', embed.create_gitem_embed)


@bot.tree.command()
@docstring_defaults
async def zitem(interaction: discord.Interaction, itemname: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Zephon item.

    Args:
        itemname (str): Name of item to look up
    """
    await return_info(interaction, itemname, verbose, flavor, invisible, 'ZItem', embed.create_zitem_embed)


@bot.tree.command()
@docstring_defaults
async def gtrait(interaction: discord.Interaction, traitname: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Gladius trait.

    Args:
        traitname (str): Name of trait to look up
    """
    await return_info(interaction, traitname, verbose, flavor, invisible, 'GTrait', embed.create_gtrait_embed)


@bot.tree.command()
@docstring_defaults
async def ztrait(interaction: discord.Interaction, traitname: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Zephon trait.

    Args:
        traitname (str): Name of trait to look up
    """
    await return_info(interaction, traitname, verbose, flavor, invisible, 'ZTrait', embed.create_ztrait_embed)


@bot.tree.command()
@docstring_defaults
async def gunit(interaction: discord.Interaction, unitname: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Gladius unit.

    Args:
        unitname (str): Name of unit to look up
    """
    await return_info(interaction, unitname, verbose, flavor, invisible, 'GUnit', embed.create_gunit_embed)


@bot.tree.command()
@docstring_defaults
async def zunit(interaction: discord.Interaction, unitname: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Zephon unit.

    Args:
        unitname (str): Name of unit to look up
    """
    await return_info(interaction, unitname, verbose, flavor, invisible, 'ZUnit', embed.create_zunit_embed)


@bot.tree.command()
@docstring_defaults
async def gupgrade(interaction: discord.Interaction, upgradename: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Gladius upgrade.

    Args:
        upgradename (str): Name of upgrade to look up
    """
    await return_info(interaction, upgradename, verbose, flavor, invisible, 'GUpgrade', embed.create_gupgrade_embed)


@bot.tree.command()
@docstring_defaults
async def zupgrade(interaction: discord.Interaction, upgradename: str, verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Broken for most entries until I figure out how to add all Zephon upgrades. Return info on a Zephon upgrade.

    Args:
        upgradename (str): Name of upgrade to look up
    """
    await return_info(interaction, upgradename, verbose, flavor, invisible, 'ZUpgrade', embed.create_zupgrade_embed)


@bot.tree.command()
@docstring_defaults
async def gweapon(interaction: discord.Interaction, weaponname: str, unitname: str = '', verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Gladius weapon. Optionally include a unit name for more accurate info.

    Args:
        weaponname (str): Name of weapon to look up
        unitname (str): Name of unit wielding the weapon
    """
    await return_info(interaction, weaponname, verbose, flavor, invisible, 'GWeapon', embed.create_gweapon_embed, unitname, 'GUnit')


@bot.tree.command()
@docstring_defaults
async def zweapon(interaction: discord.Interaction, weaponname: str, unitname: str = '', verbose: bool = False, flavor: bool = False, invisible: bool = False):
    """Return info on a Zephon weapon. Optionally include a unit name for more accurate info.

    Args:
        weaponname (str): Name of weapon to look up
        unitname (str): Name of unit wielding the weapon
    """
    await return_info(interaction, weaponname, verbose, flavor, invisible, 'ZWeapon', embed.create_zweapon_embed, unitname, 'ZUnit')


bot.run(TOKEN)
