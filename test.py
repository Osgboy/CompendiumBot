#!~/bot-env/Scripts/python.exe
import discord
import os
import json
from thefuzz import fuzz
from typing import Callable
from dotenv import load_dotenv
from discord.ext import commands
# import cProfile, pstats, io
# from pstats import SortKey
# pr = cProfile.Profile(timeunit=0.001)
# pr.enable()
# pr.disable()
# s = io.StringIO()
# sortby = SortKey.CUMULATIVE
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# with open('cprofile.txt', 'w') as fout:
#     fout.write(s.getvalue())

load_dotenv()
TOKEN = os.getenv("TEST_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)
dicts = {}


RARITY_COLORS = {'Common': discord.colour.Color.from_rgb(255, 255, 255),
                 'Uncommon': discord.colour.Color.from_rgb(0, 191, 191),
                 'Artefact': discord.colour.Color.from_rgb(191, 0, 191),
                 'Rare': discord.colour.Color.from_rgb(191, 0, 191)}
GLADIUS_FACTION_COLORS = {'Adeptus Mechanicus': discord.colour.Color.from_rgb(159, 38, 40),
                          'Astra Militarum': discord.colour.Color.from_rgb(50, 73, 53),
                          'Chaos Space Marines': discord.colour.Color.from_rgb(57, 75, 87),
                          'Drukhari': discord.colour.Color.from_rgb(15, 69, 78),
                          'Eldar': discord.colour.Color.from_rgb(52, 115, 121),
                          'Necrons': discord.colour.Color.from_rgb(4, 83, 42),
                          'Neutral': discord.colour.Color.from_rgb(255, 255, 255),
                          'Orks': discord.colour.Color.from_rgb(70, 91, 24),
                          'Sisters Of Battle': discord.colour.Color.from_rgb(87, 12, 12),
                          'Space Marines': discord.colour.Color.from_rgb(75, 98, 98),
                          'Tau': discord.colour.Color.from_rgb(46, 90, 106),
                          'Tyranids': discord.colour.Color.from_rgb(99, 37, 103)}
ZEPHON_BRANCH_COLORS = {'Cyber': discord.colour.Color.from_rgb(16, 121, 130),
                        'Human': discord.colour.Color.from_rgb(154, 129, 35),
                        'Voice': discord.colour.Color.from_rgb(123, 65, 150),
                        'Zephon': discord.colour.Color.from_rgb(205, 59, 66),
                        'Reaver': discord.colour.Color.from_rgb(138, 97, 70),
                        'Acrin': discord.colour.Color.from_rgb(62, 192, 158),
                        'Neutral': discord.colour.Color.from_rgb(255, 255, 255)}
GLADIUS_ICONS = {'biomass': '<:Biomass:1240218802831233118>', 'requisitions': '<:Requisitions:1240222555588268032>',
                 'food': '<:Food:1240218818660532317>', 'ore': '<:Ore:1240218839644377181>',
                 'energy': '<:Energy:1240221846343782501>', 'influence': '<:Influence:1240218825836728341>',
                 'production': '<:Production:1240330971514011668>',

                 'armor': '<:Armor:1240218799832174703>', 'hitpoints': '<:Hitpoints:1240330759781482528>',
                 'morale': '<:Morale:1240218836171493386>', 'movement': '<:Movement:1240222322770579487>',
                 'cargoSlots': '<:CargoSlots:1240218804982775848>', 'itemSlots': '<:ItemSlots:1240218829280378912>',

                 'damage': '<:Damage:1240218813123919893>', 'attacks': '<:Attacks:1240218801799434241>',
                 'armorPenetration': '<:ArmorPenetration:1240218800855715840>', 'accuracy': '<:Accuracy:1240218797458063361>',
                 'range': '<:Range:1240218850763477013>',

                 'actions': '<:Actions:1240218798532071515>', 'cooldown': '<:Cooldown:1240218808224972800>',
                 'transport': '<:Transport:1256002013037203587>'}
ZEPHON_ICONS = {'food': '<:Food:1250986007537647687>', 'minerals': '<:Minerals:1250986099023806464>',
                'energy': '<:Energy:1250985795242954764>', 'influence': '<:Influence:1250986095739404339>',
                'algae': '<:Algae:1250981089540046929>', 'chips': '<:Chips:1250985791455494174>',
                'antimatter': '<:Antimatter:1250981090278117416>', 'dimensionalEchoes': '<:DimensionalEchoes:1250985794450227240>',
                'singularityCores': '<:SingularityCores:1250986245085986909>', 'transuranium': '<:Transuranium:1250986247086669937>',
                'production': '<:Production:1250986164626657383>',

                'groupSize': '<:GroupSize:1250986008606933012>',
                'armor': '<:Armor:1250981091125362788>', 'hitpoints': '<:Hitpoints:1250986009429282866>',
                'morale': '<:Morale:1250986099816530033>', 'movement': '<:Movement:1250986100621836400>',
                'cargoSlots': '<:CargoSlots:1250981096070582273>', 'itemSlots': '<:ItemSlots:1250986096616017961>',

                'damage': '<:Damage:1250985792197628004>', 'attacks': '<:Attacks:1250981093314662411>',
                'armorPenetration': '<:ArmorPenetration:1250981091917955193>', 'accuracy': '<:Accuracy:1250981087954468914>',
                'range': '<:Range:1250986241604849664>',

                'actions': '<:Actions:1250981088701186128>', 'turns': '<:Turns:1250986247896305776>',
                'transport': '<:Transport:1256002285536804936>'}
GLADIUS_RESOURCES = ('biomass', 'requisitions', 'food',
                     'ore', 'energy', 'influence')
ZEPHON_RESOURCES = ('food', 'minerals', 'energy', 'transuranium', 'antimatter',
                    'dimensionalEchoes', 'singularityCores', 'algae', 'chips', 'influence')


class NotFoundError(Exception):
    def __init__(self, bestMatch: str):
        self.bestMatch = bestMatch


class UnitNotFoundError(Exception):
    def __init__(self, bestMatch: str):
        self.bestMatch = bestMatch


def fuzzy_match(classDict: dict, name: str) -> tuple[str, dict]:
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
        raise NotFoundError(bestMatch)


def operate(operand1: float, weaponStats: dict, key: str) -> float:
    try:
        operator = weaponStats[key]['operator']
        operand2 = weaponStats[key]['value']
    except KeyError:
        return operand1
    if operator in ('base', 'min', 'max'):
        return operand2
    elif operator == 'add':
        return operand1 + operand2
    elif operator == 'mul':
        return operand1 * (1 + operand2)


def calculate_gweapon_stats(range: str, weaponStats: dict, unitStats: dict = {'meleeAccuracy': 6, 'rangedAccuracy': 6,
                                                                              'meleeAttacks': 1, 'strengthDamage': 1}) -> dict:
    finalStats = {'attacks': 1, 'armorPen': 0,
                  'damage': 0, 'accuracy': 6}
    # Melee or ranged
    if range == 'Melee':
        prefix = 'melee'
    else:
        prefix = 'ranged'
    # Attacks
    if prefix == 'melee':
        finalStats['attacks'] = operate(
            unitStats['meleeAttacks'], weaponStats, 'meleeAttacks')
    finalStats['attacks'] = operate(
        finalStats['attacks'], weaponStats, 'attacks')
    # Armor penetration
    finalStats['armorPen'] = int(
        operate(finalStats['armorPen'], weaponStats, prefix + 'ArmorPenetration'))
    # Damage
    strengthDamage = operate(unitStats['strengthDamage'],
                             weaponStats, 'strengthDamage')
    damage = operate(strengthDamage, weaponStats, prefix + 'Damage')
    finalStats['damage'] = '{0:.2f}'.format(damage)
    # Accuracy
    accuracy = operate(unitStats[prefix + 'Accuracy'],
                       weaponStats, prefix + 'Accuracy')
    finalStats['accuracy'] = int(accuracy)
    return finalStats


def calculate_zweapon_stats(weaponStats: dict, unitAccuracy: int = 6) -> dict:
    finalStats = {'attacks': 0, 'armorPen': 0,
                  'damage': 0, 'accuracy': 6}
    finalStats['attacks'] = operate(
        finalStats['attacks'], weaponStats, 'attacks')
    finalStats['armorPen'] = int(operate(
        finalStats['armorPen'], weaponStats, 'armorPenetration'))
    finalStats['damage'] = operate(
        finalStats['damage'], weaponStats, 'damage')
    finalStats['accuracy'] = int(operate(
        unitAccuracy, weaponStats, 'accuracy'))
    return finalStats


class ConfirmFuzzyMatch(discord.ui.View):
    def __init__(self, name: str, verbose: bool, classDict: dict, embedFunc: Callable[[str, dict, bool, str], discord.Embed], unitName: str):
        super().__init__(timeout=60)
        self.name = name
        self.verbose = verbose
        self.classDict = classDict
        self.embedFunc = embedFunc
        self.unitName = unitName

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed, fullIconPath = match_and_create_embed(
                self.name, self.verbose, self.classDict, self.embedFunc, self.unitName)
        except UnitNotFoundError as unf:
            await interaction.response.edit_message(content=f'**{self.unitName}** not found. Did you mean **{unf.bestMatch}**?')
            self.unitName = unf.bestMatch
            print(repr(unf))
        else:
            try:
                image = discord.File(fullIconPath, filename='icon.png')
                embed.set_thumbnail(url="attachment://icon.png")
                await interaction.response.edit_message(content=None, embed=embed, attachments=[image], view=None)
                print('Successfully returned request after editing.')
            except FileNotFoundError:
                await interaction.response.edit_message(content=None, embed=embed, view=None)
                print('Successfully returned request without icon after editing.')


def match_and_create_embed(name: str, verbose: bool, classDict: dict,
                           embedFunc: Callable[[str, dict, bool, str], discord.Embed], unitName: str) -> tuple[discord.Embed, str]:
    objName, objDict = fuzzy_match(classDict, name)
    embed = embedFunc(objName, objDict, verbose, unitName)
    fullIconPath = objDict['iconPath']
    return embed, fullIconPath


async def return_info(interaction: discord.Interaction, name: str, verbose: bool, invisible: bool, key: str,
                      embedFunc: Callable[[dict, bool, str], discord.Embed], unitName: str = None):
    print(f'\nReceived request for:\n'
          f'- Class: {key}\n'
          f'- Name: {name}\n'
          f'- Unit Name: {unitName}\n')
    try:
        embed, fullIconPath = match_and_create_embed(
            name, verbose, dicts[key], embedFunc, unitName)
    except NotFoundError as nf:
        await interaction.response.send_message(f'**{name}** not found. Did you mean **{nf.bestMatch}**?', ephemeral=invisible,
                                                view=ConfirmFuzzyMatch(nf.bestMatch, verbose, dicts[key], embedFunc, unitName))
        print(repr(nf))
    except UnitNotFoundError as unf:
        await interaction.response.send_message(f'**{unitName}** not found. Did you mean **{unf.bestMatch}**?', ephemeral=invisible,
                                                view=ConfirmFuzzyMatch(name, verbose, dicts[key], embedFunc, unf.bestMatch))
        print(repr(unf))
    else:
        try:
            image = discord.File(fullIconPath, filename='icon.png')
            embed.set_thumbnail(url="attachment://icon.png")
            await interaction.response.send_message(embed=embed, file=image, ephemeral=invisible)
            print('Successfully returned request.')
        except FileNotFoundError:
            await interaction.response.send_message(embed=embed, ephemeral=invisible)
            print('Successfully returned request without icon.')


def create_gitem_embed(name: str, attrs: dict, verbose: bool, _) -> discord.Embed:
    # Name and Description
    embed = discord.Embed(title=name, description=attrs['description'])

    # Color
    embed.colour = RARITY_COLORS[attrs['rarity']]

    # Rarity
    embed.add_field(name='Rarity', value=attrs['rarity'])

    # Influence cost
    embed.add_field(
        name='Cost', value=f"{GLADIUS_ICONS['influence']} {attrs['influenceCost']}")

    # Ability
    if (ability := attrs['ability']):
        embed.add_field(name='Ability', value=ability[:1024], inline=False)

    # Flavor
    if verbose:
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_zitem_embed(name: str, attrs: dict, verbose: bool, _) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = RARITY_COLORS[attrs['rarity']]

    # Rarity
    embed.add_field(name='Rarity', value=attrs['rarity'])

    # Branch
    embed.add_field(name='Branch', value=attrs['branch'])

    # Influence cost
    embed.add_field(
        name='Cost', value=f"{ZEPHON_ICONS['influence']} {attrs['influenceCost']}")

    # Buy condition
    if (buyCondition := attrs['buyCondition']):
        embed.add_field(name='Prerequisite', value=buyCondition)

    # Ability
    if (ability := attrs['ability']):
        embed.add_field(name='Ability', value=ability[:1024], inline=False)

    # Flavor
    if verbose:
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_gunit_embed(name: str, attrs: dict, verbose: bool, _) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = GLADIUS_FACTION_COLORS[attrs['faction']]

    # Faction
    embed.add_field(name='Faction', value=attrs['faction'], inline=False)

    # Cost
    costText = [GLADIUS_ICONS['production'],
                ' ', attrs['resourceStats']['productionCost']]
    for resource in GLADIUS_RESOURCES:
        cost = attrs['resourceStats'][resource + 'Cost']
        if cost != '0':
            costText.extend((' | ', GLADIUS_ICONS[resource], ' ', cost))
    embed.add_field(name="Cost", value=''.join(costText))

    # Upkeep
    upkeepText = []
    for resource in GLADIUS_RESOURCES:
        upkeep = attrs['resourceStats'][resource + 'Upkeep']
        if upkeep != '0':
            upkeepText.extend(
                (' | ', GLADIUS_ICONS[resource], ' ', upkeep))
    if upkeepText == []:
        upkeepText = ['None']
    else:
        # delete initial ' | '
        del upkeepText[0]
    embed.add_field(name='Upkeep', value=''.join(upkeepText))

    # Stats
    statText = (f"**{attrs['combatStats']['groupSizeMax']} model(s)**\n"
                f"{GLADIUS_ICONS['armor']} {attrs['combatStats']['armor']} | {GLADIUS_ICONS['hitpoints']} {round(attrs['combatStats']['hitpointsMax'])} | "
                f"{GLADIUS_ICONS['morale']} {attrs['combatStats']['moraleMax']}\n {GLADIUS_ICONS['movement']} {attrs['combatStats']['movementMax']} | "
                f"{GLADIUS_ICONS['cargoSlots']} {attrs['combatStats']['cargoSlots']} | {GLADIUS_ICONS['itemSlots']} {attrs['combatStats']['itemSlots']}")
    embed.add_field(name='Stats', value=statText)

    # Weapons
    weaponsText = []
    for weapon in attrs['weapons']:
        # if upgrade required
        if attrs['weapons'][weapon]['requiredUpgrade']:
            upgrade = ' (U)'
        else:
            upgrade = ''
        # if weapon is secondary
        if attrs['weapons'][weapon]['secondary']:
            secondary = ' (S)'
        else:
            secondary = ''
        weaponsText.extend(
            f"{attrs['weapons'][weapon]['count']}x {weapon}{upgrade}{secondary}\n")
    if weaponsText == []:
        weaponsText = ['None']
    embed.add_field(name='Weapons', value=''.join(weaponsText))

    # Traits
    traitsText = []
    for trait in attrs['traits']:
        # if upgrade required
        if attrs['traits'][trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText))

    # Actions
    actionsText = []
    for action in attrs['actions']:
        # if upgrade required
        if attrs['actions'][action]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        actionsText.extend((action, upgrade, '\n'))
    if actionsText == []:
        actionsText = ['None']
    embed.add_field(name='Actions', value=''.join(actionsText))

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)
        embed.set_footer(text=('Traits/weapons marked with (U) require a researchable upgrade.\n'
                               'Weapons marked with (S) are secondary weapons.\n'
                               'Stat-changing traits like Fleet not taken into account.'))

    return embed


