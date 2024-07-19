from lxml import etree as ET
from os.path import join as pathJoin
from os.path import normpath
from obj import Obj, ID2name, val2val


class Upgrade(Obj):
    OBJ_CLASS = 'Upgrades'

    def __init__(self, name: str):
        super().__init__(name)
        self.tier: str
        self.requiredUpgrades = []

    def get_tier(self):
        if self.GAME == 'Gladius':
            tierStr = 'position'
        elif self.GAME == 'Zephon':
            tierStr = 'tier'
        self.tier = self.tree.getroot().get(tierStr)
        if not self.tier:
            self.tier = 'Not Researchable'

    def get_required_upgrades(self):
        try:
            for upgrade in self.tree.find('requiredUpgrades').iterfind('upgrade'):
                upgradeID = upgrade.get('name')
                self.requiredUpgrades.append(ID2name(upgradeID, self.GAME, 'Upgrades'))
        # no required upgrades
        except AttributeError:
            pass


class GUpgrade(Upgrade):
    GAME = 'Gladius'

    def __init__(self, name: str):
        super().__init__(name)
        self.factionAndID: str
        self.faction: str = 'Neutral'
        self.dlc: str = 'None'

    def get_obj_info(self, xmlTree: ET.ElementBase, entry: ET.ElementBase):
        self.factionAndID = entry.get('name')
        if '/' in self.factionAndID:
            self.faction, self.internalID = self.factionAndID.split('/')
        else:
            self.internalID = self.factionAndID
        self.XMLPath = pathJoin(
            self.CLASS_DIR, normpath(self.factionAndID) + '.xml')
        self.tree = ET.parse(self.XMLPath, parser=ET.XMLParser(
            recover=True, remove_comments=True))
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.factionAndID + 'Description':
                self.description = val2val(e.get('value'), self.ENGLISH_DIR)
            elif targetStr == self.factionAndID + 'Flavor':
                self.flavor = val2val(e.get('value'), self.ENGLISH_DIR)

    def get_dlc(self):
        if (dlc := self.tree.getroot().get('dlc')):
            self.dlc = dlc


class ZUpgrade(Upgrade):
    GAME = 'Zephon'

    def __init__(self, name: str):
        super().__init__(name)
        self.faction = 'Any'

    def get_branch(self):
        self.branch = self.tree.getroot().get('branch')
        if not self.branch:
            self.branch = 'Neutral'

    def get_faction(self):
        try:
            self.faction = self.tree.find('conditions').find('player').find('faction').get('name')
        except AttributeError:
            pass