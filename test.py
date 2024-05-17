import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import xml.etree.ElementTree as ET
#from lxml import etree as ET
from thefuzz import fuzz
from dataclasses import dataclass

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents)
englishPath = './Gladius/English/'
englishUnitsXMLPath = './Gladius/English/Units.xml'
englishWeaponsXMLPath = './Gladius/English/Weapons.xml'
englishTraitsXMLPath = './Gladius/English/Traits.xml'

class Obj():
    def __init__(self, name: str):
        self.name = name.casefold()
        self.found = False
        self.bestMatch = ''
        self.internalID = ''
        self.XMLPath = ''

    def get_info_English(self, xmlPath: str, typeFunc):
        tree = ET.parse(xmlPath, parser=ET.XMLParser())
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

    @classmethod
    def from_internalID(cls, internalID: str, xmlPath: str):
        obj = cls('placeholder')
        obj.internalID = internalID
        #IDlen = len(internalID)
        tree = ET.parse(xmlPath, parser=ET.XMLParser())
        xmlTree = tree.getroot()
        for entry in xmlTree.iterdescendants('entry'):
            targetStr = entry.get('name')
            if targetStr == internalID:
                obj.found = True
                obj.name = entry.get('value')
                return obj

class Unit(Obj):
    def __init__(self, name: str):
        super().__init__(name)
        self.factionAndID: str
        self.faction: str = 'Neutral'
        self.description: str
        self.flavor: str
        # Stats
        self.groupSize: str = '1'
        self.armor: str = '0'
        self.biomassUpkeep: str = '0'
        self.biomassCost: str = '0'
        self.cargoSlots: str = '0'  
        self.energyUpkeep: str = '0'
        self.energyCost: str = '0'
        self.itemSlots: str = '0'
        self.foodUpkeep: str = '0'
        self.foodCost: str = '0'
        self.hitpointsMax: str = '0'
        self.influenceUpkeep: str = '0'
        self.influenceCost: str = '0'
        self.moraleMax: str = '0'
        self.movementMax: str = '3'
        self.oreUpkeep: str = '0'
        self.oreCost: str = '0'
        self.productionCost: str = '0'
        self.requisitionsUpkeep: str = '0'
        self.requisitionsCost: str = '0'
        #Weapons and traits
        self.weapons: dict = {}
        self.traits: dict = {}

    def get_unit_info(self, xmlTree, entry):
        self.factionAndID = entry.get('name')
        self.faction, self.internalID = self.factionAndID.split('/')
        self.XMLPath = './Gladius/Units/' + self.factionAndID + '.xml'
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.factionAndID + 'Description':
                self.description = e.get('value')
            elif targetStr == self.factionAndID + 'Flavor':
                self.flavor = e.get('value')

    def get_unit_stats(self):
        tree = ET.parse(self.XMLPath)
        xmlStats = tree.find('modifiers').find('modifier').find('effects')
        statStrings = ('armor', 'biomassUpkeep', 'biomassCost', 'cargoSlots', 'energyUpkeep', 'energyCost', 'itemSlots', 'foodUpkeep', 'foodCost', 
                       'hitpointsMax', 'influenceUpkeep', 'influenceCost', 'moraleMax', 'movementMax', 'oreUpkeep', 
                       'oreCost', 'productionCost', 'requisitionsUpkeep', 'requisitionsCost')
        for statString in statStrings:
            statEntry = xmlStats.find(statString)
            if statEntry is not None:
                setattr(self, statString, statEntry.get('base', default='0'))

    def get_unit_count(self):
        tree = ET.parse(self.XMLPath)
        groupEntry = tree.find('group')
        if groupEntry is None:
            self.groupSize = '1'
        else:
            self.groupSize = groupEntry.get('size')

    def get_unit_weapons(self):
        tree = ET.parse(self.XMLPath)
        for weapon in tree.find('weapons').iterfind('weapon'):
            if weapon.get('name') == 'None':
                continue
            weaponObj = Weapon.from_internalID(weapon.get('name'), englishWeaponsXMLPath)
            # {weaponObj:(weaponCount, requiredUpgrade, enabled), ...}
            self.weapons[weaponObj] = (weapon.get('count', default='1'), weapon.get('requiredUpgrade'), weapon.get('enabled', default="1"))

    def get_unit_traits(self):
        tree = ET.parse(self.XMLPath)
        for trait in tree.find('traits').iterfind('trait'):
            traitObj = Trait.from_internalID(trait.get('name'), englishTraitsXMLPath)
            self.traits[traitObj] = trait.get('requiredUpgrade')

class Weapon(Obj):
    def __init__(self, name: str):
        super().__init__(name)
        self.flavor: str

class Trait(Obj):
    def __init__(self, name: str):
        super().__init__(name)
        self.factionAndID: str
        self.faction: str = 'Neutral'
        self.description: str
        self.flavor: str

    def get_trait_info(self, xmlTree, entry):
        self.factionAndID = entry.get('name')
        if '/' in self.factionAndID:
            self.faction, self.internalID = self.factionAndID.split('/')
        else:
            self.internalID = self.factionAndID
        self.XMLPath = './Gladius/Units/' + self.factionAndID + '.xml'
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.factionAndID + 'Description':
                self.description = val2val(e.get('value'))
            elif targetStr == self.factionAndID + 'Flavor':
                self.flavor = val2val(e.get('value'))

def val2val(value: str) -> str:
    if '<string name=' in value:
        path = ET.fromstring(value).get('name')
        file, name = path.split('/', 1)
        tree = ET.parse(englishPath + file + '.xml', parser=ET.XMLParser(recover=True, remove_comments=True))
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


