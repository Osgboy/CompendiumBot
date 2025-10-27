import json
import dataclasses
import traceback
from os.path import join as pathJoin
from os.path import normpath
from pathlib import Path
from typing import Type, Callable
from lxml import etree as ET
from obj import Obj, val2val, ID2name
from action import Action, GAction, ZAction
from building import Building, GBuilding, ZBuilding
from faction import Faction, GFaction, ZFaction
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
            # Get only object names by filtering out any flavor text like properties, victory text, quotes, etc.
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

    slots = ('internalID', 'tier', 'dlc', 'description', 'flavor',
             'costStats', 'upkeepStats', 'weapons', 'traits', 'actions')
    kwargs = {}
    kwargs['faction'] = camel_case_split(unit.faction)
    kwargs['combatStats'] = dataclasses.asdict(unit.combatStats)
    kwargs['weaponStats'] = dataclasses.asdict(unit.weaponStats)
    for key in slots:
        kwargs[key] = getattr(unit, key, None)
    return kwargs


def get_zunit_attrs(unit: ZUnit) -> dict:
    unit.get_branch()
    unit.get_tier()
    unit.get_stats()
    unit.get_weapons()
    unit.get_traits()
    unit.get_actions()

    slots = ('internalID', 'branch', 'tier', 'description', 'flavor',
             'costStats', 'upkeepStats', 'weapons', 'traits', 'actions')
    kwargs = {}
    kwargs['combatStats'] = dataclasses.asdict(unit.combatStats)
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
    kwargs['modifiers'] = None
    for key in slots:
        try:
            kwargs[key] = getattr(upgrade, key, None)
        except AttributeError:
            pass

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


def action_from_xml(actionCls: Type[Obj], objDict: dict, englishAction: ET.ElementBase, entry: ET.ElementBase) -> tuple[Type[Action], dict]:
    tag = entry.tag
    if not (actionID := entry.get('name')):
        # Capitalizes first letter of tag
        actionID = tag[0].upper() + tag[1:]
    actionName = ID2name(actionID, actionCls.GAME, 'Actions')
    if not actionName or actionName in objDict:
        # check faction
        return None, None
    action = actionCls(actionName)
    action.internalID = actionID
    if (model := entry.find('model')) is not None:
        entry.remove(model)
    action.tree = entry
    for e in englishAction:
        targetStr = e.get('name')
        if targetStr == actionID + 'Flavor':
            action.flavor = val2val(
                e.get('value'), action.ENGLISH_DIR)
        elif action.GAME == 'Gladius':
            if targetStr == actionID + 'Description':
                action.description = val2val(
                    e.get('value'), action.ENGLISH_DIR)
        elif action.GAME == 'Zephon':
            if targetStr == actionID + 'Properties':
                action.description = val2val(e.get('value'), action.ENGLISH_DIR).replace(
                    "<icon texture='GUI/Bullet'/>", '')
    action.get_cooldown()
    action.get_modifiers()
    action.get_raw_XML()
    action.get_icon_path()

    slots = ('internalID', 'description', 'cooldown',
            'flavor', 'modifiers', 'rawXML')
    kwargs = {}
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
    return action, kwargs


def get_unit_actions(actionCls: Type[Action], unitCls: Type[Unit]) -> dict:
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
                    if actionEntry.tag in unit.SKIPPED_ACTIONS:
                        continue
                    action, kwargs = action_from_xml(actionCls, objDict, englishAction, actionEntry)
                    if not action:
                        continue
                    action.get_conditions()
                    kwargs['conditions'] = dataclasses.asdict(
                        action.conditions)
                    objDict[kwargs['name']] = kwargs
        except Exception:
            print(
                f"Action {unitCls.__name__} {entry.get('name')} failed to convert.")
            # print(traceback.format_exc())
    return objDict


