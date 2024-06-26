#!~/bot-env/Scripts/python.exe
import discord
import os
from typing import Type, Callable
from item import *
from unit import *
from weapon import *
from trait import *
from action import *
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
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)


RARITY_COLORS = {'Common':discord.colour.Color.from_rgb(255, 255, 255),
                'Uncommon':discord.colour.Color.from_rgb(0, 191, 191),
                'Artefact':discord.colour.Color.from_rgb(191, 0, 191),
                'Rare':discord.colour.Color.from_rgb(191, 0, 191)}
GLADIUS_FACTION_COLORS = {'AdeptusMechanicus':discord.colour.Color.from_rgb(159, 38, 40),
                  'AstraMilitarum':discord.colour.Color.from_rgb(50, 73, 53),
                  'ChaosSpaceMarines':discord.colour.Color.from_rgb(57, 75, 87),
                  'Drukhari':discord.colour.Color.from_rgb(15, 69, 78),
                  'Eldar':discord.colour.Color.from_rgb(52, 115, 121),
                  'Necrons':discord.colour.Color.from_rgb(4, 83, 42),
                  'Neutral':discord.colour.Color.from_rgb(255, 255, 255),
                  'Orks':discord.colour.Color.from_rgb(70, 91, 24),
                  'SistersOfBattle':discord.colour.Color.from_rgb(87, 12, 12),
                  'SpaceMarines':discord.colour.Color.from_rgb(75, 98, 98),
                  'Tau':discord.colour.Color.from_rgb(46, 90, 106),
                  'Tyranids':discord.colour.Color.from_rgb(99, 37, 103)}
ZEPHON_BRANCH_COLORS = {'Cyber':discord.colour.Color.from_rgb(16, 121, 130),
                 'Human':discord.colour.Color.from_rgb(154, 129, 35),
                 'Voice':discord.colour.Color.from_rgb(123, 65, 150),
                 'Zephon':discord.colour.Color.from_rgb(205, 59, 66),
                 'Reaver':discord.colour.Color.from_rgb(138, 97, 70),
                 'Acrin':discord.colour.Color.from_rgb(62, 192, 158),
                 'Neutral':discord.colour.Color.from_rgb(255, 255, 255)}
GLADIUS_ICONS = {'biomass':'<:Biomass:1240218802831233118>', 'requisitions':'<:Requisitions:1240222555588268032>',
                'food':'<:Food:1240218818660532317>', 'ore':'<:Ore:1240218839644377181>',
                'energy':'<:Energy:1240221846343782501>', 'influence':'<:Influence:1240218825836728341>',
                'production':'<:Production:1240330971514011668>',
                
                'armor':'<:Armor:1240218799832174703>', 'hitpoints':'<:Hitpoints:1240330759781482528>',
                'morale':'<:Morale:1240218836171493386>', 'movement':'<:Movement:1240222322770579487>',
                'cargoSlots':'<:CargoSlots:1240218804982775848>', 'itemSlots':'<:ItemSlots:1240218829280378912>',
                
                'damage':'<:Damage:1240218813123919893>', 'attacks':'<:Attacks:1240218801799434241>',
                'armorPenetration':'<:ArmorPenetration:1240218800855715840>', 'accuracy':'<:Accuracy:1240218797458063361>',
                'range':'<:Range:1240218850763477013>'}
