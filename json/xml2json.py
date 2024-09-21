import json
import dataclasses
import traceback
from os.path import join as pathJoin
from os.path import normpath
from typing import Type, Callable
from lxml import etree as ET
from obj import Obj, val2val, ID2name
from action import Action, GAction, ZAction
from building import GBuilding, ZBuilding
from faction import GFaction, ZFaction
from item import GItem, ZItem
from trait import GTrait, ZTrait
from unit import Unit, GUnit, ZUnit
from upgrade import GUpgrade, ZUpgrade
from weapon import GWeapon, ZWeapon

OUTPUT_DIR = pathJoin('json')
dicts = {}


def camel_case_split(s: str) -> str:
    # use map to add an underscore before each uppercase letter
    modified_string = list(map(lambda x: '_' + x if x.isupper() else x, s))
    # join the modified string and split it at the underscores
    split_string = ''.join(modified_string).split('_')
    # remove any empty strings from the list
    split_string = list(filter(lambda x: x != '', split_string))
    split_string = ' '.join(split_string)
    return split_string


def main(getAttrs: Callable[[Obj], dict], objCls: Type[Obj]) -> dict:
    ENGLISH_DIR = pathJoin(objCls.GAME, 'English')
    objDict = {}
    tree = ET.parse(pathJoin(objCls.GAME, 'English', objCls.OBJ_CLASS + '.xml'), parser=ET.XMLParser(
        recover=True, remove_comments=True))
    for entry in tree.iter('entry'):
        try:
            if (all(x not in entry.get('name') for x in ('Flavor', 'Description', 'Properties')) and
                (objCls != GFaction or all(x not in entry.get('name') for x in ('Discovered', 'Defeated'))) and
                (objCls != ZFaction or 'Quote' not in entry.get('name'))):
                name = val2val(entry.get('value'), ENGLISH_DIR)
                obj = objCls(val2val(name, ENGLISH_DIR))
                obj.get_obj_info(tree, entry)
                assert obj.tree is not None
                kwargs = getAttrs(obj)
                obj.get_icon_path()
                try:
                    if not (internalPath := obj.iconPath):
                        raise AttributeError
                except AttributeError:
                    try:
                        internalPath = pathJoin(
                            obj.OBJ_CLASS, obj.factionAndID)
                    except AttributeError:
                        internalPath = pathJoin(obj.OBJ_CLASS, obj.internalID)
                kwargs['iconPath'] = pathJoin(
                    obj.GAME, 'Icons', normpath(internalPath) + '.png')
                kwargs['name'] = name
                objDict[name] = kwargs
        except Exception:
            print(f"{objCls.__name__} {entry.get('name')} failed to convert.")
            # print(traceback.format_exc())
    return objDict


def get_gbuilding_attrs(building: GBuilding) -> dict:
    building.get_resource_costs()
    building.get_resource_output()
    building.get_traits()
    building.get_actions()

    slots = ('internalID', 'description', 'flavor',
             'resourceCosts', 'resourceOutput', 'traits', 'actions')
    kwargs = {}
    kwargs['faction'] = camel_case_split(building.faction)
    for key in slots:
        kwargs[key] = getattr(building, key, None)
    return kwargs


def get_zbuilding_attrs(building: ZBuilding) -> dict:
    building.get_branch()
    building.get_resource_costs()
    building.get_resource_output()
    building.get_traits()
    building.get_actions()

    slots = ('internalID', 'branch', 'description', 'flavor',
             'resourceCosts', 'resourceOutput', 'traits', 'actions')
    kwargs = {}
    for key in slots:
        kwargs[key] = getattr(building, key, None)
    return kwargs


def get_gfaction_attrs(faction: GFaction) -> dict:
    faction.get_actions()
    faction.get_starting_units()
    faction.get_traits()

    slots = ('internalID', 'description', 'flavor', 'actions', 'startingUnits', 'traits')
    kwargs = {}
    for key in slots:
        kwargs[key] = getattr(faction, key, None)
    return kwargs


