from lxml import etree as ET
from os.path import join as pathJoin
from os.path import normpath
from obj import val2val, ID2name
from weapon import GWeapon, ZWeapon


class Gladius():
    def get_obj_info(self, classTree: ET._ElementTree, entry: ET.ElementBase):
        self.factionAndID = entry.get('name')
        if '/' in self.factionAndID:
            self.faction, self.internalID = self.factionAndID.split('/')
        else:
            self.internalID = self.factionAndID
        self.XMLPath = pathJoin(
            self.CLASS_DIR, normpath(self.factionAndID) + '.xml')
        self.tree = ET.parse(self.XMLPath, parser=ET.XMLParser(
            recover=True, remove_comments=True))
        for e in classTree.getroot():
            targetStr = e.get('name')
            if targetStr == self.factionAndID + 'Description':
                self.description = val2val(e.get('value'), self.ENGLISH_DIR)
            elif targetStr == self.factionAndID + 'Flavor':
                self.flavor = val2val(e.get('value'), self.ENGLISH_DIR)


class Modifiers():
    def get_modifiers(self):
        from trait import GTrait, ZTrait
        for effects in self.tree.iter('effects'):
            for effect in effects:
                tag = effect.tag
                if tag == 'addTrait':
                    traitID = effect.get('name') or effect.get('type')
                    duration = effect.get('duration')
                    traitStr = ID2name(traitID, self.GAME,
                                       'Traits')  # Trait name
                    if duration == '1':
                        traitStr += ' (1 turn)'
                    elif duration:
                        traitStr += f" ({duration} turns)"
                    self.modifiers.append(traitStr)
                    if self.GAME == 'Gladius':
                        appliedTrait = GTrait('placeholder')
                    elif self.GAME == 'Zephon':
                        appliedTrait = ZTrait('placeholder')
                    appliedTrait.tree = ET.parse(pathJoin(appliedTrait.CLASS_DIR, traitID + '.xml'), parser=ET.XMLParser(
                        recover=True, remove_comments=True))
                    appliedTrait.get_modifiers()
                    self.modifiers.extend(appliedTrait.modifiers)
                elif tag == 'weaponDamage':
                    weaponID = effect.get('name') or effect.get('weapon')
                    if weaponID is None:
                        continue
                    self.modifiers.append(
                        ID2name(weaponID, self.GAME, 'Weapons'))  # Weapon name
                    if self.GAME == 'Gladius':
                        appliedWeapon = GWeapon('placeholder')
                    elif self.GAME == 'Zephon':
                        appliedWeapon = ZWeapon('placeholder')
                    appliedWeapon.tree = ET.parse(pathJoin(appliedWeapon.CLASS_DIR, weaponID + '.xml'), parser=ET.XMLParser(
                        recover=True, remove_comments=True))
                    appliedWeapon.get_innate_stats()
                    appliedWeapon.calculate_final_stats()
                    for stat in appliedWeapon.finalStats.__slots__:
                        self.modifiers.append(
                            f"- {stat}: {getattr(appliedWeapon.finalStats, stat)}")
                elif tag == 'addUnit':
                    unitID = effect.get('name') or effect.get('type')
                    self.modifiers.append(
                        f"Spawn {ID2name(unitID, self.GAME, 'Units')} (Level 1)")  # Unit name
                else:
                    attributeXMLPath = pathJoin(
                        self.ENGLISH_DIR, 'Attributes.xml')
                    tree = ET.parse(attributeXMLPath, parser=ET.XMLParser(
                        recover=True, remove_comments=True))
                    attribute = tag[0].upper() + tag[1:]
                    for entry in tree.iter('entry'):
                        targetStr = entry.get('name') or entry.get('type')
                        if targetStr == attribute:
                            descriptor = entry.get('value')
                            break
                    else:
                        continue
                    operator, value = effect.attrib.items()[0]
                    try:
                        value = int(value)
                        percent = False
                    except ValueError:
                        value = float(value)
                        percent = True
                    if operator == 'add':
                        prefix = f"- {value:+{'.0%' if percent else ''}} "
                    elif operator == 'mul':
                        prefix = f"- {value:+{'.0%' if percent else ''}} "
                    elif operator == 'min':
                        prefix = f"- min {value:{'.0%' if percent else ''}} "
                    elif operator == 'max':
                        prefix = f"- max {value:{'.0%' if percent else ''}} "
                    elif operator == 'addMin':
                        addMax = effect.get('addMax')
                        try:
                            addMax = int(addMax)
                        except ValueError:
                            addMax = float(addMax)
                        prefix = f"- {value:+{'.0%' if percent else ''}}...{addMax:+{'.0%' if percent else ''}} "
                    elif operator == 'mulMin':
                        mulMax = effect.get('mulMax')
                        try:
                            mulMax = int(mulMax)
                        except ValueError:
                            mulMax = float(mulMax)
                        prefix = f"- {value:+{'.0%' if percent else ''}}...{mulMax:+{'.0%' if percent else ''}} "
                    else:
                        continue
                    self.modifiers.append(prefix + descriptor)