def get_faction_actions(actionCls: Type[Action], factionCls: Type[Faction]) -> dict:
    ENGLISH_DIR = pathJoin(actionCls.GAME, 'English')
    objDict = {}
    factionTree = ET.parse(pathJoin(factionCls.GAME, 'English', 'Factions.xml'), parser=ET.XMLParser(
        recover=True, remove_comments=True))
    englishFaction = factionTree.getroot()
    actionTree = ET.parse(pathJoin(actionCls.GAME, 'English', 'Actions.xml'), parser=ET.XMLParser(
        recover=True, remove_comments=True))
    englishAction = actionTree.getroot()
    for entry in englishFaction.iterdescendants('entry'):
        try:
            if all(x not in entry.get('name') for x in ('Flavor', 'Properties', 'Quote', 'Discovered', 'Defeated')):
                factionName = val2val(entry.get('value'), ENGLISH_DIR)
                faction = factionCls(val2val(factionName, ENGLISH_DIR))
                faction.get_obj_min_info(entry)
                factionActions = [faction.tree.find('actions'), faction.tree.find('buildingActions')]
                for actionElement in factionActions:
                    if actionElement is not None:
                        for actionEntry in actionElement:
                            action, kwargs = action_from_xml(actionCls, objDict, englishAction, actionEntry)
                            if not action:
                                continue
                            if action.GAME == 'Gladius':
                                kwargs['faction'] = factionName
                            elif action.GAME == 'Zephon':
                                faction.get_branch()
                                kwargs['branch'] = faction.branch
                            objDict[kwargs['name']] = kwargs
        except Exception:
            print(
                f"Faction {factionCls.__name__} {entry.get('name')} failed to convert.")
            print(traceback.format_exc())
    return objDict


def get_building_actions(actionCls: Type[Action], buildingCls: Type[Building]) -> dict:
    ENGLISH_DIR = pathJoin(actionCls.GAME, 'English')
    objDict = {}
    buildingTree = ET.parse(pathJoin(buildingCls.GAME, 'English', 'Buildings.xml'), parser=ET.XMLParser(
        recover=True, remove_comments=True))
    englishBuilding = buildingTree.getroot()
    actionTree = ET.parse(pathJoin(actionCls.GAME, 'English', 'Actions.xml'), parser=ET.XMLParser(
        recover=True, remove_comments=True))
    englishAction = actionTree.getroot()
    for entry in englishBuilding.iterdescendants('entry'):
        try:
            if all(x not in entry.get('name') for x in ('Flavor', 'Description', 'Properties')):
                buildingName = val2val(entry.get('value'), ENGLISH_DIR)
                building = buildingCls(val2val(buildingName, ENGLISH_DIR))
                building.get_obj_min_info(entry)
                assert building.tree is not None
                for actionEntry in building.tree.find('actions'):
                    action, kwargs = action_from_xml(actionCls, objDict, englishAction, actionEntry)
                    if not action:
                        continue
                    objDict[kwargs['name']] = kwargs
        except Exception:
            print(
                f"Faction {buildingCls.__name__} {entry.get('name')} failed to convert.")
            # print(traceback.format_exc())
    return objDict


def get_player_actions() -> dict:
    objDict = {}
    actionTree = ET.parse(pathJoin('Zephon', 'English', 'Actions.xml'), parser=ET.XMLParser(
        recover=True, remove_comments=True))
    englishAction = actionTree.getroot()
    playerActionTree = ET.parse(pathJoin('Zephon', 'Blueprints', 'ActionTypeManager.xml'), parser=ET.XMLParser(
        recover=True, remove_comments=True))
    for actionEntry in playerActionTree.find('actions'):
        action, kwargs = action_from_xml(ZAction, objDict, englishAction, actionEntry)
        if not action:
            continue
        kwargs['cooldown'] = '1'
        objDict[kwargs['name']] = kwargs
    return objDict


def get_blueprint_actions() -> dict:
    objDict = {}
    actionTree = ET.parse(pathJoin('Zephon', 'English', 'Actions.xml'), parser=ET.XMLParser(
        recover=True, remove_comments=True))
    englishAction = actionTree.getroot()

    actionDir = Path('Zephon', 'Blueprints', 'Actions')
    for path in actionDir.glob('*.xml'):
        blueprintAction = ET.parse(str(path), parser=ET.XMLParser(
            recover=True, remove_comments=True))
        actionEntry = blueprintAction.getroot()
        action, kwargs = action_from_xml(ZAction, objDict, englishAction, actionEntry)
        if not action:
            continue
        action.get_conditions()
        kwargs['conditions'] = dataclasses.asdict(
            action.conditions)
        objDict[kwargs['name']] = kwargs
    return objDict