ZEPHON_ICONS = {'food':'<:Food:1250986007537647687>', 'minerals':'<:Minerals:1250986099023806464>',
                'energy':'<:Energy:1250985795242954764>', 'influence':'<:Influence:1250986095739404339>',
                'algae':'<:Algae:1250981089540046929>', 'chips':'<:Chips:1250985791455494174>',
                'antimatter':'<:Antimatter:1250981090278117416>', 'dimensionalEchoes':'<:DimensionalEchoes:1250985794450227240>',
                'singularityCores':'<:SingularityCores:1250986245085986909>', 'transuranium':'<:Transuranium:1250986247086669937>',
                'production':'<:Production:1250986164626657383>',
                
                'groupSize':'<:GroupSize:1250986008606933012>',
                'armor':'<:Armor:1250981091125362788>', 'hitpoints':'<:Hitpoints:1250986009429282866>',
                'morale':'<:Morale:1250986099816530033>', 'movement':'<:Movement:1250986100621836400>',
                'cargoSlots':'<:CargoSlots:1250981096070582273>', 'itemSlots':'<:ItemSlots:1250986096616017961>',
                
                'damage':'<:Damage:1250985792197628004>', 'attacks':'<:Attacks:1250981093314662411>',
                'armorPenetration':'<:ArmorPenetration:1250981091917955193>', 'accuracy':'<:Accuracy:1250981087954468914>',
                'range':'<:Range:1250986241604849664>'}
GLADIUS_RESOURCES = ('biomass', 'requisitions', 'food', 'ore', 'energy', 'influence')
ZEPHON_RESOURCES = ('food', 'minerals', 'energy', 'transuranium', 'antimatter', 'dimensionalEchoes', 'singularityCores', 'algae', 'chips', 'influence')


def camel_case_split(s: str) -> str:
    # use map to add an underscore before each uppercase letter
    modified_string = list(map(lambda x: '_' + x if x.isupper() else x, s))
    # join the modified string and split it at the underscores
    split_string = ''.join(modified_string).split('_')
    # remove any empty strings from the list
    # split_string = list(filter(lambda x: x != '', split_string))
    split_string = ' '.join(split_string)
    return split_string

def get_thumbnail(embed, obj, internalPath='internalID'):
    try:
        fullIconPath = './' + obj.game + '/Icons/' + obj.iconPath + '.png'
    except (AttributeError, TypeError):
        fullIconPath = './' + obj.game + '/Icons/' + obj.objClass + '/' + getattr(obj, internalPath) + '.png'
    try:
        image = discord.File(fullIconPath, filename='icon.png')
        embed.set_thumbnail(url="attachment://icon.png")
        return {'file':image, 'embed':embed}
    except FileNotFoundError:
        return {'embed':embed}

async def return_info(interaction: discord.Interaction, name: str, verbose:bool, invisible:bool, game: str, cls: Type[Obj], embedFunc: Callable[[Obj, bool, ], discord.Embed], unitName:str=None):
    obj = cls(name, game)
    obj.fuzzy_match_name(obj.get_obj_info)
    markdown = '**'
    if not obj.found:
        await interaction.response.send_message(markdown + name + markdown + ' not found. Did you mean ' + markdown + obj.bestMatch + markdown + '?')
        return
    obj.get_icon_path()
    if unitName:
        if game == 'Gladius':
            unit = GUnit(unitName, 'Gladius')
        elif game == 'Zephon':
            unit = ZUnit(unitName, 'Zephon')
        unit.fuzzy_match_name(unit.get_obj_min_info)
        if not unit.found:
            await interaction.response.send_message(markdown + unitName + markdown + ' not found. Did you mean ' + markdown + unit.bestMatch + markdown + '?')
            return
        embed = embedFunc(obj, verbose, unit)
    else:
        embed = embedFunc(obj, verbose)    
    try:
        if not (internalPath := obj.iconPath):
            raise AttributeError
    except AttributeError:
        try:
            internalPath = obj.objClass + '/' + obj.factionAndID
        except AttributeError:
            internalPath = obj.objClass + '/' + obj.internalID
    fullIconPath = './' + obj.game + '/Icons/' + internalPath + '.png'
    try:
        image = discord.File(fullIconPath, filename='icon.png')
        embed.set_thumbnail(url="attachment://icon.png")
        await interaction.response.send_message(embed=embed, file=image, ephemeral=invisible)
    except FileNotFoundError:
        await interaction.response.send_message(embed=embed, ephemeral=invisible)
    
