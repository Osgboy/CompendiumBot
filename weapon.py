from dataclasses import dataclass
from obj import Obj, ID2name
from trait import Trait

@dataclass#(slots=True)
class GWeaponStats:
    __slots__ = ['meleeAccuracy', 'rangedAccuracy', 'meleeAttacks', 'strengthDamage']
    meleeAccuracy: str
    rangedAccuracy: str
    meleeAttacks: str
    strengthDamage: str

class Weapon(Obj):
    OBJ_CLASS = 'Weapons'

    def __init__(self, name: str):
        super().__init__(name)
        self.attacks = '?'
        self.armorPen = '0'
        self.damage = '?'
        self.range = '?'
        self.accuracy = '6'
        self.traits = {}
    
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

    def get_range(self):
        if 'Melee' in self.traits.keys():
            self.range = 'Melee'
        else:
            rangeMin = self.tree.find('target').get('rangeMin')
            rangeMax = self.tree.find('target').get('rangeMax')
            if rangeMin:
                self.range = rangeMin + ' - ' + rangeMax
            else:
                self.range = rangeMax

class GWeapon(Weapon):
    GAME = 'Gladius'

    def __init__(self, name: str):
        super().__init__(name)
        self.unitStats: dataclass = GWeaponStats('6', '6', '1', '1')

    def get_stats(self):
        try:
            effects = self.tree.find('modifiers').find('modifier').find('effects')
        except AttributeError:
            effects = None
        # Melee or ranged
        if 'Melee' in self.traits.keys():
            prefix = 'melee'
        else:
            prefix = 'ranged'
        # Attacks
        try:
            self.attacks = effects.find('attacks').items()[0][1]
        except AttributeError:
            if prefix == 'melee':
                self.attacks = self.unitStats.meleeAttacks
        # Armor penetration
        try:
            self.armorPen = effects.find(prefix + 'ArmorPenetration').items()[0][1]
        except AttributeError:
            pass
        # Damage
        try:
            strengthDamage = float(self.unitStats.strengthDamage)
            try:
                operator, strengthDamageModifier = effects.find('strengthDamage').items()[0]
                if operator == 'add':
                    strengthDamage += float(strengthDamageModifier)
                elif operator == 'mul':
                    strengthDamage += float(strengthDamageModifier) * strengthDamage
                elif operator == 'base':
                    strengthDamage = float(strengthDamageModifier)
            except AttributeError:
                pass
            damage = strengthDamage
            try:
                operator, damageTypeModifier = effects.find(prefix + 'Damage').items()[0]
                if operator == 'add':
                    damage += float(damageTypeModifier)
                elif operator == 'mul':
                    damage += float(damageTypeModifier) * strengthDamage
                elif operator == 'base':
                    damage = float(damageTypeModifier)
            except AttributeError:
                pass
            self.damage = '{0:.2f}'.format(damage)
        except AttributeError:
            pass
        # Accuracy
        try:
            operator, accuracyModifier = effects.find(prefix + 'Accuracy').items()[0]
            if operator == 'add':
                self.accuracy = str(int(getattr(self.unitStats, prefix + 'Accuracy')) + int(accuracyModifier))
            else:
                self.accuracy = accuracyModifier
        except AttributeError:
            self.accuracy = getattr(self.unitStats, prefix + 'Accuracy')

class ZWeapon(Weapon):
    GAME = 'Zephon'

    def __init__(self, name: str):
        super().__init__(name)

    def get_stats(self):
        try:
            effects = self.tree.find('modifiers').find('modifier').find('effects')
        except AttributeError:
            return
        try:
            self.attacks = effects.find('attacks').items()[0][1]
        except AttributeError:
            pass
        try:
            self.armorPen = effects.find('armorPenetration').items()[0][1]
        except AttributeError:
            pass
        try:
            self.damage = effects.find('damage').items()[0][1]
        except AttributeError:
            pass
        try:
            operator, accuracyModifier = effects.find('accuracy').items()[0]
            if operator == 'add':
                self.accuracy = str(int(self.accuracy) + int(accuracyModifier))
            else:
                self.accuracy = accuracyModifier
        except AttributeError:
            pass