GActionArgs = (
    (get_unit_actions, GUnit),
    (get_faction_actions, GFaction),
    (get_building_actions, GBuilding),
)
ZActionArgs = (
    (get_unit_actions, ZUnit),
    (get_faction_actions, ZFaction),
    (get_building_actions, ZBuilding),
)
dicts['GAction'] = {}
dicts['ZAction'] = {}
with open(pathJoin(OUTPUT_DIR, 'GAction.json'), 'w') as fout:
    for actionFunc, sourceCls in GActionArgs:
        dicts['GAction'].update(actionFunc(GAction, sourceCls))
    get_factions('GAction', ('GUnit', 'GBuilding'), 'faction', 'actions')
    json.dump(dicts['GAction'], fout, indent=4)

with open(pathJoin(OUTPUT_DIR, 'ZAction.json'), 'w') as fout:
    for actionFunc, sourceCls in ZActionArgs:
        dicts['ZAction'].update(actionFunc(ZAction, sourceCls))
    dicts['ZAction'].update(get_player_actions())
    dicts['ZAction'].update(get_blueprint_actions())
    get_factions('ZAction', ('ZUnit', 'ZBuilding'), 'branch', 'actions')
    json.dump(dicts['ZAction'], fout, indent=4)


# Get Zephon upgrades
def add_upgrade(objClsName: str, objName: str, upgradeStr: str):
    if upgradeStr in [upgrade['internalID'] for upgrade in dicts['ZUpgrade'].values()]:
        print(f'Skipping {upgradeStr}')
        return
    upgrade = ZUpgrade('placeholder')
    upgrade.internalID = upgradeStr
    print(f"Adding upgrade {upgradeStr}")
    upgrade.XMLPath = pathJoin(upgrade.CLASS_DIR, upgradeStr + '.xml')
    try:
        upgrade.tree = ET.parse(upgrade.XMLPath, parser=ET.XMLParser(
            recover=True, remove_comments=True))
    except OSError:
        print(f"{upgrade.XMLPath} not found")
        return
    
    kwargs = get_zupgrade_attrs(upgrade)
    obj: dict = dicts[objClsName][objName]
    kwargs['description'] = obj.get('description')
    kwargs['modifiers'] = obj.get('modifiers')
    kwargs['flavor'] = obj.get('flavor')
    kwargs['iconPath'] = obj.get('iconPath')
    kwargs['name'] = objName
    dicts['ZUpgrade'][objName] = kwargs


ZEPHON_CLASSES = {
    'ZBuilding',
    'ZFaction',
    'ZUnit',
    'ZWeapon',
}
for objClsName in ZEPHON_CLASSES:
    for obj, properties in dicts[objClsName].items(): # str, dict
        if 'actions' in properties:
            for action, upgrade in properties['actions'].items():
                if upgrade:
                    if action[:10] == 'Construct ':
                        if objClsName == 'ZBuilding':
                            add_upgrade('ZBuilding', action[10:], upgrade)
                        elif objClsName == 'ZUnit': # Engineer's bunker, radio telescope
                            add_upgrade('ZUnit', action[10:], upgrade)
                    elif action[:8] == 'Produce ':
                        add_upgrade('ZUnit', action[8:], upgrade)
                    else:
                        add_upgrade('ZAction', action, upgrade)
        if 'traits' in properties:
            for trait, upgrade in properties['traits'].items():
                if upgrade:
                    add_upgrade('ZTrait', trait, upgrade)
        if objClsName == 'ZUnit':
            if 'weapons' in properties:
                for weapon, weaponProperties in properties['weapons'].items():
                    if upgrade := weaponProperties['requiredUpgrade']:
                        add_upgrade('ZWeapon', weapon, upgrade)

with open(pathJoin(OUTPUT_DIR, 'ZUpgrade.json'), 'w') as fout:
    json.dump(dicts['ZUpgrade'], fout, indent=4)