def create_gitem_embed(item: GItem, verbose: bool) -> discord.Embed:
    item.get_item_ability()
    item.get_item_rarity()
    item.get_item_influence_cost()

    # Name and Description
    embed = discord.Embed(title=item.name, description=item.description)

    # Color
    embed.colour = RARITY_COLORS[item.rarity]

    # Rarity
    embed.add_field(name='Rarity', value=item.rarity)

    # Influence cost
    embed.add_field(name='Cost', value=GLADIUS_ICONS['influence'] + ' ' + item.influenceCost)

    # Ability
    if verbose:
        try:
            embed.add_field(name='Ability', value=item.ability, inline=False)
        except AttributeError:
            pass

    # Flavor
    if verbose:
        try:
            embed.add_field(name='Flavor', value='*' + item.flavor + '*', inline=False)
        except AttributeError:
            pass

    return embed

def create_zitem_embed(item: ZItem, verbose: bool) -> discord.Embed:
    item.get_branch()
    item.get_item_ability()
    item.get_item_rarity()
    item.get_item_influence_cost()
    item.get_buy_conditions()

    # Name and Description
    try:
        embed = discord.Embed(title=item.name, description=item.description)
    except AttributeError:
        embed = discord.Embed(title=item.name)

    # Color
    embed.colour = RARITY_COLORS[item.rarity]

    # Rarity
    embed.add_field(name='Rarity', value=item.rarity)

    # Branch
    embed.add_field(name='Branch', value=item.branch)

    # Influence cost
    embed.add_field(name='Cost', value=ZEPHON_ICONS['influence'] + ' ' + item.influenceCost)

    # Buy condition
    try:
        embed.add_field(name='Prerequisite', value=item.buyCondition)
    except AttributeError:
        pass

    # Ability
    if verbose:
        try:
            embed.add_field(name='Ability', value=item.ability, inline=False)
        except AttributeError:
            pass

    # Flavor
    if verbose:
        try:
            embed.add_field(name='Flavor', value='*' + item.flavor + '*', inline=False)
        except AttributeError:
            pass

    return embed