factionColors = {'AdeptusMechanicus':discord.colour.Color.from_rgb(159, 38, 40),
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
icons = {'biomassUpkeep':'<:Biomass:1240218802831233118>', 'biomassCost':'<:Biomass:1240218802831233118>',
         'requisitionsUpkeep':'<:Requisitions:1240222555588268032>', 'requisitionsCost':'<:Requisitions:1240222555588268032>',
         'foodUpkeep':'<:Food:1240218818660532317>', 'foodCost':'<:Food:1240218818660532317>',
         'oreUpkeep':'<:Ore:1240218839644377181>', 'oreCost':'<:Ore:1240218839644377181>',
         'energyUpkeep':'<:Energy:1240221846343782501>', 'energyCost':'<:Energy:1240221846343782501>',
         'influenceUpkeep':'<:Influence:1240218825836728341>', 'influenceCost':'<:Influence:1240218825836728341>'}
resources = ('biomass', 'requisitions', 'food', 'ore', 'energy', 'influence')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    synced = await client.tree.sync()
    print("# CMDs synced: " + str(len(synced)))

@client.tree.command(name='gunit', description='Return info on a Gladius unit')
async def gunit(interaction: discord.Interaction, unitname:str):
    unit = Unit(unitname)
    unit.get_info_English(englishUnitsXMLPath, unit.get_unit_info)
    if not unit.found:
        markdown = '**'
        await interaction.response.send_message(markdown + unitname + markdown + ' not found. Did you mean ' + markdown + unit.bestMatch + markdown + '?')
    else:
        unit.get_unit_stats()
        unit.get_unit_count()
        unit.get_unit_weapons()
        unit.get_unit_traits()

        #Name and Description
        embed = discord.Embed(title=unit.name, description=unit.description)

        #Thumbnail
        image = discord.File('./Gladius/Icons/Units/' + unit.factionAndID + '.png', filename='icon.png')
        embed.set_thumbnail(url="attachment://icon.png")

        #Color
        embed.colour = factionColors[unit.faction]

        #Faction
        embed.add_field(name="Faction", value=camel_case_split(unit.faction))

        #Cost
        costText = ['<:Production:1240330971514011668> ' + unit.productionCost]
        for resource in resources:
            cost = resource + 'Cost'
            costValue = getattr(unit, cost)
            if costValue != '0':
                costText.extend((' | ', icons[cost], ' ', costValue))
        embed.add_field(name="Cost", value=''.join(costText))
        
        #Upkeep
        upkeepText = []
        for resource in resources:
            upkeep = resource + 'Upkeep'
            upkeepValue = getattr(unit, upkeep)
            if upkeepValue != '0':
                upkeepText.extend((' | ', icons[upkeep], ' ', upkeepValue))
        try:
            del upkeepText[0]
        except IndexError:
            pass
        embed.add_field(name="Upkeep", value=''.join(upkeepText))

        #Stats
        statText = ('**', unit.groupSize, ' model(s)**\n',
                    '<:Armor:1240218799832174703> ', unit.armor, ' | <:Hitpoints:1240330759781482528> ', unit.hitpointsMax,
                    ' | <:Morale:1240218836171493386> ', unit.moraleMax, '\n', '<:Movement:1240222322770579487> ', unit.movementMax,
                    ' | <:CargoSlots:1240218804982775848> ', unit.cargoSlots, ' | <:ItemSlots:1240218829280378912> ', unit.itemSlots)
        embed.add_field(name="Stats", value=''.join(statText))

        #Weapons
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
        embed.add_field(name="Weapons", value=''.join(weaponsText))

        #Traits
        traitsText = []
        for trait in unit.traits:
            # if upgrade required
            if unit.traits[trait]:
                upgrade = ' (U)'
            else:
                upgrade = ''
            traitsText.extend((trait.name, upgrade, '\n'))
        embed.add_field(name="Traits", value=''.join(traitsText), inline=False)
        
        #Flavor
        embed.add_field(name='Flavor', value='*' + unit.flavor + '*')
        #embed.set_footer(text=unit.flavor)
        embed.set_footer(text='Traits/weapons marked with (U) require a researchable upgrade.\nWeapons marked with (S) are secondary weapons.')

        await interaction.response.send_message(file=image, embed=embed)

@client.tree.command(name='gtrait', description='Return info on a Gladius trait')
async def gtrait(interaction: discord.Interaction, traitname:str):
    trait = Trait(traitname)
    trait.get_info_English(englishTraitsXMLPath, trait.get_trait_info)
    if not trait.found:
        markdown = '**'
        await interaction.response.send_message(markdown + traitname + markdown + ' not found. Did you mean ' + markdown + trait.bestMatch + markdown + '?')
    else:
        #Name and Description
        embed = discord.Embed(title=trait.name, description=trait.description)        

        #Color
        embed.colour = factionColors[trait.faction]

        #Faction
        embed.add_field(name="Faction", value=camel_case_split(trait.faction))

        #Flavor
        try:
            embed.add_field(name='Flavor', value='*' + trait.flavor + '*')
        except AttributeError:
            pass

        #Thumbnail
        try:
            image = discord.File('./Gladius/Icons/Traits/' + trait.factionAndID + '.png', filename='icon.png')
            embed.set_thumbnail(url="attachment://icon.png")
            await interaction.response.send_message(file=image, embed=embed)
        except FileNotFoundError:
            await interaction.response.send_message(embed=embed)        

client.run(TOKEN)