def create_zunit_embed(name: str, attrs: dict, verbose: bool, _) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = ZEPHON_BRANCH_COLORS[attrs['branch']]

    # Branch
    embed.add_field(name='Branch', value=attrs['branch'], inline=False)

    # Cost
    costText = [ZEPHON_ICONS['production'],
                ' ', attrs['resourceStats']['productionCost']]
    for resource in ZEPHON_RESOURCES:
        cost = attrs['resourceStats'][resource + 'Cost']
        if cost != '0':
            costText.extend((' | ', ZEPHON_ICONS[resource], ' ', cost))
    embed.add_field(name='Cost', value=''.join(costText))

    # Upkeep
    upkeepText = []
    for resource in ZEPHON_RESOURCES:
        upkeep = attrs['resourceStats'][resource + 'Upkeep']
        if upkeep != '0':
            upkeepText.extend(
                (' | ', ZEPHON_ICONS[resource], ' ', upkeep))
    if upkeepText == []:
        upkeepText = ['None']
    else:
        # delete initial ' | '
        del upkeepText[0]
    embed.add_field(name='Upkeep', value=''.join(upkeepText))

    # Stats
    statText = (f"{ZEPHON_ICONS['groupSize']} {attrs['combatStats']['groupSizeMax']} | {ZEPHON_ICONS['accuracy']} {attrs['combatStats']['accuracy']}\n"
                f"{ZEPHON_ICONS['armor']} {attrs['combatStats']['armor']} | {ZEPHON_ICONS['hitpoints']} {attrs['combatStats']['hitpointsMax']} | "
                f"{ZEPHON_ICONS['morale']} {attrs['combatStats']['moraleMax']}\n {ZEPHON_ICONS['movement']} {attrs['combatStats']['movementMax']} | "
                f"{ZEPHON_ICONS['cargoSlots']} {attrs['combatStats']['cargoSlots']} | {ZEPHON_ICONS['itemSlots']} {attrs['combatStats']['itemSlots']}")
    embed.add_field(name='Stats', value=statText)

    # Weapons
    weaponsText = []
    for weapon in attrs['weapons']:
        # if upgrade required
        if attrs['weapons'][weapon]['requiredUpgrade']:
            upgrade = ' (U)'
        else:
            upgrade = ''
        # if weapon is secondary
        if attrs['weapons'][weapon]['secondary']:
            secondary = ' (S)'
        else:
            secondary = ''
        weaponsText.extend(
            f"{attrs['weapons'][weapon]['count']}x {weapon}{upgrade}{secondary}\n")
    if weaponsText == []:
        weaponsText = ['None']
    embed.add_field(name='Weapons', value=''.join(weaponsText))

    # Traits
    traitsText = []
    for trait in attrs['traits']:
        # if upgrade required
        if attrs['traits'][trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText))

    # Actions
    actionsText = []
    for action in attrs['actions']:
        # if upgrade required
        if attrs['actions'][action]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        actionsText.extend((action, upgrade, '\n'))
    if actionsText == []:
        actionsText = ['None']
    embed.add_field(name='Actions', value=''.join(actionsText))

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)
        embed.set_footer(text=('Traits/weapons marked with (U) require a researchable upgrade.\n'
                               'Weapons marked with (S) are secondary weapons.\n'
                               'Stat-changing traits like Fleet not taken into account.'))

    return embed