def create_gunit_embed(unit: GUnit, verbose: bool) -> discord.Embed:
    unit.get_unit_stats()
    unit.get_unit_count()
    unit.get_unit_weapons()
    unit.get_unit_traits()
    unit.get_unit_actions()

    # Name and Description
    try:
        embed = discord.Embed(title=unit.name, description=unit.description)
    except AttributeError:
        embed = discord.Embed(title=unit.name)

    # Color
    embed.colour = GLADIUS_FACTION_COLORS[unit.faction]

    # Faction
    embed.add_field(name="Faction", value=camel_case_split(unit.faction), inline=False)

    # Cost
    costText = [GLADIUS_ICONS['production'], ' ', unit.resourceStats.productionCost]
    for resource in GLADIUS_RESOURCES:
        cost = resource + 'Cost'
        costValue = getattr(unit.resourceStats, cost)
        if costValue != '0':
            costText.extend((' | ', GLADIUS_ICONS[resource], ' ', costValue))
    embed.add_field(name="Cost", value=''.join(costText))
    
    # Upkeep
    upkeepText = []
    for resource in GLADIUS_RESOURCES:
        upkeep = resource + 'Upkeep'
        upkeepValue = getattr(unit.resourceStats, upkeep)
        if upkeepValue != '0':
            upkeepText.extend((' | ', GLADIUS_ICONS[resource], ' ', upkeepValue))
    try:
        # delete initial ' | '
        del upkeepText[0]
    except IndexError:
        pass
    if upkeepText == []:
        upkeepText = ['None']
    embed.add_field(name="Upkeep", value=''.join(upkeepText))

    # Stats
    statText = ('**', unit.combatStats.groupSizeMax, ' model(s)**\n',
                GLADIUS_ICONS['armor'], ' ', unit.combatStats.armor, ' | ', GLADIUS_ICONS['hitpoints'], ' ', unit.combatStats.hitpointsMax, ' | ',
                GLADIUS_ICONS['morale'], ' ', unit.combatStats.moraleMax, '\n', GLADIUS_ICONS['movement'], ' ', unit.combatStats.movementMax, ' | ',
                GLADIUS_ICONS['cargoSlots'], ' ', unit.combatStats.cargoSlots, ' | ', GLADIUS_ICONS['itemSlots'], ' ', unit.combatStats.itemSlots)
    embed.add_field(name="Stats", value=''.join(statText))

    # Weapons
    weaponsText = []
    for weapon in unit.weapons:
        # if upgrade required
        if unit.weapons[weapon][1]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        # if weapon is secondary
        if unit.weapons[weapon][2] == "0":
            secondary = ' (S)'
        else:
            secondary = ''
        weaponsText.extend((unit.weapons[weapon][0], 'x ', weapon.name, upgrade, secondary, '\n'))
    if weaponsText == []:
        weaponsText = ['None']
    embed.add_field(name='Weapons', value=''.join(weaponsText))

    # Traits
    traitsText = []
    for trait in unit.traits:
        # if upgrade required
        if unit.traits[trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText))

    # Actions
    actionsText = []
    for action in unit.actions:
        # if upgrade required
        if unit.actions[action]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        actionsText.extend((action, upgrade, '\n'))
    if actionsText == []:
        actionsText = ['None']
    embed.add_field(name='Actions', value=''.join(actionsText))
    
    if verbose:
        # Flavor
        try:
            embed.add_field(name='Flavor', value='*' + unit.flavor + '*', inline=False)
        except AttributeError:
            pass
        embed.set_footer(text=('Traits/weapons marked with (U) require a researchable upgrade.\n'
                                'Weapons marked with (S) are secondary weapons.\n'
                                'Stat-changing traits like Fleet not taken into account.'))
    
    return embed

