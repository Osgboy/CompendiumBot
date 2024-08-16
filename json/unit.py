from dataclasses import dataclass
from lxml import etree as ET
from os.path import join as pathJoin
from os.path import normpath
from obj import Obj, ID2name, val2val
from weapon import GUnitWeaponStats


@dataclass  # (slots=True)
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


@dataclass  # (slots=True)
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


@dataclass  # (slots=True)
class GCombatStats:
    __slots__ = ['groupSizeMax', 'armor', 'hitpointsMax', 'moraleMax',
                 'movementMax', 'cargoSlots', 'itemSlots']
    groupSizeMax: int
    armor: int
    hitpointsMax: float
    moraleMax: int
    movementMax: int
    cargoSlots: int
    itemSlots: int


@dataclass  # (slots=True)
class ZCombatStats:
    __slots__ = ['groupSizeMax', 'accuracy', 'armor', 'hitpointsMax',
                 'moraleMax', 'movementMax', 'cargoSlots', 'itemSlots']
    groupSizeMax: int
    accuracy: int
    armor: int
    hitpointsMax: int
    moraleMax: int
    movementMax: int
    cargoSlots: int
    itemSlots: int


class Unit(Obj):
    OBJ_CLASS = 'Units'
    SKIPPED_ACTIONS: tuple

    def __init__(self, name: str):
        super().__init__(name)
        # Stats
        self.resourceStats: dataclass
        self.combatStats: dataclass
        self.weaponStats: dataclass
        # Weapons and traits
        self.weapons: dict[str, dict] = {}
        self.traits: dict[str, str] = {}
        self.actions: dict[str, str] = {}

    def get_stats(self):
        xmlStats = self.tree.find('modifiers').find('modifier').find('effects')
        for stat in self.resourceStats.__slots__:
            statEntry = xmlStats.find(stat)
            if statEntry is not None:
                setattr(self.resourceStats, stat,
                        statEntry.get('base', default='0'))
        for stat in self.combatStats.__slots__:
            statEntry = xmlStats.find(stat)
            if statEntry is not None:
                value = statEntry.get('base', default=0)
                try:
                    value = int(value)
                except ValueError:
                    value = float(value)
                setattr(self.combatStats, stat, value)

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
                self.weapons[weaponName] = {
                    'count': weapon.get('count', default='1'),
                    'requiredUpgrade': weapon.get('requiredUpgrade'),
                    'secondary': (lambda x: x == '0')(weapon.get('enabled', default='1'))}
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
                    # Capitalizes first letter of tag
                    actionID = tag[0].upper() + tag[1:]
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
        self.resourceStats: dataclass = GResourceStats(
            *['0']*len(GResourceStats.__slots__))
        self.combatStats: dataclass = GCombatStats(
            *[0]*len(GCombatStats.__slots__))
        self.factionAndID: str
        self.faction: str = 'Neutral'
        self.dlc: str = 'None'

    def get_obj_info(self, classTree: ET._ElementTree, entry: ET.ElementBase):
        self.factionAndID = entry.get('name')
        factionAndIDList = self.factionAndID.split('/')
        try:
            self.faction, self.internalID = factionAndIDList
        # only for Neutral/Artefacts/unit.xml
        except ValueError:
            self.faction, self.internalID = factionAndIDList[0], factionAndIDList[-1]
        self.XMLPath = pathJoin(
            self.CLASS_DIR, normpath(self.factionAndID) + '.xml')
        self.tree = ET.parse(self.XMLPath, parser=ET.XMLParser(
            recover=True, remove_comments=True))
        for e in classTree.getroot():
            targetStr = e.get('name')
            if targetStr == self.factionAndID + 'Description':
                self.description = val2val(e.get('value'), self.ENGLISH_DIR)
            elif targetStr == self.factionAndID + 'Flavor':
                self.flavor = val2val(e.get('value'), self.ENGLISH_DIR)

    def get_group_size(self):
        groupEntry = self.tree.find('group')
        if groupEntry is None:
            self.combatStats.groupSizeMax = '1'
        else:
            self.combatStats.groupSizeMax = groupEntry.get('size')

    def get_weapon_stats(self):
        self.weaponStats = GUnitWeaponStats(6, 6, 1, 1)
        xmlStats = self.tree.find('modifiers').find('modifier').find('effects')
        for statName in self.weaponStats.__slots__:
            statEntry = xmlStats.find(statName)
            if statEntry is not None and (statValue := statEntry.get('base')) is not None:
                setattr(self.weaponStats, statName, float(statValue))

    def get_dlc(self):
        if (dlc := self.tree.getroot().get('dlc')):
            self.dlc = dlc


class ZUnit(Unit):
    GAME = 'Zephon'
    SKIPPED_ACTIONS = ('appear', 'attack', 'die', 'endure', 'holdPosition', 'holdPositionUntilHealed',
                       'idle', 'kill', 'move', 'poke', 'select', 'skip')

    def __init__(self, name: str):
        super().__init__(name)
        self.resourceStats: dataclass = ZResourceStats(
            *['0']*len(ZResourceStats.__slots__))
        self.combatStats: dataclass = ZCombatStats(
            '1', '6', '0', '0', '0', '0', '0', '0')
        self.branch = 'Neutral'

    def get_branch(self):
        self.branch = self.tree.getroot().get('branch')
        if not self.branch:
            self.branch = 'Neutral'

    def get_accuracy(self):
        try:
            self.combatStats.accuracy = self.tree.find('modifiers').find(
                'modifier').find('effects').find('accuracy').get('base', default='6')
        except AttributeError:
            self.combatStats.accuracy = '6'