def create_gweapon_embed(name: str, attrs: dict, verbose: bool, unitName: str = None) -> discord.Embed:
    if unitName:
        try:
            unitName, unitDict = fuzzy_match(dicts['GUnit'], unitName)
        except NotFoundError as e:
            raise UnitNotFoundError(e.bestMatch)
        weaponStats = calculate_gweapon_stats(
            attrs['range'], attrs['innateStats'], unitDict['weaponStats'])
    else:
        weaponStats = calculate_gweapon_stats(
            attrs['range'], attrs['innateStats'])

    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Wielder
    if unitName:
        embed.add_field(name='Wielder', value=unitName, inline=False)

    # Stats
    statText = (f"{GLADIUS_ICONS['damage']} {weaponStats['damage']} | {GLADIUS_ICONS['attacks']} {weaponStats['attacks']} | "
                f"{GLADIUS_ICONS['armorPenetration']} {weaponStats['armorPen']} | {GLADIUS_ICONS['accuracy']} {weaponStats['accuracy']} | "
                f"{GLADIUS_ICONS['range']} {attrs['range']}")
    embed.add_field(name='Stats', value=statText)

    # Traits
    traitsText = []
    for trait in attrs['traits']:
        # if upgrade required
        if attrs['traits'][trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText), inline=False)

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)
        embed.set_footer(text=('Traits marked with (U) require a researchable upgrade.\n'
                               'Weapon stats depend on the unit wielding the weapon. Stat-changing traits like Twin-Linked not taken into account. '
                               'Values shown may not be accurate.'))

    return embed