def create_zunit_embed(unit: ZUnit, verbose: bool) -> discord.Embed:
    unit.get_branch()
    unit.get_unit_stats()
    unit.get_unit_weapons()
    unit.get_unit_traits()
    unit.get_unit_actions()

    # Name and Description
    try:
        embed = discord.Embed(title=unit.name, description=unit.description)
    except AttributeError:
        embed = discord.Embed(title=unit.name)

    # Color
    embed.colour = ZEPHON_BRANCH_COLORS[unit.branch]

    # Branch
    embed.add_field(name="Branch", value=unit.branch, inline=False)

    # Cost
    costText = [ZEPHON_ICONS['production'], ' ', unit.resourceStats.productionCost]
    for resource in ZEPHON_RESOURCES:
        cost = resource + 'Cost'
        costValue = getattr(unit.resourceStats, cost)
        if costValue != '0':
            costText.extend((' | ', ZEPHON_ICONS[resource], ' ', costValue))
    embed.add_field(name="Cost", value=''.join(costText))
    
    # Upkeep
    upkeepText = []
    for resource in ZEPHON_RESOURCES:
        upkeep = resource + 'Upkeep'
        upkeepValue = getattr(unit.resourceStats, upkeep)
        if upkeepValue != '0':
            upkeepText.extend((' | ', ZEPHON_ICONS[resource], ' ', upkeepValue))
    try:
        # delete initial ' | '
        del upkeepText[0]
    except IndexError:
        pass
    if upkeepText == []:
        upkeepText = ['None']
    embed.add_field(name="Upkeep", value=''.join(upkeepText))

    # Stats
    statText = (ZEPHON_ICONS['groupSize'], ' ', unit.combatStats.groupSizeMax, ' | ', ZEPHON_ICONS['accuracy'], ' ', unit.combatStats.accuracy, '\n',
                ZEPHON_ICONS['armor'], ' ', unit.combatStats.armor, ' | ', ZEPHON_ICONS['hitpoints'], ' ', unit.combatStats.hitpointsMax, ' | ',
                ZEPHON_ICONS['morale'], ' ', unit.combatStats.moraleMax, '\n', ZEPHON_ICONS['movement'], ' ', unit.combatStats.movementMax, ' | ',
                ZEPHON_ICONS['cargoSlots'], ' ', unit.combatStats.cargoSlots, ' | ', ZEPHON_ICONS['itemSlots'], ' ', unit.combatStats.itemSlots)
    embed.add_field(name="Stats", value=''.join(statText))

    # Weapons
    weaponsText = []
    for weapon in unit.weapons:
        # if upgrade required
        if unit.weapons[weapon][1]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        # if weapon is secondary
        if unit.weapons[weapon][2] == "0":
            secondary = ' (S)'
        else:
            secondary = ''
        weaponsText.extend((unit.weapons[weapon][0], 'x ', weapon.name, upgrade, secondary, '\n'))
    if weaponsText == []:
        weaponsText = ['None']
    embed.add_field(name='Weapons', value=''.join(weaponsText))

    # Traits
    traitsText = []
    for trait in unit.traits:
        # if upgrade required
        if unit.traits[trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText))

    # Actions
    actionsText = []
    for action in unit.actions:
        # if upgrade required
        if unit.actions[action]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        actionsText.extend((action, upgrade, '\n'))
    if actionsText == []:
        actionsText = ['None']
    embed.add_field(name='Actions', value=''.join(actionsText))
    
    if verbose:
        # Flavor
        try:
            embed.add_field(name='Flavor', value='*' + unit.flavor + '*', inline=False)
        except AttributeError:
            pass
        embed.set_footer(text=('Traits/weapons marked with (U) require a researchable upgrade.\n'
                                'Weapons marked with (S) are secondary weapons.\n'
                                'Stat-changing traits like Fleet not taken into account.'))
    
    return embed

def create_gweapon_embed(weapon: GWeapon, verbose: bool, unit: GUnit = None) -> discord.Embed:
    if unit:
        unit.get_unit_weapon_stats()
        weapon.unitStats = unit.weaponStats

    weapon.get_weapon_traits()
    weapon.get_weapon_range()
    weapon.get_weapon_stats()

    # Name and Description
    try:
        embed = discord.Embed(title=weapon.name, description=weapon.description)
    except AttributeError:
        embed = discord.Embed(title=weapon.name)

    # Wielder
    if unit:
        embed.add_field(name='Wielder', value=unit.name, inline=False)

    # Stats
    statText = (GLADIUS_ICONS['damage'], ' ', weapon.damage, ' | ', GLADIUS_ICONS['attacks'], ' ', weapon.attacks, ' | ',
                GLADIUS_ICONS['armorPenetration'], ' ', weapon.armorPen, ' | ', GLADIUS_ICONS['accuracy'], ' ', weapon.accuracy, ' | ',
                GLADIUS_ICONS['range'], ' ', weapon.range)
    embed.add_field(name="Stats", value=''.join(statText))

    # Traits
    traitsText = []
    for trait in weapon.traits:
        # if upgrade required
        if weapon.traits[trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText), inline=False)

    if verbose:
        # Flavor
        try:
            embed.add_field(name='Flavor', value='*' + weapon.flavor + '*', inline=False)
        except AttributeError:
            pass
        embed.set_footer(text=('Traits marked with (U) require a researchable upgrade.\n'
                                'Weapon stats depend on the unit wielding the weapon. Stat-changing traits like Twin-Linked not taken into account. '
                                'Values shown may not be accurate.'))

    return embed

