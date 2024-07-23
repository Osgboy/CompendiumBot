import discord

RARITY_COLORS = {
    'Common': discord.colour.Color.from_rgb(255, 255, 255),
    'Uncommon': discord.colour.Color.from_rgb(0, 191, 191),
    'Artefact': discord.colour.Color.from_rgb(191, 0, 191),
    'Rare': discord.colour.Color.from_rgb(191, 0, 191)
}
GLADIUS_FACTION_COLORS = {
    'Adeptus Mechanicus': discord.colour.Color.from_rgb(159, 38, 40),
    'Astra Militarum': discord.colour.Color.from_rgb(50, 73, 53),
    'Chaos Space Marines': discord.colour.Color.from_rgb(57, 75, 87),
    'Drukhari': discord.colour.Color.from_rgb(15, 69, 78),
    'Eldar': discord.colour.Color.from_rgb(52, 115, 121),
    'Necrons': discord.colour.Color.from_rgb(4, 83, 42),
    'Neutral': discord.colour.Color.from_rgb(255, 255, 255),
    'Orks': discord.colour.Color.from_rgb(70, 91, 24),
    'Sisters Of Battle': discord.colour.Color.from_rgb(87, 12, 12),
    'Space Marines': discord.colour.Color.from_rgb(75, 98, 98),
    'Tau': discord.colour.Color.from_rgb(46, 90, 106),
    'Tyranids': discord.colour.Color.from_rgb(99, 37, 103)
}
GLADIUS_ICONS = {
    'biomass': '<:Biomass:1240218802831233118>', 'requisitions': '<:Requisitions:1240222555588268032>',
    'food': '<:Food:1240218818660532317>', 'ore': '<:Ore:1240218839644377181>',
    'energy': '<:Energy:1240221846343782501>', 'influence': '<:Influence:1240218825836728341>',
    'production': '<:Production:1240330971514011668>',

    'armor': '<:Armor:1240218799832174703>', 'hitpoints': '<:Hitpoints:1240330759781482528>',
    'morale': '<:Morale:1240218836171493386>', 'movement': '<:Movement:1240222322770579487>',
    'cargoSlots': '<:CargoSlots:1240218804982775848>', 'itemSlots': '<:ItemSlots:1240218829280378912>',

    'damage': '<:Damage:1240218813123919893>', 'attacks': '<:Attacks:1240218801799434241>',
    'armorPenetration': '<:ArmorPenetration:1240218800855715840>', 'accuracy': '<:Accuracy:1240218797458063361>',
    'range': '<:Range:1240218850763477013>',

    'actions': '<:Actions:1240218798532071515>', 'cooldown': '<:Cooldown:1240218808224972800>',
    'transport': '<:Transport:1256002013037203587>'
}
ZEPHON_ICONS = {
    'food': '<:Food:1250986007537647687>', 'minerals': '<:Minerals:1250986099023806464>',
    'energy': '<:Energy:1250985795242954764>', 'influence': '<:Influence:1250986095739404339>',
    'algae': '<:Algae:1250981089540046929>', 'chips': '<:Chips:1250985791455494174>',
    'antimatter': '<:Antimatter:1250981090278117416>', 'dimensionalEchoes': '<:DimensionalEchoes:1250985794450227240>',
    'singularityCores': '<:SingularityCores:1250986245085986909>', 'transuranium': '<:Transuranium:1250986247086669937>',
    'production': '<:Production:1250986164626657383>',

    'groupSize': '<:GroupSize:1250986008606933012>',
    'armor': '<:Armor:1250981091125362788>', 'hitpoints': '<:Hitpoints:1250986009429282866>',
    'morale': '<:Morale:1250986099816530033>', 'movement': '<:Movement:1250986100621836400>',
    'cargoSlots': '<:CargoSlots:1250981096070582273>', 'itemSlots': '<:ItemSlots:1250986096616017961>',

    'damage': '<:Damage:1250985792197628004>', 'attacks': '<:Attacks:1250981093314662411>',
    'armorPenetration': '<:ArmorPenetration:1250981091917955193>', 'accuracy': '<:Accuracy:1250981087954468914>',
    'range': '<:Range:1250986241604849664>',

    'actions': '<:Actions:1250981088701186128>', 'turns': '<:Turns:1250986247896305776>',
    'transport': '<:Transport:1256002285536804936>'
}
GLADIUS_RESOURCES = (
    'biomass', 'requisitions', 'food', 'ore', 'energy', 'influence'
)
ZEPHON_RESOURCES = (
    'food', 'minerals', 'energy', 'transuranium', 'antimatter', 'dimensionalEchoes', 'singularityCores', 'algae', 'chips', 'influence'
)

def create_gaction_list(classDict: dict, *, faction: str = None, cooldown: str = None, condition: str = None, GUpgrade: str = None) -> str:
    actionList = []
    for action, attrs in classDict.items():
        if (
            (faction and faction != attrs['faction'])
            or (cooldown and cooldown != attrs['cooldown'])
            or (condition and attrs['conditions'][condition])
            or (GUpgrade and GUpgrade != attrs['conditions']['requiredUpgrade'])
        ):
            continue
        actionList.append(action)

    if actionList:
        return('\n'.join(actionList))
    else:
        return('No actions found to match given filters.')

