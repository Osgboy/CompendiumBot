from lxml import etree as ET
from thefuzz import fuzz
from re import sub as sub

class Obj():
    def __init__(self, name: str, game: str):
        self.name: str = name.casefold()
        self.game: str = game
        self.objClass: str# = ''
        self.englishDir: str = './' + game + '/English/'
        self.classDir: str = './' + game + '/' + self.objClass + '/'
        self.classXMLpath: str = self.englishDir + self.objClass + '.xml'
        self.found = False
        self.bestMatch: str
        self.internalID: str
        self.XMLPath: str
        self.tree: ET.ElementBase
        self.iconPath: str
        self.description: str
        self.flavor: str

    def fuzzy_match_name(self, typeFunc):
        tree = ET.parse(self.classXMLpath, parser=ET.XMLParser(recover=True, remove_comments=True))
        bestRatio = 0
        xmlTree = tree.getroot()
        for entry in xmlTree.iterdescendants('entry'):
            if all(x not in entry.get('name') for x in ('Flavor', 'Description', 'Properties')):
                targetStr = val2val(entry.get('value'), self.englishDir)
                try:
                    if targetStr.casefold() == self.name:
                        self.found = True
                        self.name = targetStr
                        typeFunc(xmlTree, entry)
                        return
                    else:
                        fuzzRatio = fuzz.token_sort_ratio(targetStr.casefold(), self.name)
                        if fuzzRatio > bestRatio:
                            bestRatio = fuzzRatio
                            self.bestMatch = targetStr
                except AttributeError:
                    pass

    def get_obj_info(self, xmlTree: ET.ElementBase, entry: ET.ElementBase):
        '''Gets internal ID, XML path, XML tree, flavor, and description.'''
        self.internalID = entry.get('name')
        self.XMLPath = self.classDir + self.internalID + '.xml'
        try:
            self.tree = ET.parse(self.XMLPath, parser=ET.XMLParser(recover=True, remove_comments=True))
        except OSError:
            pass
        for e in xmlTree:
            targetStr = e.get('name')
            if targetStr == self.internalID + 'Flavor':
                self.flavor = val2val(e.get('value'), self.englishDir)
            elif self.game == 'Gladius':
                if targetStr == self.internalID + 'Description':
                    self.description = val2val(e.get('value'), self.englishDir)
            elif self.game == 'Zephon':
                if targetStr == self.internalID + 'Properties':
                    self.description = val2val(e.get('value'), self.englishDir).replace("<icon texture='GUI/Bullet'/>", '')

    def get_obj_min_info(self, xmlTree: ET.ElementBase, entry: ET.ElementBase):
        '''Gets internal ID, XML path, and XML tree.'''
        self.internalID = entry.get('name')
        self.XMLPath = self.classDir + self.internalID + '.xml'
        try:
            self.tree = ET.parse(self.XMLPath, parser=ET.XMLParser(recover=True, remove_comments=True))
        except OSError:
            pass

    def get_icon_path(self):
        self.iconPath = self.tree.getroot().get('icon')

    @classmethod
    def from_internalID(cls, internalID: str, game: str):
        obj = cls('placeholder', game)
        obj.internalID = internalID
        #IDlen = len(internalID)
        tree = ET.parse(obj.classXMLpath, parser=ET.XMLParser(recover=True, remove_comments=True))
        xmlTree = tree.getroot()
        for entry in xmlTree.iterdescendants('entry'):
            targetStr = entry.get('name')
            if targetStr == internalID:
                obj.found = True
                obj.name = val2val(entry.get('value'), obj.englishDir)
                return obj

def val2val(value: str, englishDir: str) -> str:
    def valFromFile(matchobj):
        file, name = matchobj.group(1), matchobj.group(2)
        tree = ET.parse(englishDir + file + '.xml', parser=ET.XMLParser(recover=True, remove_comments=True))
        xmlTree = tree.getroot()
        for entry in xmlTree.iterdescendants('entry'):
            if entry.get('name') == name:
                if '/>' in (newval := entry.get('value')):
                    newval = val2val(newval, englishDir)
                return newval
    value = sub(r'<icon.*?\/>', '', value)
    value = sub(r'<br\/>', '\n', value)
    value = sub(r'<string\sname=\'(.*?)/(.*?)\'\/>', valFromFile, value)
    return value
