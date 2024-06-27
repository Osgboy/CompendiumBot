from dataclasses import dataclass
from lxml import etree as ET
from obj import Obj, ID2name
from weapon import Weapon, GWeaponStats
from trait import Trait
from action import Action

@dataclass#(slots=True)
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

@dataclass#(slots=True)
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

@dataclass#(slots=True)
class GCombatStats:
    __slots__ = ['groupSizeMax', 'armor', 'hitpointsMax', 'moraleMax',
                 'movementMax', 'cargoSlots', 'itemSlots']
    groupSizeMax: str
    armor: str
    hitpointsMax: str
    moraleMax: str
    movementMax: str
    cargoSlots: str
    itemSlots: str

@dataclass#(slots=True)
class ZCombatStats:
    __slots__ = ['groupSizeMax', 'accuracy', 'armor', 'hitpointsMax',
                 'moraleMax', 'movementMax', 'cargoSlots', 'itemSlots']
    groupSizeMax: str
    accuracy: str
    armor: str
    hitpointsMax: str
    moraleMax: str
    movementMax: str
    cargoSlots: str
    itemSlots: str

class Unit(Obj):
    OBJ_CLASS = 'Units'
    SKIPPED_ACTIONS: tuple

    def __init__(self, name: str):
        super().__init__(name)
        # Stats
        self.resourceStats: dataclass
        self.combatStats: dataclass
        self.weaponStats: dataclass
        #Weapons and traits
        self.weapons = {}
        self.traits = {}
        self.actions = {}

    def get_stats(self):
        xmlStats = self.tree.find('modifiers').find('modifier').find('effects')
        for stat in self.resourceStats.__slots__:
            statEntry = xmlStats.find(stat)
            if statEntry is not None:
                setattr(self.resourceStats, stat, statEntry.get('base', default='0'))
        for stat in self.combatStats.__slots__:
            statEntry = xmlStats.find(stat)
            if statEntry is not None:
                if self.GAME == 'Gladius' and stat == 'hitpointsMax':
                    setattr(self.combatStats, stat, str(round(float(statEntry.get('base')))))
                else:
                    setattr(self.combatStats, stat, statEntry.get('base', default='0'))

    def get_weapons(self):
        if self.GAME == 'Gladius':
            attrName = 'name'
        elif self.GAME == 'Zephon':
            attrName = 'type'
        try:
            for weapon in self.tree.find('weapons').iterfind('weapon'):
                if (weaponID := weapon.get(attrName)) == 'None':
                    continue
                weaponName = ID2name(weaponID, self.GAME, 'Weapons')
                self.weapons[weaponName] = (weapon.get('count', default='1'), weapon.get('requiredUpgrade'), weapon.get('enabled', default="1"))
        # no weapons
        except AttributeError:
            pass

    def get_traits(self):
        if self.GAME == 'Gladius':
            attrName = 'name'
        elif self.GAME == 'Zephon':
            attrName = 'type'
        try:
            for trait in self.tree.find('traits').iterfind('trait'):
                traitID = trait.get(attrName)
                traitName = ID2name(traitID, self.GAME, 'Traits')
                self.traits[traitName] = trait.get('requiredUpgrade')
        # no traits
        except AttributeError:
            pass

    def get_actions(self):
        try:
            for action in self.tree.find('actions'):
                if (tag := action.tag) in self.SKIPPED_ACTIONS:
                    continue
                if not (actionID := action.get('name')):
                    actionID = tag[0].upper() + tag[1:] # Capitalizes first letter of tag
                actionName = ID2name(actionID, self.GAME, 'Actions')
                if actionName:
                    self.actions[actionName] = action.get('requiredUpgrade')
        # no actions
        except AttributeError:
            pass

class GUnit(Unit):
    GAME = 'Gladius'
    SKIPPED_ACTIONS = ('attack', 'die', 'idle', 'move')

    def __init__(self, name: str):
        super().__init__(name)        
        self.resourceStats: dataclass = GResourceStats(*['0']*len(GResourceStats.__slots__))
        self.combatStats: dataclass = GCombatStats(*['0']*len(GCombatStats.__slots__))
        self.factionAndID: str
        self.faction = 'Neutral'

    def get_obj_info(self, xmlTree: ET.ElementBase, entry: ET.ElementBase):
        self.factionAndID = entry.get('name')
        try:
            self.faction, self.internalID = self.factionAndID.split('/')
        # only for Neutral/Artefacts/unit.xml
        except ValueError:
            self.faction, self.internalID = self.factionAndID.split('/')[0], self.factionAndID.split('/')[-1] 
        self.XMLPath = self.CLASS_DIR + self.factionAndID + '.xml'
        self.tree = ET.parse(self.XMLPath)
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.factionAndID + 'Description':
                self.description = e.get('value')
            elif targetStr == self.factionAndID + 'Flavor':
                self.flavor = e.get('value')

    def get_group_size(self):
        groupEntry = self.tree.find('group')
        if groupEntry is None:
            self.combatStats.groupSizeMax = '1'
        else:
            self.combatStats.groupSizeMax = groupEntry.get('size')

    def get_weapon_stats(self):
        self.weaponStats = GWeaponStats('6', '6', '1', '1')
        xmlStats = self.tree.find('modifiers').find('modifier').find('effects')
        for statName in self.weaponStats.__slots__:
            statEntry = xmlStats.find(statName)
            if statEntry is not None and (statValue := statEntry.get('base')) is not None:
                setattr(self.weaponStats, statName, statValue)

class ZUnit(Unit):
    GAME = 'Zephon'
    SKIPPED_ACTIONS = ('appear', 'attack', 'die', 'endure', 'holdPosition', 'holdPositionUntilHealed',
                        'idle', 'kill', 'move', 'poke', 'select', 'skip')

    def __init__(self, name: str):
        super().__init__(name)
        self.resourceStats: dataclass = ZResourceStats(*['0']*len(ZResourceStats.__slots__))
        self.combatStats: dataclass = ZCombatStats('1', '6', '0', '0', '0', '0', '0', '0')
        self.branch = 'Neutral'

    def get_branch(self):
        self.branch = self.tree.getroot().get('branch')
        if not self.branch:
            self.branch = 'Neutral'

    def get_accuracy(self):
        self.combatStats.accuracy = self.tree.find('modifiers').find('modifier').find('effects').find('accuracy').get('base', default='6')