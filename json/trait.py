from lxml import etree as ET
from os.path import join as pathJoin
from os.path import normpath
from obj import Obj, val2val


class Trait(Obj):
    OBJ_CLASS = 'Traits'

    def __init__(self, name: str):
        super().__init__(name)
        self.modifiers: str

    def get_modifiers(self):
        self.modifiers = ET.tostring(
            self.tree.getroot(), encoding='unicode')


class GTrait(Trait):
    GAME = 'Gladius'

    def __init__(self, name: str):
        super().__init__(name)
        self.factionAndID: str
        self.faction: str = None

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


class ZTrait(Trait):
    GAME = 'Zephon'

    def __init__(self, name: str):
        super().__init__(name)
