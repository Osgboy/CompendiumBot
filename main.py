import discord
from discord.ext import commands
from lxml import etree as ET
from thefuzz import fuzz
from dataclasses import dataclass

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents)
englishUnitsXMLPath = './Gladius/English/Units.xml'
englishWeaponsXMLPath = './Gladius/English/Weapons.xml'

class Obj():
    def __init__(self, name: str):
        self.name = name.casefold()
        self.found = False
        self.bestMatch = ''
        self.internalID = ''

    def get_info_English(self, xmlPath: str, typeFunc):
        tree = ET.parse(xmlPath, parser=ET.XMLParser(recover=True, remove_comments=True))
        bestRatio = 0
        xmlTree = tree.getroot()
        for entry in xmlTree.iterdescendants('entry'):
            targetStr = entry.get('value')
            if targetStr.casefold() == self.name:
                self.found = True
                self.name = targetStr
                typeFunc(xmlTree, entry)
            elif 'Flavor' not in entry.get('name') and 'Description' not in entry.get('name'):
                fuzzRatio = fuzz.ratio(targetStr.casefold(), self.name)
                if fuzzRatio > bestRatio:
                    bestRatio = fuzzRatio
                    self.bestMatch = targetStr

    @classmethod
    def from_internalID(cls, internalID: str, xmlPath: str):
        obj = cls('placeholder')
        obj.internalID = internalID
        IDlen = len(internalID)
        tree = ET.parse(xmlPath, parser=ET.XMLParser(recover=True, remove_comments=True))
        xmlTree = tree.getroot()
        for entry in xmlTree.iterdescendants('entry'):
            targetStr = entry.get('name')
            if targetStr[-IDlen:] == internalID:
                obj.found = True
                obj.name = entry.get('value')
                return obj

class Unit(Obj):
    def __init__(self, name: str):
        super().__init__(name)
        self.factionAndID: str
        self.faction: str
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
        self.weapons: dict = {}

    def get_unit_info(self, xmlTree, entry):
        self.factionAndID = entry.get('name')
        self.faction, self.internalID = self.factionAndID.split('/')
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.factionAndID + 'Description':
                self.description = e.get('value')
            elif targetStr == self.factionAndID + 'Flavor':
                self.flavor = e.get('value')

    def get_unit_stats(self):
        tree = ET.parse('./Gladius/Units/' + self.factionAndID + '.xml')
        xmlStats = tree.find('modifiers').find('modifier').find('effects')
        statStrings = ('armor', 'biomassUpkeep', 'biomassCost', 'cargoSlots', 'energyUpkeep', 'energyCost', 'itemSlots', 'foodUpkeep', 'foodCost', 
                       'hitpointsMax', 'influenceUpkeep', 'influenceCost', 'moraleMax', 'movementMax', 'oreUpkeep', 
                       'oreCost', 'productionCost', 'requisitionsUpkeep', 'requisitionsCost')
        for statString in statStrings:
            statEntry = xmlStats.find(statString)
            if statEntry is not None:
                setattr(self, statString, statEntry.get('base', default='0'))

    def get_unit_count(self):
        tree = ET.parse('./Gladius/Units/' + self.factionAndID + '.xml')
        groupEntry = tree.find('group')
        if groupEntry is None:
            self.groupSize = '1'
        else:
            self.groupSize = groupEntry.get('size')

    def get_unit_weapons(self):
        tree = ET.parse('./Gladius/Units/' + self.factionAndID + '.xml')
        for weapon in tree.find('weapons').iterfind('weapon'):
            weaponName = Weapon.from_internalID(weapon.get('name'), englishWeaponsXMLPath)
            self.weapons[weaponName] = weapon.get('count', default='1')


class Weapon(Obj):
    def __init__(self, name: str):
        super().__init__(name)
        self.flavor: str


def camel_case_split(s):
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
    print("CMDs synced: " + str(len(synced)))

@client.tree.command(name='gunit', description='Return info on a Gladius unit')
async def gunit(interaction: discord.Interaction, unitname:str):
    unit = Unit(unitname)
    unit.get_info_English(englishUnitsXMLPath, unit.get_unit_info)
    if not unit.found:
        await interaction.response.send_message("__" + unitname + "__ not found. Did you mean __" + unit.bestMatch + '__?')
    else:
        unit.get_unit_stats()
        unit.get_unit_count()
        unit.get_unit_weapons()

        #Name and Description
        embed = discord.Embed(title=unit.name, description=unit.description)

        #Thumbnail
        image = discord.File('./Gladius/Icons/Units/' + unit.factionAndID + '.png', filename='icon.png')
        embed.set_thumbnail(url="attachment://icon.png")

        #Color
        embed.colour = factionColors[unit.faction]

        #Faction
        embed.add_field(name="Faction", value=camel_case_split(unit.faction))

        #Stats
        statText = ('**', unit.groupSize, ' model(s)**\n',
                    unit.armor, ' <:Armor:1240218799832174703> | ', unit.hitpointsMax, ' <:Hitpoints:1240330759781482528> | ',
                    unit.moraleMax, ' <:Morale:1240218836171493386>\n', unit.movementMax, ' <:Movement:1240222322770579487> | ',
                    unit.cargoSlots, ' <:CargoSlots:1240218804982775848> | ', unit.itemSlots, ' <:ItemSlots:1240218829280378912>')
        embed.add_field(name="Stats", value=''.join(statText))

        #Cost
        costText = [unit.productionCost + ' <:Production:1240330971514011668>']
        for resource in resources:
            cost = resource + 'Cost'
            costValue = getattr(unit, cost)
            if costValue != '0':
                costText.extend((' | ', costValue, ' ', icons[cost]))
        embed.add_field(name="Cost", value=''.join(costText))

        #Traits
        embed.add_field(name="Traits", value="placeholder")

        #Weapons
        weaponsText = []
        for weapon in unit.weapons:
            weaponsText.extend((unit.weapons[weapon], 'x ', weapon.name, '\n'))
        embed.add_field(name="Weapons", value=''.join(weaponsText))

        #Upkeep
        upkeepText = []
        for resource in resources:
            upkeep = resource + 'Upkeep'
            upkeepValue = getattr(unit, upkeep)
            if upkeepValue != '0':
                upkeepText.extend((' | ', upkeepValue, ' ', icons[upkeep]))
        try:
            del upkeepText[0]
        except IndexError:
            pass
        embed.add_field(name="Upkeep", value=''.join(upkeepText))

        #Flavor
        #embed.add_field(name='Flavor', value='*' + unit.flavor + '*')
        embed.set_footer(text=unit.flavor)

        await interaction.response.send_message(file=image, embed=embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('MTI0MDEwOTUyMzU0OTU1MjcxMw.GpjwW6.4GH7lLwXdHAgN-AlaEf1NJpONoKRvrEDo-n_3s')