def get_zfaction_attrs(faction: ZFaction) -> dict:
    faction.get_branch()
    faction.get_actions()
    faction.get_starting_units()
    faction.get_traits()
    faction.get_liked_labels()
    faction.get_disliked_labels()

    slots = ('internalID', 'description', 'flavor', 'branch', 'actions', 'startingUnits', 'traits', 'likedLabels', 'dislikedLabels')
    kwargs = {}
    for key in slots:
        kwargs[key] = getattr(faction, key, None)
    return kwargs


def get_gitem_attrs(item: GItem) -> dict:
    item.get_rarity()
    item.get_influence_cost()
    item.get_modifiers()
    item.get_raw_XML()

    slots = ('internalID', 'description', 'flavor',
             'rarity', 'influenceCost', 'modifiers', 'rawXML')
    kwargs = {}
    for key in slots:
        kwargs[key] = getattr(item, key, None)
    return kwargs


def get_zitem_attrs(item: ZItem) -> dict:
    item.get_branch()
    item.get_rarity()
    item.get_influence_cost()
    item.get_buy_condition()
    item.get_modifiers()
    item.get_raw_XML()

    slots = ('internalID', 'branch', 'description', 'flavor',
             'rarity', 'influenceCost', 'buyCondition', 'modifiers', 'rawXML')
    kwargs = {}
    for key in slots:
        kwargs[key] = getattr(item, key, None)
    return kwargs


def get_gtrait_attrs(trait: GTrait) -> dict:
    trait.get_modifiers()
    trait.get_raw_XML()

    slots = ('internalID', 'description', 'flavor', 'modifiers', 'rawXML')
    kwargs = {}
    if trait.faction:
        kwargs['faction'] = camel_case_split(trait.faction)
    for key in slots:
        kwargs[key] = getattr(trait, key, None)
    return kwargs


def get_ztrait_attrs(trait: ZTrait) -> dict:
    trait.get_modifiers()
    trait.get_raw_XML()

    slots = ('internalID', 'description', 'flavor', 'modifiers', 'rawXML')
    kwargs = {}
    for key in slots:
        kwargs[key] = getattr(trait, key, None)

    return kwargs


def get_gunit_attrs(unit: GUnit) -> dict:
    unit.get_tier()
    unit.get_dlc()
    unit.get_stats()
    unit.get_weapon_stats()
    unit.get_group_size()
    unit.get_weapons()
    unit.get_traits()
    unit.get_actions()

    slots = ('internalID', 'tier', 'dlc', 'description',
             'flavor', 'weapons', 'traits', 'actions')
    kwargs = {}
    kwargs['faction'] = camel_case_split(unit.faction)
    kwargs['combatStats'] = dataclasses.asdict(unit.combatStats)
    kwargs['resourceStats'] = dataclasses.asdict(unit.resourceStats)
    kwargs['weaponStats'] = dataclasses.asdict(unit.weaponStats)
    for key in slots:
        kwargs[key] = getattr(unit, key, None)
    return kwargs


def get_zunit_attrs(unit: ZUnit) -> dict:
    unit.get_branch()
    unit.get_stats()
    unit.get_weapons()
    unit.get_traits()
    unit.get_actions()

    slots = ('internalID', 'branch', 'description',
             'flavor', 'weapons', 'traits', 'actions')
    kwargs = {}
    kwargs['combatStats'] = dataclasses.asdict(unit.combatStats)
    kwargs['resourceStats'] = dataclasses.asdict(unit.resourceStats)
    for key in slots:
        kwargs[key] = getattr(unit, key, None)
    return kwargs


def get_gupgrade_attrs(upgrade: GUpgrade) -> dict:
    upgrade.get_dlc()
    upgrade.get_tier()
    upgrade.get_required_upgrades()

    slots = ('internalID', 'dlc', 'description',
             'flavor', 'tier', 'requiredUpgrades')
    kwargs = {}
    kwargs['faction'] = camel_case_split(upgrade.faction)
    for key in slots:

        kwargs[key] = getattr(upgrade, key, None)
    return kwargs


