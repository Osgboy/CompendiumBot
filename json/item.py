from obj import Obj, ID2name
from lxml import etree as ET
from util import Modifiers


class Item(Obj, Modifiers):
    OBJ_CLASS = 'Items'

    def __init__(self, name: str):
        super().__init__(name)
        self.rarity = 'Common'
        self.influenceCost = '0'
        self.modifiers: list[str] = []
        self.rawXML: str

    def get_rarity(self):
        trait = self.tree.find('traits')
        if trait != None:
            if self.GAME == 'Gladius':
                self.rarity = trait.find('trait').get('name')
            elif self.GAME == 'Zephon':
                self.rarity = trait.find('trait').get('type')

    def get_influence_cost(self):
        self.influenceCost = self.tree.find('modifiers').find(
            'modifier').find('effects').find('influenceCost').get('base')

    def get_raw_XML(self):
        try:
            self.rawXML = ET.tostring(self.tree.find(
                'actions'), encoding='unicode')
        except TypeError:
            pass


class GItem(Item):
    GAME = 'Gladius'

    def __init__(self, name: str):
        super().__init__(name)


class ZItem(Item):
    GAME = 'Zephon'

    def __init__(self, name: str):
        super().__init__(name)
        self.branch: str
        self.buyCondition: str

    def get_branch(self):
        self.branch = self.tree.getroot().get('branch')

    def get_buy_condition(self):
        try:
            buyConditionID = self.tree.find('buyConditions').find(
                'player').find('trait').get('type')
            self.buyCondition = ID2name(buyConditionID, self.GAME, 'Traits')
        except AttributeError:
            pass