def create_zweapon_embed(weapon: ZWeapon, verbose: bool, unit: ZUnit = None) -> discord.Embed:
    if unit:
        unit.get_unit_accuracy()
        weapon.accuracy = unit.combatStats.accuracy

    weapon.get_weapon_traits()
    weapon.get_weapon_range()
    weapon.get_weapon_stats()

    # Name and Description
    try:
        embed = discord.Embed(title=weapon.name, description=weapon.description)
    except AttributeError:
        embed = discord.Embed(title=weapon.name)

    # Stats
    statText = (ZEPHON_ICONS['damage'], ' ', weapon.damage, ' | ', ZEPHON_ICONS['attacks'], ' ', weapon.attacks, ' | ',
                ZEPHON_ICONS['armorPenetration'], ' ', weapon.armorPen, ' | ', ZEPHON_ICONS['accuracy'], ' ', weapon.accuracy, ' | ',
                ZEPHON_ICONS['range'], ' ', weapon.range)
    embed.add_field(name="Stats", value=''.join(statText))

    # Traits
    traitsText = []
    for trait in weapon.traits:
        # if upgrade required
        if weapon.traits[trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name="Traits", value=''.join(traitsText), inline=False)

    if verbose:
        # Flavor
        try:
            embed.add_field(name='Flavor', value='*' + weapon.flavor + '*', inline=False)
        except AttributeError:
            pass
        embed.set_footer(text=('Traits marked with (U) require a researchable upgrade.\n'
                                'Weapon stats depend on the unit wielding the weapon. Stat-changing traits like Twin-Linked not taken into account. '
                                'Values shown may not be accurate.'))
    
    return embed

def create_gtrait_embed(trait: GTrait, verbose: bool) -> discord.Embed:
    trait.get_trait_modifiers()

    # Name and Description
    try:
        embed = discord.Embed(title=trait.name, description=trait.description)
    except AttributeError:
        embed = discord.Embed(title=trait.name)

    # Color
    try:
        embed.colour = GLADIUS_FACTION_COLORS[trait.faction]
    except (AttributeError, KeyError):
        embed.colour = GLADIUS_FACTION_COLORS['Neutral']

    # Faction
    embed.add_field(name="Faction", value=camel_case_split(trait.faction))

    if verbose:
        # Modifiers
        try:
            embed.add_field(name='Modifiers', value=trait.modifiers, inline=False)
        except AttributeError:
            pass

        # Flavor
        try:
            embed.add_field(name='Flavor', value='*' + trait.flavor + '*', inline=False)
        except AttributeError:
            pass
    
    return embed

def create_ztrait_embed(trait: ZTrait, verbose: bool) -> discord.Embed:
    trait.get_trait_modifiers()

    # Name and Description
    try:
        embed = discord.Embed(title=trait.name, description=trait.description)
    except AttributeError:
        embed = discord.Embed(title=trait.name)

    if verbose:
        # Modifiers
        try:
            embed.add_field(name='Modifiers', value=trait.modifiers, inline=False)
        except AttributeError:
            pass

        # Flavor
        try:
            embed.add_field(name='Flavor', value='*' + trait.flavor + '*', inline=False)
        except AttributeError:
            pass

    return embed

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    synced = await client.tree.sync()
    print("# CMDs synced: " + str(len(synced)))

@client.tree.command(name='gitem', description='Return info on a Gladius item')
async def gitem(interaction: discord.Interaction, itemname:str, verbose:bool=False, invisible:bool=False):
    await return_info(interaction, itemname, verbose, invisible, 'Gladius', GItem, create_gitem_embed)

@client.tree.command(name='zitem', description='Return info on a Zephon item')
async def gitem(interaction: discord.Interaction, itemname:str, verbose:bool=False, invisible:bool=False):
    await return_info(interaction, itemname, verbose, invisible,'Zephon', ZItem, create_zitem_embed)

@client.tree.command(name='gunit', description='Return info on a Gladius unit')
async def gunit(interaction: discord.Interaction, unitname:str, verbose:bool=False, invisible:bool=False):
    await return_info(interaction, unitname, verbose, invisible, 'Gladius', GUnit, create_gunit_embed)

