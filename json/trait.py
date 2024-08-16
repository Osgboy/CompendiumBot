from lxml import etree as ET
from obj import Obj
from util import Gladius, Modifiers


class Trait(Obj, Modifiers):
    OBJ_CLASS = 'Traits'

    def __init__(self, name: str):
        super().__init__(name)
        self.modifiers: list[str] = []
        self.rawXML: str

    def get_raw_XML(self):
        self.rawXML = ET.tostring(
            self.tree.getroot(), encoding='unicode')


class GTrait(Gladius, Trait):
    GAME = 'Gladius'

    def __init__(self, name: str):
        super().__init__(name)
        self.factionAndID: str
        self.faction: str = None


class ZTrait(Trait):
    GAME = 'Zephon'

    def __init__(self, name: str):
        super().__init__(name)
