from obj import Obj, ID2name, val2val
from lxml import etree as ET
from os.path import join as pathJoin

class Faction(Obj):
    OBJ_CLASS = 'Factions'

    def __init__(self, name: str):
        super().__init__(name)
        self.actions: dict[str, str] = {}
        self.startingUnits: dict[str, str] = {}
        self.traits: dict[str, str] = {}

    def get_actions(self):
        if (xmlActions := self.tree.find('actions')) is not None:
            for action in xmlActions:
                if not (actionID := action.get('name')):
                    # Capitalizes first letter of tag
                    actionID = action.tag[0].upper() + action.tag[1:]
                actionName = ID2name(actionID, self.GAME, 'Actions')
                self.actions[actionName] = action.get('requiredUpgrade')

    def get_starting_units(self):
        if (xmlUnits := self.tree.find('startingUnits')) is not None:
            for unit in xmlUnits:
                unitName = ID2name(unit.get('type'), self.GAME, 'Units')
                if (count := unit.get('count')):
                    self.startingUnits[unitName] = unit.get('count')
                else:
                    self.startingUnits[unitName] = '1'


    def get_traits(self):
        if self.GAME == 'Gladius':
            attrName = 'name'
        elif self.GAME == 'Zephon':
            attrName = 'type'
        if (xmlTraits := self.tree.find('traits')) is not None:
            for trait in xmlTraits:
                traitName = ID2name(trait.get(attrName), self.GAME, 'Traits')
                self.traits[traitName] = trait.get('requiredUpgrade')


class GFaction(Faction):
    GAME = 'Gladius'

    def get_obj_info(self, classTree: ET._ElementTree, entry: ET.ElementBase):
        '''Gets internal ID, XML path, XML tree, flavor, and description.'''
        self.internalID = entry.get('name')
        self.XMLPath = pathJoin(self.CLASS_DIR, self.internalID + '.xml')
        try:
            self.tree = ET.parse(self.XMLPath, parser=ET.XMLParser(
                recover=True, remove_comments=True))
        except OSError:
            pass
        for e in classTree.getroot():
            targetStr = e.get('name')
            if targetStr == self.internalID + 'Flavor':
                self.flavor = val2val(e.get('value'), self.ENGLISH_DIR)
                self.flavor = self.flavor.replace("<style name='Italic'/>", '')
                self.flavor = self.flavor.replace("<style name='Default'/>", '')
            if targetStr == self.internalID + 'ShortFlavor':
                self.description = val2val(
                    e.get('value'), self.ENGLISH_DIR)


class ZFaction(Faction):
    GAME = 'Zephon'

    def __init__(self, name: str):
        super().__init__(name)
        self.branch: str
        self.likedLabels: list = []
        self.dislikedLabels: list = []

    def get_obj_info(self, classTree: ET._ElementTree, entry: ET.ElementBase):
        '''Gets internal ID, XML path, XML tree, flavor, and description.'''
        self.internalID = entry.get('name')
        self.XMLPath = pathJoin(self.CLASS_DIR, self.internalID + '.xml')
        try:
            self.tree = ET.parse(self.XMLPath, parser=ET.XMLParser(
                recover=True, remove_comments=True))
        except OSError:
            pass
        for e in classTree.getroot():
            targetStr = e.get('name')
            if targetStr == self.internalID + 'Flavor':
                self.flavor = val2val(e.get('value'), self.ENGLISH_DIR)
            if targetStr == self.internalID + 'Quote':
                self.description = val2val(
                    e.get('value'), self.ENGLISH_DIR)
                self.description = self.description.replace("<style name='Italic'/>", '')
                self.description = self.description.replace("<style name='Default'/>", '')
    
    def get_branch(self):
        self.branch = self.tree.getroot().get('branch')
        if not self.branch:
            self.branch = 'Neutral'

    def get_liked_labels(self):
        if (xmlLabels := self.tree.find('likedLabels')) is not None:
            for label in xmlLabels:
                labelName = ID2name(label.get('name'), self.GAME, 'Traits')
                if labelName:
                    self.likedLabels.append(labelName)
                else:
                    self.likedLabels.append(label.get('name'))

    def get_disliked_labels(self):
        if (xmlLabels := self.tree.find('dislikedLabels')) is not None:
            for label in xmlLabels:
                labelName = ID2name(label.get('name'), self.GAME, 'Traits')
                if labelName:
                    self.dislikedLabels.append(labelName)
                else:
                    self.dislikedLabels.append(label.get('name'))
