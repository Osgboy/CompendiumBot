from dataclasses import dataclass
from obj import Obj
from trait import Trait

@dataclass#(slots=True)
class GWeaponStats:
    __slots__ = ['meleeAccuracy', 'rangedAccuracy', 'meleeAttacks', 'strengthDamage']
    meleeAccuracy: str
    rangedAccuracy: str
    meleeAttacks: str
    strengthDamage: str

class Weapon(Obj):
    def __init__(self, name: str, game: str):
        self.objClass = 'Weapons'
        super().__init__(name, game)
        self.attacks = '?'
        self.armorPen = '0'
        self.damage = '?'
        self.range = '?'
        self.accuracy = '6'
        self.traits = {}
    
    def get_weapon_traits(self):
        try:
            for trait in self.tree.find('traits').iterfind('trait'):
                if self.game == 'Gladius':
                    traitName = trait.get('name')
                elif self.game == 'Zephon':
                    traitName = trait.get('type')
                traitObj = Trait.from_internalID(traitName, self.game)
                self.traits[traitObj.name] = trait.get('requiredUpgrade')
        # no traits
        except AttributeError:
            pass

    def get_weapon_range(self):
        if 'Melee' in self.traits.keys():
            self.range = 'Melee'
        else:
            rangeMin = self.tree.find('target').get('rangeMin')
            rangeMax = self.tree.find('target').get('rangeMax')
            if rangeMin != None:
                self.range = str(rangeMin) + ' - ' + str(rangeMax)
            else:
                self.range = rangeMax

class GWeapon(Weapon):
    def __init__(self, name: str, game: str):
        super().__init__(name, game)
        self.unitStats: dataclass = GWeaponStats('6', '6', '1', '1')

    def get_weapon_stats(self):
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
            if prefix == 'melee':
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
                try:
                    operator, meleeDamageModifier = effects.find('meleeDamage').items()[0]
                    if operator == 'add':
                        meleeDamage = float(meleeDamageModifier) + strengthDamage
                    elif operator == 'base':
                        meleeDamage = float(meleeDamageModifier)
                except AttributeError:
                    meleeDamage = strengthDamage
                self.damage = '{0:.2f}'.format(meleeDamage)
            else:
                self.damage = effects.find('rangedDamage').items()[0][1]
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
    def __init__(self, name: str, game: str):
        super().__init__(name, game)

    def get_weapon_stats(self):
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