@client.tree.command(name='zunit', description='Return info on a Zephon unit')
async def gunit(interaction: discord.Interaction, unitname:str, verbose:bool=False, invisible:bool=False):
    await return_info(interaction, unitname, verbose, invisible, 'Zephon', ZUnit, create_zunit_embed)

@client.tree.command(name='gweapon', description='Return info on a Gladius weapon. Optionally include unit name for more accurate info.')
async def gweapon(interaction: discord.Interaction, weaponname:str, unitname:str='', verbose:bool=False, invisible:bool=False):
    await return_info(interaction, weaponname, verbose, invisible, 'Gladius', GWeapon, create_gweapon_embed, unitname)

@client.tree.command(name='zweapon', description='Return info on a Zephon weapon. Optionally include unit name for more accurate info.')
async def zweapon(interaction: discord.Interaction, weaponname:str, unitname:str='', verbose:bool=False, invisible:bool=False):
    await return_info(interaction, weaponname, verbose, invisible, 'Zephon', ZWeapon, create_zweapon_embed, unitname)
    weapon = ZWeapon(weaponname, 'Zephon', 'Weapons')
    weapon.fuzzy_match_name(weapon.get_obj_info)
    if not weapon.found:
        markdown = '**'
        await interaction.response.send_message(markdown + weaponname + markdown + ' not found. Did you mean ' + markdown + weapon.bestMatch + markdown + '?')
    else:
        weapon.get_icon_path()
        weapon.get_weapon_traits()
        weapon.get_weapon_range()
        weapon.get_weapon_stats()

        # Name and Description
        try:
            embed = discord.Embed(title=weapon.name, description=weapon.description)
        except AttributeError:
            embed = discord.Embed(title=weapon.name)

        # Stats
        statText = (ZEPHON_ICONS['damage'], ' ', weapon.damage, ' | ', ZEPHON_ICONS['attacks'], ' ', weapon.attacks, ' | ',
                    ZEPHON_ICONS['armorPenetration'], ' ', weapon.armorPen, ' | ', ZEPHON_ICONS['accuracy'], ' ', weapon.accuracy, ' | ',
                    ZEPHON_ICONS['range'], ' ', weapon.range)
        embed.add_field(name="Stats", value=''.join(statText))

        # Traits
        traitsText = []
        for trait in weapon.traits:
            # if upgrade required
            if weapon.traits[trait]:
                upgrade = ' (U)'
            else:
                upgrade = ''
            traitsText.extend((trait, upgrade, '\n'))
        if traitsText == []:
            traitsText = ['None']
        embed.add_field(name="Traits", value=''.join(traitsText), inline=False)

        # Flavor
        try:
            embed.add_field(name='Flavor', value='*' + weapon.flavor + '*', inline=False)
        except AttributeError:
            pass
        embed.set_footer(text=('Traits marked with (U) require a researchable upgrade.\n'
                               'Weapon stats depend on the unit wielding the weapon. Stat-changing traits like Twin-Linked not taken into account. '
                               'Values shown may not be accurate.'))

        # Thumbnail
        await interaction.response.send_message(**get_thumbnail(embed, weapon))

@client.tree.command(name='gtrait', description='Return info on a Gladius trait')
async def gtrait(interaction: discord.Interaction, traitname:str, verbose:bool=False, invisible:bool=False):
    await return_info(interaction, traitname, verbose, invisible, 'Gladius', GTrait, create_gtrait_embed)

@client.tree.command(name='ztrait', description='Return info on a Zephon trait')
async def ztrait(interaction: discord.Interaction, traitname:str, verbose:bool=False, invisible:bool=False):
    await return_info(interaction, traitname, verbose, invisible, 'Zephon', ZTrait, create_ztrait_embed)

client.run(TOKEN)
