from dataclasses import dataclass
from obj import Obj, ID2name


@dataclass  # (slots=True)
class GUnitWeaponStats:
    __slots__ = ['meleeAccuracy', 'rangedAccuracy',
                 'meleeAttacks', 'strengthDamage']
    meleeAccuracy: float
    rangedAccuracy: float
    meleeAttacks: float
    strengthDamage: float


@dataclass  # (slots=True)
class WeaponFinalStats:
    __slots__ = ['attacks', 'armorPen',
                 'damage', 'accuracy']
    attacks: float
    armorPen: int
    damage: float
    accuracy: int


class Weapon(Obj):
    OBJ_CLASS = 'Weapons'

    def __init__(self, name: str):
        super().__init__(name)
        self.range: str = 'N/A'
        self.innateStats: dict[str, dict] = {}
        self.finalStats: dataclass = WeaponFinalStats(1, 0, 0, 6)
        self.traits = {}

    def get_traits(self):
        if self.GAME == 'Gladius':
            attrName = 'name'
        elif self.GAME == 'Zephon':
            attrName = 'type'
        if (xmlTraits := self.tree.find('traits')) is not None:
            for trait in xmlTraits.iterfind('trait'):
                traitID = trait.get(attrName)
                traitName = ID2name(traitID, self.GAME, 'Traits')
                self.traits[traitName] = trait.get('requiredUpgrade')

    def get_range(self):
        if 'Melee' in self.traits.keys():
            self.range = 'Melee'
        else:
            try:
                rangeMin = self.tree.find('target').get('rangeMin')
                rangeMax = self.tree.find('target').get('rangeMax')
                if rangeMin:
                    self.range = rangeMin + ' - ' + rangeMax
                else:
                    self.range = rangeMax
            except AttributeError:
                pass

    def get_innate_stats(self):
        try:
            effects = self.tree.find('modifiers').find(
                'modifier').find('effects')
        except AttributeError:
            return
        for stat in effects:
            operator, value = stat.attrib.items()[0]
            self.innateStats[stat.tag] = {
                'operator': operator, 'value': float(value)}

    def _operate(self, operand1, key) -> float:
        try:
            operator = self.innateStats[key]['operator']
            operand2 = self.innateStats[key]['value']
            if operator in ('base', 'min', 'max'):
                return operand2
            elif operator == 'add':
                return operand1 + operand2
            elif operator == 'mul':
                return operand1 * (1 + operand2)
        except KeyError:
            return operand1


class GWeapon(Weapon):
    GAME = 'Gladius'

    def __init__(self, name: str):
        super().__init__(name)
        self.unitStats: dataclass = GUnitWeaponStats(6, 6, 1, 1)

    def calculate_final_stats(self):
        # Melee or ranged
        if self.range == 'Melee':
            prefix = 'melee'
        else:
            prefix = 'ranged'
        # Attacks
        if prefix == 'melee':
            self.finalStats.attacks = self._operate(
                self.unitStats.meleeAttacks, 'meleeAttacks')
        self.finalStats.attacks = self._operate(0, 'attacks')
        # Armor penetration
        self.finalStats.armorPen = int(
            self._operate(0, prefix + 'ArmorPenetration'))
        # Damage
        strengthDamage = self._operate(
            self.unitStats.strengthDamage, 'strengthDamage')
        damage = self._operate(strengthDamage, prefix + 'Damage')
        self.finalStats.damage = '{0:.2f}'.format(damage)
        # Accuracy
        accuracy = self._operate(getattr(self.unitStats, prefix +
                                         'Accuracy'), prefix + 'Accuracy')
        self.finalStats.accuracy = int(accuracy)


class ZWeapon(Weapon):
    GAME = 'Zephon'

    def __init__(self, name: str):
        super().__init__(name)
        self.unitAccuracy = 6

    def calculate_final_stats(self):
        self.finalStats.attacks = self._operate(
            self.finalStats.attacks, 'attacks')
        self.finalStats.armorPen = int(self._operate(
            self.finalStats.armorPen, 'armorPenetration'))
        self.finalStats.damage = self._operate(
            self.finalStats.damage, 'damage')
        self.finalStats.accuracy = int(self._operate(
            self.unitAccuracy, 'accuracy'))