def create_zweapon_embed(name: str, attrs: dict, verbose: bool, unitName: str = None) -> discord.Embed:
    if unitName:
        try:
            unitName, unitDict = fuzzy_match(dicts['ZUnit'], unitName)
        except NotFoundError as e:
            raise UnitNotFoundError(e.bestMatch)
        weaponStats = calculate_zweapon_stats(
            attrs['innateStats'], unitDict['combatStats']['accuracy'])
    else:
        weaponStats = calculate_zweapon_stats(attrs['innateStats'])

    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Wielder
    if unitName:
        embed.add_field(name='Wielder', value=unitName, inline=False)

    # Stats
    statText = (f"{ZEPHON_ICONS['damage']} {weaponStats['damage']} | {ZEPHON_ICONS['attacks']} {weaponStats['attacks']} | "
                f"{ZEPHON_ICONS['armorPenetration']} {weaponStats['armorPen']} | {ZEPHON_ICONS['accuracy']} {weaponStats['accuracy']} | "
                f"{ZEPHON_ICONS['range']} {attrs['range']}")
    embed.add_field(name='Stats', value=statText)

    # Traits
    traitsText = []
    for trait in attrs['traits']:
        # if upgrade required
        if attrs['traits'][trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText), inline=False)

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)
        embed.set_footer(text=('Traits marked with (U) require a researchable upgrade.\n'
                               'Weapon stats depend on the unit wielding the weapon. Stat-changing traits like Twin-Linked not taken into account. '
                               'Values shown may not be accurate.'))

    return embed


