import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from lxml import etree as ET
from thefuzz import fuzz
from dataclasses import dataclass

load_dotenv()
TOKEN = os.getenv("TEST_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)

class Obj():
    def __init__(self, name: str, game: str, objClass: str):
        self.name: str = name.casefold()
        self.game: str = game
        self.objClass: str = objClass
        self.englishDir: str = './' + game + '/English/'
        self.classDir: str = './' + game + '/' + objClass + '/'
        self.classXMLpath: str = self.englishDir + objClass + '.xml'
        self.found: bool = False
        self.bestMatch: str = ''
        self.internalID: str = ''
        self.XMLPath: str = ''
        self.tree: object
        self.iconPath: str = ''
        self.description: str = ''
        self.flavor: str = ''

    def fuzzy_match_name(self, typeFunc):
        tree = ET.parse(self.classXMLpath, parser=ET.XMLParser(recover=True, remove_comments=True))
        bestRatio = 0
        xmlTree = tree.getroot()
        for entry in xmlTree.iterdescendants('entry'):
            targetStr = entry.get('value')
            if targetStr.casefold() == self.name:
                self.found = True
                self.name = targetStr
                typeFunc(xmlTree, entry)
            elif 'Flavor' not in entry.get('name') and 'Description' not in entry.get('name'):
                fuzzRatio = fuzz.token_sort_ratio(targetStr.casefold(), self.name)
                if fuzzRatio > bestRatio:
                    bestRatio = fuzzRatio
                    self.bestMatch = targetStr

    def get_obj_info(self, xmlTree, entry):
        self.internalID = entry.get('name')
        self.XMLPath = self.classDir + self.internalID + '.xml'
        self.tree = ET.parse(self.XMLPath)
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.internalID + 'Flavor':
                self.flavor = val2val(e.get('value'), self.englishDir)
            elif self.game == 'Gladius':
                if targetStr == self.internalID + 'Description':
                    self.description = val2val(e.get('value'), self.englishDir)
            elif self.game == 'Zephon':
                if targetStr == self.internalID + 'Properties':
                    self.description = val2val(e.get('value'), self.englishDir).replace("<icon texture='GUI/Bullet'/>", '')

    def get_icon(self):
        self.iconPath = self.tree.getroot().get('icon')

    @classmethod
    def from_internalID(cls, internalID: str, game: str, objClass: str):
        obj = cls('placeholder', game, objClass)
        obj.internalID = internalID
        #IDlen = len(internalID)
        tree = ET.parse(obj.classXMLpath, parser=ET.XMLParser(recover=True, remove_comments=True))
        xmlTree = tree.getroot()
        for entry in xmlTree.iterdescendants('entry'):
            targetStr = entry.get('name')
            if targetStr == internalID:
                obj.found = True
                obj.name = val2val(entry.get('value'), obj.englishDir)
                return obj

class Item(Obj):
    def __init__(self, name: str, game: str, objClass: str):
        super().__init__(name, game, objClass)
        self.rarity: str = 'Common'
        self.influenceCost: int = 0

    def get_item_rarity(self):
        trait = self.tree.find('traits')
        if trait != None:
            self.rarity = trait.find('trait').get('name')

    def get_item_influence_cost(self):
        self.influenceCost = self.tree.find('modifiers').find('modifier').find('effects').find('influenceCost').get('base')

@dataclass
class CombatStats:
    __slots__ = ['groupSizeMax', 'armor', 'hitpointsMax', 'moraleMax',
                 'movementMax', 'cargoSlots', 'itemSlots']
    groupSizeMax: str
    armor: str
    hitpointsMax: str
    moraleMax: str
    movementMax: str
    cargoSlots: str
    itemSlots: str

@dataclass
class GResourceStats:
    __slots__ = ['biomassUpkeep', 'biomassCost', 'requisitionsUpkeep', 'requisitionsCost',
                 'foodUpkeep', 'foodCost', 'oreUpkeep', 'oreCost',
                 'energyUpkeep', 'energyCost', 'influenceUpkeep', 'influenceCost', 'productionCost']
    biomassUpkeep: str
    biomassCost: str
    requisitionsUpkeep: str
    requisitionsCost: str
    foodUpkeep: str
    foodCost: str
    oreUpkeep: str
    oreCost: str
    energyUpkeep: str
    energyCost: str
    influenceUpkeep: str
    influenceCost: str
    productionCost: str

@dataclass
class ZResourceStats:
    __slots__ = ['foodUpkeep', 'foodCost', 'mineralsUpkeep', 'mineralsCost',
                 'energyUpkeep', 'energyCost', 'transuraniumUpkeep', 'transuraniumCost',
                 'antimatterUpkeep', 'antimatterCost', 'dimensionalEchoesUpkeep', 'dimensionalEchoesCost',
                 'singularityCoresUpkeep', 'singularityCoresCost', 'algaeUpkeep', 'algaeCost',
                 'chipsUpkeep', 'chipsCost', 'influenceUpkeep', 'influenceCost', 'productionCost']
    foodUpkeep: str
    foodCost: str
    mineralsUpkeep: str
    mineralsCost: str
    energyUpkeep: str
    energyCost: str
    transuraniumUpkeep: str
    transuraniumCost: str
    antimatterUpkeep: str
    antimatterCost: str
    dimensionalEchoesUpkeep: str
    dimensionalEchoesCost: str
    singularityCoresUpkeep: str
    singularityCoresCost: str
    algaeUpkeep: str
    algaeCost: str
    chipsUpkeep: str
    chipsCost: str
    influenceUpkeep: str
    influenceCost: str
    productionCost: str

class Unit(Obj):
    def __init__(self, name: str, game: str, objClass: str):
        super().__init__(name, game, objClass)
        # Stats
        self.resourceStats: dataclass
        self.combatStats: dataclass = CombatStats(*['0']*len(CombatStats.__slots__))
        #Weapons and traits
        self.weapons: dict = {}
        self.traits: dict = {}

    def get_unit_stats(self):
        xmlStats = self.tree.find('modifiers').find('modifier').find('effects')
        for stat in self.resourceStats.__slots__:
            statEntry = xmlStats.find(stat)
            if statEntry is not None:
                setattr(self.resourceStats, stat, statEntry.get('base', default='0'))
        for stat in self.combatStats.__slots__:
            statEntry = xmlStats.find(stat)
            if statEntry is not None:
                setattr(self.combatStats, stat, statEntry.get('base', default='0'))

    def get_unit_weapons(self):
        try:    
            for weapon in self.tree.find('weapons').iterfind('weapon'):
                if self.game == 'Gladius':
                    weaponName = weapon.get('name')
                elif self.game == 'Zephon':
                    weaponName = weapon.get('type')
                if weaponName == 'None':
                    continue
                weaponObj = Weapon.from_internalID(weaponName, self.game, 'Weapons')
                # {weaponObj:(weaponCount, requiredUpgrade, enabled), ...}
                self.weapons[weaponObj] = (weapon.get('count', default='1'), weapon.get('requiredUpgrade'), weapon.get('enabled', default="1"))
        # no weapons
        except AttributeError:
            pass

    def get_unit_traits(self):
        try:
            for trait in self.tree.find('traits').iterfind('trait'):
                if self.game == 'Gladius':
                    traitName = trait.get('name')
                elif self.game == 'Zephon':
                    traitName = trait.get('type')
                traitObj = Trait.from_internalID(traitName, self.game, 'Traits')
                self.traits[traitObj.name] = trait.get('requiredUpgrade')
        # no traits
        except AttributeError:
            pass

class GUnit(Unit):
    def __init__(self, name: str, game: str, objClass: str):
        super().__init__(name, game, objClass)
        self.resourceStats = GResourceStats(*['0']*len(GResourceStats.__slots__))
        self.factionAndID: str
        self.faction: str = 'Neutral'

    def get_obj_info(self, xmlTree, entry):
        self.factionAndID = entry.get('name')
        try:
            self.faction, self.internalID = self.factionAndID.split('/')
        # only for Neutral/Artefacts/unit.xml
        except ValueError:
            self.faction, self.internalID = self.factionAndID.split('/')[0], self.factionAndID.split('/')[-1] 
        self.XMLPath = self.classDir + self.factionAndID + '.xml'
        self.tree = ET.parse(self.XMLPath)
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.factionAndID + 'Description':
                self.description = e.get('value')
            elif targetStr == self.factionAndID + 'Flavor':
                self.flavor = e.get('value')

    def get_unit_count(self):
        groupEntry = self.tree.find('group')
        if groupEntry is None:
            self.combatStats.groupSizeMax = '1'
        else:
            self.combatStats.groupSizeMax = groupEntry.get('size')

class ZUnit(Unit):
    def __init__(self, name: str, game: str, objClass: str):
        super().__init__(name, game, objClass)
        self.resourceStats = ZResourceStats(*['0']*len(ZResourceStats.__slots__))
        self.branch: str

    def get_unit_branch(self):
        self.branch = self.tree.getroot().get('branch')

class Weapon(Obj):
    def __init__(self, name: str, game: str, objClass: str):
        super().__init__(name, game, objClass)
        self.attacks = '1'
        self.armorPen = '0'
        self.damage = '1'
        self.range = '?'
        self.accuracy = '6'
        self.traits: dict = {}
    
    def get_weapon_traits(self):
        try:
            for trait in self.tree.find('traits').iterfind('trait'):
                traitObj = Trait.from_internalID(trait.get('name'), self.game, 'Traits')
                self.traits[traitObj.name] = trait.get('requiredUpgrade')
        # no traits
        except AttributeError:
            pass

    def get_weapon_range(self):
        if 'Melee' in self.traits.keys():
            self.range = 'Melee'
        else:
            rangeMin = self.tree.find('target').get('rangeMin')
            rangeMax = self.tree.find('target').get('rangeMax')
            if rangeMin != None:
                self.range = str(rangeMin) + ' - ' + str(rangeMax)
            else:
                self.range = rangeMax

    def get_weapon_stats(self):
        try:
            effects = self.tree.find('modifiers').find('modifier').find('effects')
        except AttributeError:
            return
        if 'Melee' in self.traits.keys():
            prefix = 'melee'
        else:
            prefix = 'ranged'
        try:
            self.attacks = effects.find('attacks').items()[0][1]
        except AttributeError:
            pass
        try:
            self.armorPen = effects.find(prefix + 'ArmorPenetration').items()[0][1]
        except AttributeError:
            pass
        try:
            if prefix == 'melee':
                operator, strengthDamage = effects.find('strengthDamage').items()[0]
                if operator != 'base':
                    strengthDamage = str(float(strengthDamage) + 1)
                self.damage = strengthDamage
                self.damage = str(float(self.damage) + float(effects.find('meleeDamage').items()[0][1]))
            else:
                self.damage = effects.find(prefix + 'Damage').items()[0][1]
        except AttributeError:
            pass
        try:
            self.accuracy = effects.find(prefix + 'Accuracy').items()[0][1]
        except AttributeError:
            pass

class Trait(Obj):
    def __init__(self, name: str, game: str, objClass: str):
        super().__init__(name, game, objClass)
        self.factionAndID: str
        self.faction: str = 'Neutral'

    def get_obj_info(self, xmlTree, entry):
        self.factionAndID = entry.get('name')
        if '/' in self.factionAndID:
            self.faction, self.internalID = self.factionAndID.split('/')
        else:
            self.internalID = self.factionAndID
        self.XMLPath = self.classDir + self.factionAndID + '.xml'
        self.tree = ET.parse(self.XMLPath)
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.factionAndID + 'Description':
                self.description = val2val(e.get('value'), self.englishDir)
            elif targetStr == self.factionAndID + 'Flavor':
                self.flavor = val2val(e.get('value'), self.englishDir)

class ZTrait(Obj):
    def __init__(self, name: str, game: str, objClass: str):
        super().__init__(name, game, objClass)

def val2val(value: str, englishDir: str) -> str:
    if '<string name=' in value:
        path = value[14:-3]
        file, name = path.split('/', 1)
        tree = ET.parse(englishDir + file + '.xml', parser=ET.XMLParser(recover=True, remove_comments=True))
        xmlTree = tree.getroot()
        for entry in xmlTree.iterdescendants('entry'):
            if entry.get('name') == name:
                return entry.get('value')
    else:
        return value

def camel_case_split(s: str) -> str:
    # use map to add an underscore before each uppercase letter
    modified_string = list(map(lambda x: '_' + x if x.isupper() else x, s))
    # join the modified string and split it at the underscores
    split_string = ''.join(modified_string).split('_')
    # remove any empty strings from the list
    # split_string = list(filter(lambda x: x != '', split_string))
    split_string = ' '.join(split_string)
    return split_string

rarityColors = {'Common':discord.colour.Color.from_rgb(255, 255, 255),
                'Uncommon':discord.colour.Color.from_rgb(0, 191, 191),
                'Artefact':discord.colour.Color.from_rgb(191, 0, 191)}
gFactionColors = {'AdeptusMechanicus':discord.colour.Color.from_rgb(159, 38, 40),
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
zBranchColors = {'Cyber':discord.colour.Color.from_rgb(16, 121, 130),
                 'Human':discord.colour.Color.from_rgb(154, 129, 35),
                 'Voice':discord.colour.Color.from_rgb(123, 65, 150),
                 'Zephon':discord.colour.Color.from_rgb(205, 59, 66),
                 'Reaver':discord.colour.Color.from_rgb(138, 97, 70),
                 'Acrin':discord.colour.Color.from_rgb(62, 192, 158)}
gIcons = {'biomass':'<:Biomass:1240218802831233118>', 'requisitions':'<:Requisitions:1240222555588268032>',
                'food':'<:Food:1240218818660532317>', 'ore':'<:Ore:1240218839644377181>',
                'energy':'<:Energy:1240221846343782501>', 'influence':'<:Influence:1240218825836728341>',
                'production':'<:Production:1240330971514011668>',
                
                'armor':'<:Armor:1240218799832174703>', 'hitpoints':'<:Hitpoints:1240330759781482528>',
                'morale':'<:Morale:1240218836171493386>', 'movement':'<:Movement:1240222322770579487>',
                'cargoSlots':'<:CargoSlots:1240218804982775848>', 'itemSlots':'<:ItemSlots:1240218829280378912>',
                
                'damage':'<:Damage:1240218813123919893>', 'attacks':'<:Attacks:1240218801799434241>',
                'armorPenetration':'<:ArmorPenetration:1240218800855715840>', 'accuracy':'<:Accuracy:1240218797458063361>',
                'range':'<:Range:1240218850763477013>'}
zIcons = {'food':'<:Food:1250986007537647687>', 'minerals':'<:Minerals:1250986099023806464>',
                'energy':'<:Energy:1250985795242954764>', 'influence':'<:Influence:1250986095739404339>',
                'algae':'<:Algae:1250981089540046929>', 'chips':'<:Chips:1250985791455494174>',
                'antimatter':'<:Antimatter:1250981090278117416>', 'singularityCores':'<:SingularityCores:1250986245085986909>',
                'transuranium':'<:Transuranium:1250986247086669937>', 'production':'<:Production:1250986164626657383>',
                
                'armor':'<:Armor:1250981091125362788>', 'hitpoints':'<:Hitpoints:1250986009429282866>',
                'morale':'<:Morale:1250986099816530033>', 'movement':'<:Movement:1250986100621836400>',
                'cargoSlots':'<:CargoSlots:1250981096070582273>', 'itemSlots':'<:ItemSlots:1250986096616017961>',
                
                'damage':'<:Damage:1250985792197628004>', 'attacks':'<:Attacks:1250981093314662411>',
                'armorPenetration':'<:ArmorPenetration:1250981091917955193>', 'accuracy':'<:Accuracy:1250981087954468914>',
                'range':'<:Range:1250986241604849664>'}
gResources = ('biomass', 'requisitions', 'food', 'ore', 'energy', 'influence')
zResources = ('food', 'minerals', 'energy', 'transuranium', 'antimatter', 'dimensionalEchoes', 'singularityCores', 'algae', 'chips', 'influence')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    synced = await client.tree.sync()
    print("# CMDs synced: " + str(len(synced)))

@client.tree.command(name='gitem', description='Return info on a Gladius item')
async def gitem(interaction: discord.Interaction, itemname:str):
    item = Item(itemname, 'Gladius', 'Items')
    item.fuzzy_match_name(item.get_obj_info)
    if not item.found:
        markdown = '**'
        await interaction.response.send_message(markdown + itemname + markdown + ' not found. Did you mean ' + markdown + item.bestMatch + markdown + '?')
    else:
        item.get_icon()
        item.get_item_rarity()
        item.get_item_influence_cost()

        # Name and Description
        embed = discord.Embed(title=item.name, description=item.description)

        # Color
        embed.colour = rarityColors[item.rarity]

        # Rarity
        embed.add_field(name="Rarity", value=item.rarity)

        # Influence cost
        embed.add_field(name="Cost", value=gIcons['influence'] + ' ' + item.influenceCost)

        # Flavor
        if item.flavor != '':
            embed.add_field(name='Flavor', value='*' + item.flavor + '*')

        # Thumbnail
        try:
            if item.iconPath:
                image = discord.File('./Gladius/Icons/' + item.iconPath + '.png', filename='icon.png')
            else:
                image = discord.File('./Gladius/Icons/Items/' + item.internalID + '.png', filename='icon.png')
            embed.set_thumbnail(url="attachment://icon.png")
            await interaction.response.send_message(file=image, embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message(embed=embed)

@client.tree.command(name='gunit', description='Return info on a Gladius unit')
async def gunit(interaction: discord.Interaction, unitname:str):
    unit = GUnit(unitname, 'Gladius', 'Units')
    unit.fuzzy_match_name(unit.get_obj_info)
    if not unit.found:
        markdown = '**'
        await interaction.response.send_message(markdown + unitname + markdown + ' not found. Did you mean ' + markdown + unit.bestMatch + markdown + '?')
    else:
        unit.get_icon()
        unit.get_unit_stats()
        unit.get_unit_count()
        unit.get_unit_weapons()
        unit.get_unit_traits()

        # Name and Description
        embed = discord.Embed(title=unit.name, description=unit.description)

        # Color
        embed.colour = gFactionColors[unit.faction]

        # Faction
        embed.add_field(name="Faction", value=camel_case_split(unit.faction))

        # Cost
        costText = [gIcons['production'], ' ', unit.resourceStats.productionCost]
        for resource in gResources:
            cost = resource + 'Cost'
            costValue = getattr(unit.resourceStats, cost)
            if costValue != '0':
                costText.extend((' | ', gIcons[resource], ' ', costValue))
        embed.add_field(name="Cost", value=''.join(costText))
        
        # Upkeep
        upkeepText = []
        for resource in gResources:
            upkeep = resource + 'Upkeep'
            upkeepValue = getattr(unit.resourceStats, upkeep)
            if upkeepValue != '0':
                upkeepText.extend((' | ', gIcons[resource], ' ', upkeepValue))
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
                    gIcons['armor'], ' ', unit.combatStats.armor, ' | ', gIcons['hitpoints'], ' ', unit.combatStats.hitpointsMax, ' | ',
                    gIcons['morale'], ' ', unit.combatStats.moraleMax, '\n', gIcons['movement'], ' ', unit.combatStats.movementMax, ' | ',
                    gIcons['cargoSlots'], ' ', unit.combatStats.cargoSlots, ' | ', gIcons['itemSlots'], ' ', unit.combatStats.itemSlots)
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
        embed.add_field(name="Weapons", value=''.join(weaponsText))

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
        embed.add_field(name="Traits", value=''.join(traitsText), inline=False)
        
        # Flavor
        if unit.flavor != '':
            embed.add_field(name='Flavor', value='*' + unit.flavor + '*')
        #embed.set_footer(text=unit.flavor)
        embed.set_footer(text=('Traits/weapons marked with (U) require a researchable upgrade.\n'
                               'Weapons marked with (S) are secondary weapons.\n'
                               'Stat-changing traits like Fleet not taken into account.'))

        # Thumbnail
        try:
            if unit.iconPath:
                image = discord.File('./Gladius/Icons/' + unit.iconPath + '.png', filename='icon.png')
            else:
                image = discord.File('./Gladius/Icons/Units/' + unit.factionAndID + '.png', filename='icon.png')
            embed.set_thumbnail(url="attachment://icon.png")
            await interaction.response.send_message(file=image, embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message(embed=embed)

@client.tree.command(name='zunit', description='Return info on a Zephon unit')
async def gunit(interaction: discord.Interaction, unitname:str):
    unit = ZUnit(unitname, 'Zephon', 'Units')
    unit.fuzzy_match_name(unit.get_obj_info)
    if not unit.found:
        markdown = '**'
        await interaction.response.send_message(markdown + unitname + markdown + ' not found. Did you mean ' + markdown + unit.bestMatch + markdown + '?')
    else:
        unit.get_icon()
        unit.get_unit_branch()
        unit.get_unit_stats()
        unit.get_unit_weapons()
        unit.get_unit_traits()

        # Name and Description
        embed = discord.Embed(title=unit.name, description=unit.description)

        # Color
        embed.colour = zBranchColors[unit.branch]

        # Branch
        embed.add_field(name="Branch", value=unit.branch)

        # Cost
        costText = [zIcons['production'], ' ', unit.resourceStats.productionCost]
        for resource in zResources:
            cost = resource + 'Cost'
            costValue = getattr(unit.resourceStats, cost)
            if costValue != '0':
                costText.extend((' | ', zIcons[resource], ' ', costValue))
        embed.add_field(name="Cost", value=''.join(costText))
        
        # Upkeep
        upkeepText = []
        for resource in zResources:
            upkeep = resource + 'Upkeep'
            upkeepValue = getattr(unit.resourceStats, upkeep)
            if upkeepValue != '0':
                upkeepText.extend((' | ', zIcons[resource], ' ', upkeepValue))
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
                    zIcons['armor'], ' ', unit.combatStats.armor, ' | ', zIcons['hitpoints'], ' ', unit.combatStats.hitpointsMax, ' | ',
                    zIcons['morale'], ' ', unit.combatStats.moraleMax, '\n', zIcons['movement'], ' ', unit.combatStats.movementMax, ' | ',
                    zIcons['cargoSlots'], ' ', unit.combatStats.cargoSlots, ' | ', zIcons['itemSlots'], ' ', unit.combatStats.itemSlots)
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
        embed.add_field(name="Weapons", value=''.join(weaponsText))

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
        embed.add_field(name="Traits", value=''.join(traitsText), inline=False)
        
        # Flavor
        if unit.flavor != '':
            embed.add_field(name='Flavor', value='*' + unit.flavor + '*')
        #embed.set_footer(text=unit.flavor)
        embed.set_footer(text=('Traits/weapons marked with (U) require a researchable upgrade.\n'
                               'Weapons marked with (S) are secondary weapons.\n'
                               'Stat-changing traits like Fleet not taken into account.'))

        # Thumbnail
        try:
            if unit.iconPath:
                image = discord.File('./Zephon/Icons/' + unit.iconPath + '.png', filename='icon.png')
            else:
                image = discord.File('./Zephon/Icons/Units/' + unit.internalID + '.png', filename='icon.png')
            embed.set_thumbnail(url="attachment://icon.png")
            await interaction.response.send_message(file=image, embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message(embed=embed)

@client.tree.command(name='gweapon', description='Return info on a Gladius weapon')
async def gweapon(interaction: discord.Interaction, weaponname:str):
    weapon = Weapon(weaponname, 'Gladius', 'Weapons')
    weapon.fuzzy_match_name(weapon.get_obj_info)
    if not weapon.found:
        markdown = '**'
        await interaction.response.send_message(markdown + weaponname + markdown + ' not found. Did you mean ' + markdown + weapon.bestMatch + markdown + '?')
    else:
        weapon.get_icon()
        weapon.get_weapon_traits()
        weapon.get_weapon_range()
        weapon.get_weapon_stats()

        # Name and Description
        if weapon.description:
            embed = discord.Embed(title=weapon.name, description=weapon.description)
        else:
            embed = discord.Embed(title=weapon.name)

        # Stats
        statText = (gIcons['damage'], ' ', weapon.damage, ' | ', gIcons['attacks'], ' ', weapon.attacks, ' | ',
                    gIcons['armorPenetration'], ' ', weapon.armorPen, ' | ', gIcons['accuracy'], ' ', weapon.accuracy, ' | ',
                    gIcons['range'], ' ', weapon.range)
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
        if weapon.flavor != '':
            embed.add_field(name='Flavor', value='*' + weapon.flavor + '*')
        embed.set_footer(text=('Traits marked with (U) require a researchable upgrade.\n'
                               'Weapon stats depend on the unit wielding the weapon. Stat-changing traits like Twin-Linked not taken into account. '
                               'Values shown may not be accurate.'))

        # Thumbnail
        try:
            if weapon.iconPath:
                image = discord.File('./Gladius/Weapons/' + weapon.iconPath + '.png', filename='icon.png')
            else:
                image = discord.File('./Gladius/Icons/Weapons/' + weapon.internalID + '.png', filename='icon.png')
            embed.set_thumbnail(url="attachment://icon.png")
            await interaction.response.send_message(file=image, embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message(embed=embed)

@client.tree.command(name='gtrait', description='Return info on a Gladius trait')
async def gtrait(interaction: discord.Interaction, traitname:str):
    trait = Trait(traitname, 'Gladius', 'Traits')
    trait.fuzzy_match_name(trait.get_obj_info)
    if not trait.found:
        markdown = '**'
        await interaction.response.send_message(markdown + traitname + markdown + ' not found. Did you mean ' + markdown + trait.bestMatch + markdown + '?')
    else:
        trait.get_icon()

        # Name and Description
        embed = discord.Embed(title=trait.name, description=trait.description)        

        # Color
        embed.colour = gFactionColors[trait.faction]

        # Faction
        embed.add_field(name="Faction", value=camel_case_split(trait.faction))

        # Flavor
        if trait.flavor != '':
            embed.add_field(name='Flavor', value='*' + trait.flavor + '*')

        # Thumbnail
        try:
            if trait.iconPath:
                image = discord.File('./Gladius/Icons/' + trait.iconPath + '.png', filename='icon.png')
            else:
                image = discord.File('./Gladius/Icons/Traits/' + trait.factionAndID + '.png', filename='icon.png')
            embed.set_thumbnail(url="attachment://icon.png")
            await interaction.response.send_message(file=image, embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message(embed=embed)

@client.tree.command(name='ztrait', description='Return info on a Zephon trait')
async def ztrait(interaction: discord.Interaction, traitname:str):
    trait = ZTrait(traitname, 'Zephon', 'Traits')
    trait.fuzzy_match_name(trait.get_obj_info)
    if not trait.found:
        markdown = '**'
        await interaction.response.send_message(markdown + traitname + markdown + ' not found. Did you mean ' + markdown + trait.bestMatch + markdown + '?')
    else:
        trait.get_icon()

        # Name and Description
        embed = discord.Embed(title=trait.name, description=trait.description)   

        # Flavor
        if trait.flavor != '':
            embed.add_field(name='Flavor', value='*' + trait.flavor + '*')

        # Thumbnail
        try:
            if trait.iconPath:
                image = discord.File('./Zephon/Icons/' + trait.iconPath + '.png', filename='icon.png')
            else:
                image = discord.File('./Zephon/Icons/Traits/' + trait.internalID + '.png', filename='icon.png')
            embed.set_thumbnail(url="attachment://icon.png")
            await interaction.response.send_message(file=image, embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message(embed=embed)

client.run(TOKEN)
