import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from lxml import etree as ET
from thefuzz import fuzz

load_dotenv()
TOKEN = os.getenv("TEST_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents)
ENGLISH_PATH = './Gladius/English/'
ENGLISH_ITEMS_XML_PATH = './Gladius/English/Items.xml'
ENGLISH_UNITS_XML_PATH = './Gladius/English/Units.xml'
ENGLISH_WEAPONS_XML_PATH = './Gladius/English/Weapons.xml'
ENGLISH_TRAITS_XML_PATH = './Gladius/English/Traits.xml'

class Obj():
    def __init__(self, name: str):
        self.name: str = name.casefold()
        self.found: bool = False
        self.bestMatch: str = ''
        self.internalID: str = ''
        self.XMLPath: str = ''
        self.tree: object
        self.iconPath: str = ''
        self.description: str = ''
        self.flavor: str = ''

    def get_info_English(self, classXMLPath: str, typeFunc):
        tree = ET.parse(classXMLPath, parser=ET.XMLParser(recover=True, remove_comments=True))
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

    def get_icon(self):
        self.iconPath = self.tree.getroot().get('icon')

    @classmethod
    def from_internalID(cls, internalID: str, xmlPath: str):
        obj = cls('placeholder')
        obj.internalID = internalID
        #IDlen = len(internalID)
        tree = ET.parse(xmlPath, parser=ET.XMLParser(recover=True, remove_comments=True))
        xmlTree = tree.getroot()
        for entry in xmlTree.iterdescendants('entry'):
            targetStr = entry.get('name')
            if targetStr == internalID:
                obj.found = True
                obj.name = val2val(entry.get('value'))
                return obj

class Item(Obj):
    def __init__(self, name: str):
        super().__init__(name)
        self.rarity: str = 'Common'
        self.influenceCost: int = 0

    def get_item_info(self, xmlTree, entry):
        self.internalID = entry.get('name')
        self.XMLPath = './Gladius/Items/' + self.internalID + '.xml'
        self.tree = ET.parse(self.XMLPath)
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.internalID + 'Description':
                self.description = val2val(e.get('value'))
            elif targetStr == self.internalID + 'Flavor':
                self.flavor = val2val(e.get('value'))

    def get_item_rarity(self):
        trait = self.tree.find('traits')
        if trait != None:
            self.rarity = trait.find('trait').get('name')

    def get_item_influence_cost(self):
        self.influenceCost = self.tree.find('modifiers').find('modifier').find('effects').find('influenceCost').get('base')

class Unit(Obj):
    def __init__(self, name: str):
        super().__init__(name)
        self.factionAndID: str
        self.faction: str = 'Neutral'
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
        self.movementMax: str = '0'
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
        try:
            self.faction, self.internalID = self.factionAndID.split('/')
        # only for Neutral/Artefacts/unit.xml
        except ValueError:
            self.faction, self.internalID = self.factionAndID.split('/')[0], self.factionAndID.split('/')[-1] 
        self.XMLPath = './Gladius/Units/' + self.factionAndID + '.xml'
        self.tree = ET.parse(self.XMLPath)
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.factionAndID + 'Description':
                self.description = e.get('value')
            elif targetStr == self.factionAndID + 'Flavor':
                self.flavor = e.get('value')

    def get_unit_stats(self):
        xmlStats = self.tree.find('modifiers').find('modifier').find('effects')
        statStrings = ('armor', 'biomassUpkeep', 'biomassCost', 'cargoSlots', 'energyUpkeep', 'energyCost', 'itemSlots', 'foodUpkeep', 'foodCost', 
                       'hitpointsMax', 'influenceUpkeep', 'influenceCost', 'moraleMax', 'movementMax', 'oreUpkeep', 
                       'oreCost', 'productionCost', 'requisitionsUpkeep', 'requisitionsCost')
        for statString in statStrings:
            statEntry = xmlStats.find(statString)
            if statEntry is not None:
                setattr(self, statString, statEntry.get('base', default='0'))

    def get_unit_count(self):
        groupEntry = self.tree.find('group')
        if groupEntry is None:
            self.groupSize = '1'
        else:
            self.groupSize = groupEntry.get('size')

    def get_unit_weapons(self):
        try:    
            for weapon in self.tree.find('weapons').iterfind('weapon'):
                if weapon.get('name') == 'None':
                    continue
                weaponObj = Weapon.from_internalID(weapon.get('name'), ENGLISH_WEAPONS_XML_PATH)
                # {weaponObj:(weaponCount, requiredUpgrade, enabled), ...}
                self.weapons[weaponObj] = (weapon.get('count', default='1'), weapon.get('requiredUpgrade'), weapon.get('enabled', default="1"))
        # no weapons
        except AttributeError:
            pass

    def get_unit_traits(self):
        try:
            for trait in self.tree.find('traits').iterfind('trait'):
                traitObj = Trait.from_internalID(trait.get('name'), ENGLISH_TRAITS_XML_PATH)
                self.traits[traitObj.name] = trait.get('requiredUpgrade')
        # no traits
        except AttributeError:
            pass

class Weapon(Obj):
    def __init__(self, name: str):
        super().__init__(name)
        self.attacks = '?'
        self.armorPen = '?'
        self.damage = '?'
        self.range = '?'
        self.accuracy = '?'
        self.traits: dict = {}

    def get_weapon_info(self, xmlTree, entry):
        self.internalID = entry.get('name')
        self.XMLPath = './Gladius/Weapons/' + self.internalID + '.xml'
        self.tree = ET.parse(self.XMLPath)
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.internalID + 'Description':
                self.description = val2val(e.get('value'))
            elif targetStr == self.internalID + 'Flavor':
                self.flavor = val2val(e.get('value'))
    
    def get_weapon_traits(self):
        try:
            for trait in self.tree.find('traits').iterfind('trait'):
                traitObj = Trait.from_internalID(trait.get('name'), ENGLISH_TRAITS_XML_PATH)
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
            damagePrefix = 'strength'
        else:
            prefix = 'ranged'
            damagePrefix = 'ranged'
        try:
            self.attacks = effects.find('attacks').items()[0][1]
        except AttributeError:
            pass
        try:
            self.armorPen = effects.find(prefix + 'ArmorPenetration').items()[0][1]
        except AttributeError:
            pass
        try:
            self.damage = effects.find(damagePrefix + 'Damage').items()[0][1]
        except AttributeError:
            pass
        try:
            self.accuracy = effects.find(prefix + 'Accuracy').items()[0][1]
        except AttributeError:
            pass

class Trait(Obj):
    def __init__(self, name: str):
        super().__init__(name)
        self.factionAndID: str
        self.faction: str = 'Neutral'

    def get_trait_info(self, xmlTree, entry):
        self.factionAndID = entry.get('name')
        if '/' in self.factionAndID:
            self.faction, self.internalID = self.factionAndID.split('/')
        else:
            self.internalID = self.factionAndID
        self.XMLPath = './Gladius/Traits/' + self.factionAndID + '.xml'
        self.tree = ET.parse(self.XMLPath)
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.factionAndID + 'Description':
                self.description = val2val(e.get('value'))
            elif targetStr == self.factionAndID + 'Flavor':
                self.flavor = val2val(e.get('value'))

def val2val(value: str) -> str:
    if '<string name=' in value:
        path = value[14:-3]
        file, name = path.split('/', 1)
        tree = ET.parse(ENGLISH_PATH + file + '.xml', parser=ET.XMLParser(recover=True, remove_comments=True))
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
rarityColors = {'Common':discord.colour.Color.from_rgb(255, 255, 255),
                'Uncommon':discord.colour.Color.from_rgb(0, 191, 191),
                'Artefact':discord.colour.Color.from_rgb(191, 0, 191)}
icons = {'biomassUpkeep':'<:Biomass:1240218802831233118>', 'biomassCost':'<:Biomass:1240218802831233118>',
         'requisitionsUpkeep':'<:Requisitions:1240222555588268032>', 'requisitionsCost':'<:Requisitions:1240222555588268032>',
         'foodUpkeep':'<:Food:1240218818660532317>', 'foodCost':'<:Food:1240218818660532317>',
         'oreUpkeep':'<:Ore:1240218839644377181>', 'oreCost':'<:Ore:1240218839644377181>',
         'energyUpkeep':'<:Energy:1240221846343782501>', 'energyCost':'<:Energy:1240221846343782501>',
         'influenceUpkeep':'<:Influence:1240218825836728341>', 'influenceCost':'<:Influence:1240218825836728341>',
         'production':'<:Production:1240330971514011668>',
         
         'armor':'<:Armor:1240218799832174703>', 'hitpoints':'<:Hitpoints:1240330759781482528>',
         'morale':'<:Morale:1240218836171493386>', 'movement':'<:Movement:1240222322770579487>',
         'cargoSlots':'<:CargoSlots:1240218804982775848>', 'itemSlots':'<:ItemSlots:1240218829280378912>',
         
         'damage':'<:Damage:1240218813123919893>', 'attacks':'<:Attacks:1240218801799434241>',
         'armorPenetration':'<:ArmorPenetration:1240218800855715840>', 'accuracy':'<:Accuracy:1240218797458063361>',
         'range':'<:Range:1240218850763477013>'}
resources = ('biomass', 'requisitions', 'food', 'ore', 'energy', 'influence')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    synced = await client.tree.sync()
    print("# CMDs synced: " + str(len(synced)))

@client.tree.command(name='gitem', description='Return info on a Gladius item')
async def gitem(interaction: discord.Interaction, itemname:str):
    item = Item(itemname)
    item.get_info_English(ENGLISH_ITEMS_XML_PATH, item.get_item_info)
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
        embed.add_field(name="Cost", value=icons['influenceCost'] + ' ' + item.influenceCost)

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
    unit = Unit(unitname)
    unit.get_info_English(ENGLISH_UNITS_XML_PATH, unit.get_unit_info)
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
        embed.colour = factionColors[unit.faction]

        # Faction
        embed.add_field(name="Faction", value=camel_case_split(unit.faction))

        # Cost
        costText = [icons['production'], ' ', unit.productionCost]
        for resource in resources:
            cost = resource + 'Cost'
            costValue = getattr(unit, cost)
            if costValue != '0':
                costText.extend((' | ', icons[cost], ' ', costValue))
        embed.add_field(name="Cost", value=''.join(costText))
        
        # Upkeep
        upkeepText = []
        for resource in resources:
            upkeep = resource + 'Upkeep'
            upkeepValue = getattr(unit, upkeep)
            if upkeepValue != '0':
                upkeepText.extend((' | ', icons[upkeep], ' ', upkeepValue))
        try:
            # delete initial ' | '
            del upkeepText[0]
        except IndexError:
            pass
        if upkeepText == []:
            upkeepText = ['None']
        embed.add_field(name="Upkeep", value=''.join(upkeepText))

        # Stats
        statText = ('**', unit.groupSize, ' model(s)**\n',
                    icons['armor'], ' ', unit.armor, ' | ', icons['hitpoints'], ' ', unit.hitpointsMax, ' | ',
                    icons['morale'], ' ', unit.moraleMax, '\n', icons['movement'], ' ', unit.movementMax, ' | ',
                    icons['cargoSlots'], ' ', unit.cargoSlots, ' | ', icons['itemSlots'], ' ', unit.itemSlots)
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
        embed.set_footer(text='Traits/weapons marked with (U) require a researchable upgrade.\nWeapons marked with (S) are secondary weapons.')

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

@client.tree.command(name='gweapon', description='Return info on a Gladius weapon')
async def gweapon(interaction: discord.Interaction, weaponname:str):
    weapon = Weapon(weaponname)
    weapon.get_info_English(ENGLISH_WEAPONS_XML_PATH, weapon.get_weapon_info)
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
        statText = (icons['damage'], ' ', weapon.damage, ' | ', icons['attacks'], ' ', weapon.attacks, '\n',
                    icons['armorPenetration'], ' ', weapon.armorPen, ' | ', icons['accuracy'], ' ', weapon.accuracy, '\n',
                    icons['range'], ' ', weapon.range)
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
                                'Weapon stats depend on the unit wielding the weapon. '
                                'Values may not be accurate.'))

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
    trait = Trait(traitname)
    trait.get_info_English(ENGLISH_TRAITS_XML_PATH, trait.get_trait_info)
    if not trait.found:
        markdown = '**'
        await interaction.response.send_message(markdown + traitname + markdown + ' not found. Did you mean ' + markdown + trait.bestMatch + markdown + '?')
    else:
        trait.get_icon()

        # Name and Description
        embed = discord.Embed(title=trait.name, description=trait.description)        

        # Color
        embed.colour = factionColors[trait.faction]

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

client.run(TOKEN)