def get_zupgrade_attrs(upgrade: ZUpgrade) -> dict:
    upgrade.get_branch()
    upgrade.get_faction()
    upgrade.get_tier()
    upgrade.get_required_upgrades()

    slots = ('internalID', 'branch', 'description',
             'flavor', 'tier', 'requiredUpgrades')
    kwargs = {}
    kwargs['faction'] = camel_case_split(upgrade.faction)
    for key in slots:
        kwargs[key] = getattr(upgrade, key, None)

    return kwargs


def get_gweapon_attrs(weapon: GWeapon) -> dict:
    weapon.get_traits()
    weapon.get_range()
    weapon.get_innate_stats()

    slots = ('internalID', 'description', 'flavor',
             'traits', 'range', 'innateStats')
    kwargs = {}
    for key in slots:
        kwargs[key] = getattr(weapon, key, None)
    return kwargs


def get_zweapon_attrs(weapon: ZWeapon) -> dict:
    weapon.get_traits()
    weapon.get_range()
    weapon.get_innate_stats()

    slots = ('internalID', 'description', 'flavor',
             'traits', 'range', 'innateStats')
    kwargs = {}
    for key in slots:
        kwargs[key] = getattr(weapon, key, None)
    return kwargs


def get_factions(objDict: str, sourceDicts: tuple[str], faction: str, objType: str):
    objDict = dicts[objDict]
    blank = set()
    for k, v in objDict.items():
        if faction not in v:
            blank.add(k)
    for sourceDict in sourceDicts:
        for sourceName, sourceAttrs in dicts[sourceDict].items():
            if sourceDict == 'ZItem':
                if sourceName in blank:
                    objDict[sourceName][faction] = sourceAttrs[faction]
            else:
                for o in sourceAttrs[objType]:
                    if o in blank:
                        try:
                            if objDict[o][faction] != sourceAttrs[faction]:
                                objDict[o][faction] = 'Neutral'
                        except KeyError:
                            objDict[o][faction] = sourceAttrs[faction]
    for v in objDict.values():
        if faction not in v:
            v[faction] = 'Neutral'

# mainArgs order must place factionArgs[0] after anything in factionArgs[1]
mainArgs = {
    get_gbuilding_attrs: GBuilding,
    get_zbuilding_attrs: ZBuilding,
    get_gunit_attrs: GUnit,
    get_zunit_attrs: ZUnit,
    get_gfaction_attrs: GFaction,
    get_zfaction_attrs: ZFaction,
    get_gitem_attrs: GItem,
    get_zitem_attrs: ZItem,
    get_gupgrade_attrs: GUpgrade,
    get_zupgrade_attrs: ZUpgrade,
    get_gweapon_attrs: GWeapon,
    get_zweapon_attrs: ZWeapon,
    get_gtrait_attrs: GTrait,
    get_ztrait_attrs: ZTrait,
}
factionArgs = {
    GTrait: ('GTrait', ('GUnit', 'GWeapon'), 'faction', 'traits'),
    ZTrait: ('ZTrait', ('ZUnit', 'ZWeapon', 'ZItem'), 'branch', 'traits'),
    GWeapon: ('GWeapon', ('GUnit',), 'faction', 'weapons'),
    ZWeapon: ('ZWeapon', ('ZUnit',), 'branch', 'weapons'),
}
for getAttrs, objCls in mainArgs.items():
    with open(pathJoin(OUTPUT_DIR, objCls.__name__ + '.json'), 'w') as fout:
        dicts[objCls.__name__] = main(getAttrs, objCls)
        if objCls in factionArgs:
            args = factionArgs[objCls]
            get_factions(*args)
        json.dump(dicts[objCls.__name__], fout, indent=4)


