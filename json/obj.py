from lxml import etree as ET
from thefuzz import fuzz
from re import sub as sub
from typing import Callable
from os.path import join as pathJoin


class Obj():
    GAME: str
    OBJ_CLASS: str

    def __init__(self, name: str):
        self.name: str = name.casefold()
        self.ENGLISH_DIR: str = pathJoin(self.GAME, 'English')
        self.CLASS_DIR: str = pathJoin(self.GAME, self.OBJ_CLASS)
        self.CLASS_XML_PATH: str = pathJoin(self.ENGLISH_DIR, self.OBJ_CLASS + '.xml')
        self.found: bool = False
        self.bestMatch: str
        self.internalID: str
        self.XMLPath: str
        self.tree: ET._ElementTree
        self.iconPath: str
        self.description: str
        self.flavor: str

    def fuzzy_match_name(self, typeFunc: Callable[[ET._ElementTree, ET.ElementBase], None]):
        classTree = ET.parse(self.CLASS_XML_PATH, parser=ET.XMLParser(
            recover=True, remove_comments=True))
        bestRatio = 0
        for entry in classTree.iter('entry'):
            if (all(x not in entry.get('name') for x in ('Flavor', 'Description', 'Properties')) and
                (self.OBJ_CLASS != 'Factions' or all(x not in entry.get('name') for x in ('Discovered', 'Defeated', 'Quote')))):
                targetStr = val2val(entry.get('value'), self.ENGLISH_DIR)
                compareStr = targetStr.casefold()
                try:
                    if compareStr == self.name:
                        self.found = True
                        self.name = targetStr
                        typeFunc(classTree, entry)
                        return
                    else:
                        fuzzRatio = fuzz.token_sort_ratio(
                            compareStr, self.name)
                        for word in self.name.split():
                            if word in compareStr:
                                fuzzRatio += 100
                        if fuzzRatio > bestRatio:
                            bestRatio = fuzzRatio
                            self.bestMatch = targetStr
                except AttributeError:
                    pass

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
            elif self.GAME == 'Gladius':
                if targetStr == self.internalID + 'Description':
                    self.description = val2val(
                        e.get('value'), self.ENGLISH_DIR)
            elif self.GAME == 'Zephon':
                if targetStr == self.internalID + 'Properties':
                    self.description = val2val(e.get('value'), self.ENGLISH_DIR).replace(
                        "<icon texture='GUI/Bullet'/>", '')

    def get_obj_min_info(self, entry: ET.ElementBase):
        '''Gets internal ID, XML path, and XML tree.'''
        self.internalID = entry.get('name')
        self.XMLPath = pathJoin(self.CLASS_DIR, self.internalID + '.xml')
        try:
            self.tree = ET.parse(self.XMLPath, parser=ET.XMLParser(
                recover=True, remove_comments=True))
        except OSError:
            pass

    def get_icon_path(self):
        try:
            self.iconPath = self.tree.getroot().get('icon')
        except AttributeError:
            self.iconPath = self.tree.get('icon')


def ID2name(internalID: str, game: str, objClass: str) -> str:
    '''Converts an internal ID to a name.'''
    englishDir = pathJoin(game, 'English')
    classXMLPath = pathJoin(englishDir, objClass + '.xml')
    tree = ET.parse(classXMLPath, parser=ET.XMLParser(
        recover=True, remove_comments=True))
    for entry in tree.iter('entry'):
        targetStr = entry.get('name')
        if targetStr == internalID:
            return val2val(entry.get('value'), englishDir)


def val2val(value: str, englishDir: str) -> str:
    '''Follows a path recursively until a nonpath string is reached.'''
    def valFromFile(matchobj):
        file, name = matchobj.group(1), matchobj.group(2)
        tree = ET.parse(pathJoin(englishDir, file + '.xml'),
                        parser=ET.XMLParser(recover=True, remove_comments=True))
        for entry in tree.iter('entry'):
            if entry.get('name') == name:
                if '/>' in (newval := entry.get('value')):
                    newval = val2val(newval, englishDir)
                return newval
    value = sub(r'<icon.*?\/>', '', value)
    value = sub(r'<br\/>', '\n', value)
    value = sub(r'<string\sname=\'(.*?)/(.*?)\'\/>', valFromFile, value)
    return value
