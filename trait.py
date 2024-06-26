from lxml import etree as ET
from obj import Obj, val2val

class Trait(Obj):
    def __init__(self, name: str, game: str):
        self.objClass = 'Traits'
        super().__init__(name, game)
        self.modifiers: str

    def get_trait_modifiers(self):
        self.modifiers = ET.tostring(self.tree.getroot(), encoding='unicode')[:1024]

class GTrait(Trait):
    def __init__(self, name: str, game: str):
        super().__init__(name, game)
        self.factionAndID: str
        self.faction = 'Neutral'

    def get_obj_info(self, xmlTree: ET.ElementBase, entry: ET.ElementBase):
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

class ZTrait(Trait):
    def __init__(self, name: str, game: str):
        super().__init__(name, game)