def get_action_attrs(actionCls: Type[Action], unitCls: Type[Unit]) -> dict:
    ENGLISH_DIR = pathJoin(actionCls.GAME, 'English')
    objDict = {}
    unitTree = ET.parse(pathJoin(unitCls.GAME, 'English', 'Units.xml'), parser=ET.XMLParser(
        recover=True, remove_comments=True))
    englishUnit = unitTree.getroot()
    actionTree = ET.parse(pathJoin(actionCls.GAME, 'English', 'Actions.xml'), parser=ET.XMLParser(
        recover=True, remove_comments=True))
    englishAction = actionTree.getroot()
    for entry in englishUnit.iterdescendants('entry'):
        try:
            if all(x not in entry.get('name') for x in ('Flavor', 'Description', 'Properties')):
                unitName = val2val(entry.get('value'), ENGLISH_DIR)
                unit = unitCls(val2val(unitName, ENGLISH_DIR))
                unit.get_obj_min_info(entry)
                assert unit.tree is not None
                for actionEntry in unit.tree.find('actions'):
                    if (tag := actionEntry.tag) in unit.SKIPPED_ACTIONS:
                        continue
                    if not (actionID := actionEntry.get('name')):
                        # Capitalizes first letter of tag
                        actionID = tag[0].upper() + tag[1:]
                    actionName = ID2name(actionID, unit.GAME, 'Actions')
                    if not actionName or actionName in objDict:
                        # check faction
                        continue
                    action = actionCls(actionName)
                    action.internalID = actionID
                    if (model := actionEntry.find('model')) is not None:
                        actionEntry.remove(model)
                    action.tree = actionEntry
                    for e in englishAction:
                        targetStr = e.get('name')
                        if targetStr == actionID + 'Flavor':
                            action.flavor = val2val(
                                e.get('value'), ENGLISH_DIR)
                        elif action.GAME == 'Gladius':
                            if targetStr == actionID + 'Description':
                                action.description = val2val(
                                    e.get('value'), ENGLISH_DIR)
                        elif action.GAME == 'Zephon':
                            if targetStr == actionID + 'Properties':
                                action.description = val2val(e.get('value'), ENGLISH_DIR).replace(
                                    "<icon texture='GUI/Bullet'/>", '')
                    action.get_cooldown()
                    action.get_conditions()
                    action.get_modifiers()
                    action.get_raw_XML()
                    action.get_icon_path()

                    slots = ('internalID', 'description',
                             'flavor', 'modifiers', 'rawXML')
                    kwargs = {}
                    if action.passive:
                        kwargs['cooldown'] = 'Passive'
                    else:
                        kwargs['cooldown'] = action.cooldown
                    kwargs['conditions'] = dataclasses.asdict(
                        action.conditions)
                    for key in slots:
                        kwargs[key] = getattr(action, key, None)
                    try:
                        if not (internalPath := action.iconPath):
                            raise AttributeError
                    except AttributeError:
                        try:
                            internalPath = pathJoin(
                                action.OBJ_CLASS, action.factionAndID)
                        except AttributeError:
                            internalPath = pathJoin(
                                action.OBJ_CLASS, action.internalID)
                    kwargs['iconPath'] = pathJoin(
                        action.GAME, 'Icons', normpath(internalPath) + '.png')
                    kwargs['name'] = actionName
                    objDict[actionName] = kwargs
        except Exception:
            print(
                f"Action {unitCls.__name__} {entry.get('name')} failed to convert.")
            # print(traceback.format_exc())
    return objDict


for actionCls, unitCls, faction in ((GAction, GUnit, 'faction'), (ZAction, ZUnit, 'branch')):
    with open(pathJoin(OUTPUT_DIR, actionCls.__name__ + '.json'), 'w') as fout:
        dicts[actionCls.__name__] = get_action_attrs(actionCls, unitCls)
        get_factions(actionCls.__name__,
                     (unitCls.__name__,), faction, 'actions')
        json.dump(dicts[actionCls.__name__], fout, indent=4)