def create_gtrait_embed(name: str, attrs: dict, verbose: bool, _) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    try:
        embed.colour = GLADIUS_FACTION_COLORS[attrs['faction']]
    except KeyError:
        embed.colour = GLADIUS_FACTION_COLORS['Neutral']

    # Faction
    embed.add_field(name='Faction', value=attrs['faction'])

    # Modifiers
    if (modifiers := attrs['modifiers']):
        embed.add_field(name='Modifiers', value=modifiers[:1024], inline=False)

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_ztrait_embed(name: str, attrs: dict, verbose: bool, _) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Modifiers
    if (modifiers := attrs['modifiers']):
        embed.add_field(name='Modifiers', value=modifiers[:1024], inline=False)

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_gaction_embed(name: str, attrs: dict, verbose: bool, _) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Cooldown
    if attrs['cooldown'] == 'Passive':
        embed.add_field(name='Cooldown', value='Passive', inline=False)
    else:
        embed.add_field(
            name='Cooldown', value=f"{GLADIUS_ICONS['cooldown']} {attrs['cooldown']}", inline=False)

    # Conditions
    embed.add_field(name=f"Required upgrade", value=str(
        attrs['conditions']['requiredUpgrade']))
    embed.add_field(name=f"Requires {GLADIUS_ICONS['actions']} AP?", value=str(
        attrs['conditions']['requiredActionPoints']))
    embed.add_field(name=f"Requires {GLADIUS_ICONS['movement']} movement?", value=str(
        attrs['conditions']['requiredMovement']))
    embed.add_field(name=f"Usable in {GLADIUS_ICONS['transport']} transport?", value=str(
        attrs['conditions']['usableInTransport']))
    embed.add_field(name=f"Consumes {GLADIUS_ICONS['actions']} AP?", value=str(
        attrs['conditions']['consumedActionPoints']))
    embed.add_field(name=f"Consumes {GLADIUS_ICONS['movement']} movement?", value=str(
        attrs['conditions']['consumedMovement']))

    # Modifiers
    if (modifiers := attrs['modifiers']):
        embed.add_field(name='Modifiers', value=modifiers[:1024], inline=False)

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_zaction_embed(name: str, attrs: dict, verbose: bool, _) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Cooldown
    if attrs['cooldown'] == 'Passive':
        embed.add_field(name='Cooldown', value='Passive', inline=False)
    else:
        embed.add_field(
            name='Cooldown', value=f"{ZEPHON_ICONS['turns']} {attrs['cooldown']}", inline=False)

    # Conditions
    embed.add_field(name=f"Required upgrade", value=str(
        attrs['conditions']['requiredUpgrade']))
    embed.add_field(name=f"Requires {ZEPHON_ICONS['actions']} AP?", value=str(
        attrs['conditions']['requiredActionPoints']))
    embed.add_field(name=f"Requires {ZEPHON_ICONS['movement']} movement?", value=str(
        attrs['conditions']['requiredMovement']))
    embed.add_field(name=f"Usable in {ZEPHON_ICONS['transport']} transport?", value=str(
        attrs['conditions']['usableInTransport']))
    embed.add_field(name=f"Consumes {ZEPHON_ICONS['actions']} AP?", value=str(
        attrs['conditions']['consumedActionPoints']))
    embed.add_field(name=f"Consumes {ZEPHON_ICONS['movement']} movement?", value=str(
        attrs['conditions']['consumedMovement']))

    # Modifiers
    if (modifiers := attrs['modifiers']):
        embed.add_field(name='Modifiers', value=modifiers[:1024], inline=False)

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


