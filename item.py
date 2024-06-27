from obj import Obj
from lxml import etree as ET

class Item(Obj):
    OBJ_CLASS = 'Items'

    def __init__(self, name: str):
        super().__init__(name)
        self.rarity = 'Common'
        self.influenceCost = '0'
        self.ability: str

    def get_ability(self):
        try:
            self.ability = ET.tostring(self.tree.find('actions'), encoding='unicode')[:1024]
        except AttributeError:
            pass

    def get_rarity(self):
        trait = self.tree.find('traits')
        if trait != None:
            if self.GAME == 'Gladius':
                self.rarity = trait.find('trait').get('name')
            elif self.GAME == 'Zephon':
                self.rarity = trait.find('trait').get('type')

    def get_influence_cost(self):
        self.influenceCost = self.tree.find('modifiers').find('modifier').find('effects').find('influenceCost').get('base')

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

    def get_buy_conditions(self):
        try:
            self.buyCondition = self.tree.find('buyConditions').find('player').find('unlockedTrait').get('type')
        except AttributeError:
            pass
