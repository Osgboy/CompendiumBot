from obj import Obj, ID2name
from util import Gladius

GLADIUS_RESOURCE_COSTS = (
    'biomassUpkeep', 'biomassCost',
    'requisitionsUpkeep', 'requisitionsCost',
    'foodUpkeep', 'foodCost',
    'oreUpkeep', 'oreCost',
    'energyUpkeep', 'energyCost',
    'influenceUpkeep', 'influenceCost',
    'productionCost',
)
ZEPHON_RESOURCE_COSTS = (
    'foodUpkeep', 'foodCost',
    'mineralsUpkeep', 'mineralsCost',
    'energyUpkeep', 'energyCost',
    'transuraniumUpkeep', 'transuraniumCost',
    'antimatterUpkeep', 'antimatterCost',
    'dimensionalEchoesUpkeep', 'dimensionalEchoesCost',
    'singularityCoresUpkeep', 'singularityCoresCost',
    'algaeUpkeep', 'algaeCost',
    'chipsUpkeep', 'chipsCost',
    'influenceUpkeep', 'influenceCost',
    'productionCost',
)
GLADIUS_RESOURCE_OUTPUT = (
    'biomass',
    'requisitions',
    'food',
    'ore',
    'energy',
    'influence',
    'production',
    'research',
    'loyalty',
    'populationLimit',
)
ZEPHON_RESOURCE_OUTPUT = (
    'food',
    'minerals',
    'energy',
    'transuranium',
    'antimatter',
    'dimensionalEchoes',
    'singularityCores',
    'algae',
    'chips',
    'influence',
    'production',
    'research',
    'loyalty',
    'populationLimit',
)

class Building(Obj):
    OBJ_CLASS = 'Buildings'

    def __init__(self, name: str):
        super().__init__(name)
        self.costNames: tuple
        self.outputNames: tuple
        self.resourceCosts: dict[str, str] = {}
        self.resourceOutput: dict[str, str] = {}
        self.traits: dict[str, str] = {}
        self.actions: dict[str, str] = {}

    def get_resource_costs(self):
        xmlStats: list = self.tree.find('modifiers').xpath('modifier[@visible]/effects/*')
        for resource in xmlStats:
            if resource.tag in self.costNames:
                self.resourceCosts[resource.tag] = resource.attrib.items()[0][1]

    def get_resource_output(self):
        xmlStats: list = self.tree.find('modifiers').xpath('modifier[not(@visible)]/effects/*')
        for resource in xmlStats:
            if resource.tag in self.outputNames:
                self.resourceOutput[resource.tag] = resource.attrib.items()[0][1]

    def get_traits(self):
        if self.GAME == 'Gladius':
            attrName = 'name'
        elif self.GAME == 'Zephon':
            attrName = 'type'
        try:
            for trait in self.tree.find('traits').iterfind('trait'):
                traitID = trait.get(attrName)
                traitName = ID2name(traitID, self.GAME, 'Traits')
                self.traits[traitName] = trait.get('requiredUpgrade')
        # no traits
        except AttributeError:
            pass

    def get_actions(self):
        try:
            for action in self.tree.find('actions'):
                tag = action.tag
                if tag == 'produceUnit':
                    actionName = f"Produce {ID2name(action.get('unit'), self.GAME, 'Units')}"
                elif tag == 'constructBuilding':
                    actionName = f"Construct {ID2name(action.get('building'), self.GAME, 'Buildings')}"
                elif tag == 'constructFeature':
                    actionName = f"Construct {ID2name(action.get('feature'), self.GAME, 'Features')}"
                else:
                    if (actionID := action.get('name')):
                        pass
                    elif (actionID := action.get('action')):
                        pass
                    else:
                        # Capitalizes first letter of tag
                        actionID = tag[0].upper() + tag[1:]
                    actionName = ID2name(actionID, self.GAME, 'Actions')
                if actionName:
                    self.actions[actionName] = action.get('requiredUpgrade')
        # no actions
        except TypeError:
            pass


class GBuilding(Gladius, Building):
    GAME = 'Gladius'

    def __init__(self, name: str):
        super().__init__(name)
        self.costNames = GLADIUS_RESOURCE_COSTS
        self.outputNames = GLADIUS_RESOURCE_OUTPUT
        self.factionAndID: str
        self.faction: str = 'Neutral'

    
class ZBuilding(Building):
    GAME = 'Zephon'

    def __init__(self, name: str):
        super().__init__(name)
        self.costNames = ZEPHON_RESOURCE_COSTS
        self.outputNames = ZEPHON_RESOURCE_OUTPUT
        self.branch = 'Neutral'

    def get_branch(self):
        self.branch = self.tree.getroot().get('branch')
        if not self.branch:
            self.branch = 'Neutral'