@client.event
async def on_ready():
    JSON_DIR = os.path.join('json')
    print(f'We have logged in as {client.user}')
    synced = await client.tree.sync()
    print("# CMDs synced: " + str(len(synced)))

    for objClass in ('GAction', 'ZAction', 'GItem', 'ZItem', 'GUnit', 'ZUnit', 'GTrait', 'ZTrait', 'GWeapon', 'ZWeapon'):
        with open(os.path.join(JSON_DIR, objClass + '.json'), 'r') as file:
            dicts[objClass] = json.load(file)
            print(f"Loaded {objClass}.json")


def docstring_defaults(func):
    doc = func.__doc__ or ''
    doc += "\tverbose (bool): Flag to include flavor and footer text (default is False)" + \
        "\n\tinvisible (bool): Flag to make the bot's reply invisible to everyone except you (default is False)"
    func.__doc__ = doc
    return func


@client.tree.command(name='gitem')
@docstring_defaults
async def gitem(interaction: discord.Interaction, itemname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Gladius item.

    Args:
        itemname (str): Name of item to look up
    """
    await return_info(interaction, itemname, verbose, invisible, 'GItem', create_gitem_embed)


@client.tree.command(name='zitem')
@docstring_defaults
async def gitem(interaction: discord.Interaction, itemname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Zephon item.

    Args:
        itemname (str): Name of item to look up
    """
    await return_info(interaction, itemname, verbose, invisible, 'ZItem', create_zitem_embed)


@client.tree.command(name='gunit')
@docstring_defaults
async def gunit(interaction: discord.Interaction, unitname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Gladius unit.

    Args:
        unitname (str): Name of unit to look up
    """
    await return_info(interaction, unitname, verbose, invisible, 'GUnit', create_gunit_embed)


@client.tree.command(name='zunit')
@docstring_defaults
async def gunit(interaction: discord.Interaction, unitname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Zephon unit.

    Args:
        unitname (str): Name of unit to look up
    """
    await return_info(interaction, unitname, verbose, invisible, 'ZUnit', create_zunit_embed)


@client.tree.command(name='gweapon')
@docstring_defaults
async def gweapon(interaction: discord.Interaction, weaponname: str, unitname: str = '', verbose: bool = False, invisible: bool = False):
    """Return info on a Gladius weapon. Optionally include a unit name for more accurate info.

    Args:
        weaponname (str): Name of weapon to look up
        unitname (str): Name of unit wielding the weapon
    """
    await return_info(interaction, weaponname, verbose, invisible, 'GWeapon', create_gweapon_embed, unitname)


@client.tree.command(name='zweapon')
@docstring_defaults
async def zweapon(interaction: discord.Interaction, weaponname: str, unitname: str = '', verbose: bool = False, invisible: bool = False):
    """Return info on a Zephon weapon. Optionally include a unit name for more accurate info.

    Args:
        weaponname (str): Name of weapon to look up
        unitname (str): Name of unit wielding the weapon
    """
    await return_info(interaction, weaponname, verbose, invisible, 'ZWeapon', create_zweapon_embed, unitname)


@client.tree.command(name='gtrait')
@docstring_defaults
async def gtrait(interaction: discord.Interaction, traitname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Gladius trait.

    Args:
        traitname (str): Name of trait to look up
    """
    await return_info(interaction, traitname, verbose, invisible, 'GTrait', create_gtrait_embed)


@client.tree.command(name='ztrait')
@docstring_defaults
async def ztrait(interaction: discord.Interaction, traitname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Zephon trait.

    Args:
        traitname (str): Name of trait to look up
    """
    await return_info(interaction, traitname, verbose, invisible, 'ZTrait', create_ztrait_embed)


@client.tree.command(name='gaction')
@docstring_defaults
async def gaction(interaction: discord.Interaction, actionname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Gladius action.

    Args:
        actionname (str): Name of action to look up
        unitname (str): Name of unit with the action
    """
    await return_info(interaction, actionname, verbose, invisible, 'GAction', create_gaction_embed)


@client.tree.command(name='zaction')
@docstring_defaults
async def zaction(interaction: discord.Interaction, actionname: str, verbose: bool = False, invisible: bool = False):
    """Return info on a Zephon action.

    Args:
        actionname (str): Name of action to look up
        unitname (str): Name of unit with the action
    """
    await return_info(interaction, actionname, verbose, invisible, 'ZAction', create_zaction_embed)

client.run(TOKEN)