def create_zaction_list(classDict: dict, *, branch: str = None, cooldown: str = None, condition: str = None, ZUpgrade: str = None) -> str:
    actionList = []
    for action, attrs in classDict.items():
        if (
            (branch and branch != attrs['branch'])
            or (cooldown and cooldown != attrs['cooldown'])
            or (condition and attrs['conditions'][condition])
            or (ZUpgrade and ZUpgrade != attrs['conditions']['requiredUpgrade'])
        ):
            continue
        actionList.append(action)

    if actionList:
        return('\n'.join(actionList))
    else:
        return('No actions found to match given filters.')

def create_gbuilding_list(classDict: dict, *, faction: str = None, GTrait: str = None) -> str:
    buildingList = []
    for building, attrs in classDict.items():
        if (
            (faction and faction != attrs['faction'])
            or (GTrait and GTrait not in attrs['traits'])
        ):
            continue
        buildingList.append(building)

    if buildingList:
        return('\n'.join(buildingList))
    else:
        return('No buildings found to match given filters.')

def create_zbuilding_list(classDict: dict, *, branch: str = None, ZTrait: str = None) -> str:
    buildingList = []
    for building, attrs in classDict.items():
        if (
            (branch and branch != attrs['branch'])
            or (ZTrait and ZTrait not in attrs['traits'])
        ):
            continue
        buildingList.append(building)

    if buildingList:
        return('\n'.join(buildingList))
    else:
        return('No buildings found to match given filters.')

def create_gitem_list(classDict: dict, *, rarity: str = None) -> str:
    itemList = []
    for item, attrs in classDict.items():
        if (
            (rarity and rarity != attrs['rarity'])
        ):
            continue
        itemList.append(item)

    if itemList:
        return('\n'.join(itemList))
    else:
        return('No items found to match given filters.')
    
def create_zitem_list(classDict: dict, *, branch: str = None, rarity: str = None, ZTrait: str = None) -> str:
    itemList = []
    for item, attrs in classDict.items():
        if (
            (branch and branch != attrs['branch'])
            or (rarity and rarity != attrs['rarity'])
            or (ZTrait and ZTrait != attrs['buyCondition'])
        ):
            continue
        itemList.append(item)

    if itemList:
        return('\n'.join(itemList))
    else:
        return('No items found to match given filters.')

def create_gtrait_list(classDict: dict, *, faction: str = None) -> str:
    traitList = []
    for trait, attrs in classDict.items():
        if (
            (faction and faction != attrs['faction'])
        ):
            continue
        traitList.append(trait)

    if traitList:
        return('\n'.join(traitList))
    else:
        return('No traits found to match given filters.')
    
def create_ztrait_list(classDict: dict, *, branch: str = None) -> str:
    traitList = []
    for trait, attrs in classDict.items():
        if (
            (branch and branch != attrs['branch'])
        ):
            continue
        traitList.append(trait)

    if traitList:
        return('\n'.join(traitList))
    else:
        return('No traits found to match given filters.')

def create_gunit_list(classDict: dict, *, faction: str = None, dlc: str = None, GWeapon: str = None, GTrait: str = None, GAction: str = None) -> str:
    unitList = []
    for unit, attrs in classDict.items():
        if (
            (faction and faction != attrs['faction'])
            or (dlc and dlc != attrs['dlc'])
            or (GWeapon and GWeapon not in attrs['weapons'])
            or (GTrait and GTrait not in attrs['traits'])
            or (GAction and GAction not in attrs['actions'])
        ):
            continue
        unitList.append(unit)

    if unitList:
        return('\n'.join(unitList))
    else:
        return('No units found to match given filters.')

def create_zunit_list(classDict: dict, *, branch: str = None, ZWeapon: str = None, ZTrait: str = None, ZAction: str = None) -> str:
    unitList = []
    for unit, attrs in classDict.items():
        if (
            (branch and branch != attrs['branch'])
            or (ZWeapon and ZWeapon not in attrs['weapons'])
            or (ZTrait and ZTrait not in attrs['traits'])
            or (ZAction and ZAction not in attrs['actions'])
        ):
            continue
        unitList.append(unit)

    if unitList:
        return('\n'.join(unitList))
    else:
        return('No units found to match given filters.')

def create_gweapon_list(classDict: dict, *, faction: str = None, GTrait: str = None, range: str = None) -> str:
    weaponList = []
    for weapon, attrs in classDict.items():
        if (
            (faction and faction != attrs['faction'])
            or (GTrait and GTrait not in attrs['traits'])
            or (range and range != attrs['range'])
        ):
            continue
        weaponList.append(weapon)

    if weaponList:
        return('\n'.join(weaponList))
    else:
        return('No weapons found to match given filters.')

def create_zweapon_list(classDict: dict, *, branch: str = None, ZTrait: str = None, range: str = None) -> str:
    weaponList = []
    for weapon, attrs in classDict.items():
        if (
            (branch and branch != attrs['branch'])
            or (ZTrait and ZTrait not in attrs['traits'])
            or (range and range != attrs['range'])
        ):
            continue
        weaponList.append(weapon)

    if weaponList:
        return('\n'.join(weaponList))
    else:
        return('No weapons found to match given filters.')