import discord
from discord.ext import commands
from lxml import etree as ET
from thefuzz import fuzz
from dataclasses import dataclass

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents)

class Obj():
    def __init__(self, name: str):
        self.name = name
        self.found = False
        self.bestMatch = ''
        self.internalID = ''

    def get_info_English(self, xmlPath: str, typeFunc):
        tree = ET.parse(xmlPath, parser=ET.XMLParser(recover=True, remove_comments=True))
        bestRatio = 0
        xmlTree = tree.getroot()
        for entry in xmlTree.iterdescendants('entry'):
            targetStr = entry.get('value')
            if targetStr == self.name:
                self.found = True
                typeFunc(xmlTree, entry)
            elif 'Flavor' not in entry.get('name') and 'Description' not in entry.get('name'):
                fuzzRatio = fuzz.ratio(targetStr, self.name)
                if fuzzRatio > bestRatio:
                    bestRatio = fuzzRatio
                    self.bestMatch = targetStr

    @classmethod
    def from_internalID(cls, internalID: str):
        obj = cls('placeholder')
        obj.internalID = internalID


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
        self.weapons: dict

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
        statStrings = ('armor', 'cargoSlots', 'energyUpkeep', 'energyCost', 'itemSlots', 'foodUpkeep', 'foodCost', 
                       'hitpointsMax', 'influenceUpkeep', 'influenceCost', 'moraleMax', 'movementMax', 'oreUpkeep', 
                       'oreCost', 'productionCost')
        for statString in statStrings:
            statEntry = xmlStats.find(statString)
            if statEntry is not None:
                setattr(self, statString, statEntry.get('base', default='0'))

    def get_unit_count(self):
        tree = ET.parse('./Gladius/Units/' + self.factionAndID + '.xml')
        groupEntry = tree.find('group')
        if groupEntry is None:
            self.groupSize = 1
        else:
            self.groupSize = groupEntry.get('size')

    def get_unit_weapons(self):
        tree = ET.parse('./Gladius/Units/' + self.factionAndID + '.xml')
        for weapon in tree.iterfind('weapons'):
            self.weapons[Weapon(weapon.get('name'))] = weapon.get('count', default='1')



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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    synced = await client.tree.sync()
    print("CMDs synced: " + str(len(synced)))

@client.tree.command(name='gunit', description='Return info on a Gladius unit')
async def gunit(interaction: discord.Interaction, unitname:str):
    unit = Unit(unitname)
    if not unit.found:
        await interaction.response.send_message(unitname + " not found. Did you mean " + unit.bestMatch + '?')
    else:
        embed = discord.Embed(title=unitname, description=unit.description)
        image = discord.File('./Gladius/Icons/Units/' + unit.factionAndID + '.png', filename='icon.png')
        embed.set_thumbnail(url="attachment://icon.png")
        embed.add_field(name="Faction", value=camel_case_split(unit.faction))
        statText = (unit.armor, '<:Armor:1240218799832174703> | ', unit.hitpointsMax, '<:Hitpoints:1240330759781482528> | ',
                    unit.moraleMax, '<:Morale:1240218836171493386>\n', unit.movementMax, '<:Movement:1240222322770579487> | ',
                    unit.cargoSlots, '<:CargoSlots:1240218804982775848> | ', unit.itemSlots, '<:ItemSlots:1240218829280378912>')
        embed.add_field(name="Stats", value=''.join(statText))
        costText = [unit.productionCost + '<:Production:1240330971514011668>']
        if unit.foodCost:
            costText.extend((' | ', unit.foodCost, '<:Food:1240218818660532317>'))
        if unit.oreCost:
            costText.extend((' | ', unit.oreCost, '<:Ore:1240218839644377181>'))
        if unit.energyCost:
            costText.extend((' | ', unit.energyCost, '<:Energy:1240221846343782501>'))
        if unit.influenceCost:
            costText.extend((' | ', unit.influenceCost, '<:Influence:1240218825836728341>'))
        embed.add_field(name="Cost", value=''.join(costText))
        embed.add_field(name="Traits", value="big tank")
        embed.add_field(name="Weapons", value="big dakka")
        upkeepText = []
        if unit.foodUpkeep:
            costText.extend((' | ', unit.foodUpkeep, '<:Food:1240218818660532317>'))
        if unit.oreUpkeep:
            costText.extend((' | ', unit.oreUpkeep, '<:Ore:1240218839644377181>'))
        if unit.energyUpkeep:
            costText.extend((' | ', unit.energyUpkeep, '<:Energy:1240221846343782501>'))
        if unit.influenceUpkeep:
            costText.extend((' | ', unit.influenceUpkeep, '<:Influence:1240218825836728341>'))
        embed.add_field(name="Upkeep", value=''.join(upkeepText))
        await interaction.response.send_message(file=image, embed=embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

unitname = "Baneblade"
unit = Unit(unitname)
if not unit.found:
    print(unitname + " not found. Did you mean " + unit.bestMatch + '?')
else:
    embed = discord.Embed(title=unitname, description=unit.description)
    embed.add_field(name="Faction", value=camel_case_split(unit.faction))
    statText = (unit.armor, '<:Armor:1240218799832174703> | ', unit.hitpointsMax, '<:Hitpoints:1240330759781482528> | ',
                unit.moraleMax, '<:Morale:1240218836171493386>\n', unit.movementMax, '<:Movement:1240222322770579487> | ',
                unit.cargoSlots, '<:CargoSlots:1240218804982775848> | ', unit.itemSlots, '<:ItemSlots:1240218829280378912>')
    embed.add_field(name="Stats", value=''.join(statText))
    costText = [unit.productionCost + '<:Production:1240330971514011668>']
    if unit.foodCost:
        costText.extend((' | ', unit.foodCost, '<:Food:1240218818660532317>'))
    if unit.oreCost:
        costText.extend((' | ', unit.oreCost, '<:Ore:1240218839644377181>'))
    if unit.energyCost:
        costText.extend((' | ', unit.energyCost, '<:Energy:1240221846343782501>'))
    if unit.influenceCost:
        costText.extend((' | ', unit.influenceCost, '<:Influence:1240218825836728341>'))
    embed.add_field(name="Cost", value=''.join(costText))
    embed.add_field(name="Traits", value="big tank")
    embed.add_field(name="Weapons", value="big dakka")
    upkeepText = []
    if unit.foodUpkeep:
        costText.extend((' | ', unit.foodUpkeep, '<:Food:1240218818660532317>'))
    if unit.oreUpkeep:
        costText.extend((' | ', unit.oreUpkeep, '<:Ore:1240218839644377181>'))
    if unit.energyUpkeep:
        costText.extend((' | ', unit.energyUpkeep, '<:Energy:1240221846343782501>'))
    if unit.influenceUpkeep:
        costText.extend((' | ', unit.influenceUpkeep, '<:Influence:1240218825836728341>'))
    embed.add_field(name="Upkeep", value=''.join(upkeepText))
    print(vars(unit))