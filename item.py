from obj import Obj
from lxml import etree as ET

class Item(Obj):
    def __init__(self, name: str, game: str):
        self.objClass = 'Items'
        super().__init__(name, game)
        self.rarity = 'Common'
        self.influenceCost = '0'
        self.ability: str

    def get_item_ability(self):
        try:
            self.ability = ET.tostring(self.tree.find('actions'), encoding='unicode')[:1024]
        except AttributeError:
            pass

    def get_item_rarity(self):
        trait = self.tree.find('traits')
        if trait != None:
            if self.game == 'Gladius':
                self.rarity = trait.find('trait').get('name')
            elif self.game == 'Zephon':
                self.rarity = trait.find('trait').get('type')

    def get_item_influence_cost(self):
        self.influenceCost = self.tree.find('modifiers').find('modifier').find('effects').find('influenceCost').get('base')

class GItem(Item):
    def __init__(self, name: str, game: str):
        super().__init__(name, game)

class ZItem(Item):
    def __init__(self, name: str, game: str):
        super().__init__(name, game)
        self.branch: str
        self.buyCondition: str

    def get_branch(self):
        self.branch = self.tree.getroot().get('branch')

    def get_buy_conditions(self):
        try:
            self.buyCondition = self.tree.find('buyConditions').find('player').find('unlockedTrait').get('type')
        except AttributeError:
            pass
