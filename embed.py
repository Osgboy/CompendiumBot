import discord


DLCS = {
    'None': 'None',
    'Supplement1': 'Reinforcement Pack',
    'Supplement2': 'Tyranids',
    'Supplement3': 'Chaos Space Marines',
    'Supplement4': 'Fortification Pack',
    'Supplement5': 'Tau',
    'Supplement6': 'Assault Pack',
    'Supplement7': 'Eldar',
    'Supplement8': 'Specialist Pack',
    'Supplement9': 'Adeptus Mechanicus',
    'Supplement10': 'Escalation Pack',
    'Supplement11': 'Adepta Sororitas',
    'Supplement12': 'Firepower Pack',
    'Supplement13': 'Drukhari',
    'Supplement14': 'Demolition Pack',
    'LordOfSkulls': 'Lord of Skulls'
}
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
ZEPHON_BRANCH_COLORS = {
    'Cyber': discord.colour.Color.from_rgb(16, 121, 130),
    'Human': discord.colour.Color.from_rgb(154, 129, 35),
    'Voice': discord.colour.Color.from_rgb(123, 65, 150),
    'Zephon': discord.colour.Color.from_rgb(205, 59, 66),
    'Reaver': discord.colour.Color.from_rgb(138, 97, 70),
    'Acrin': discord.colour.Color.from_rgb(62, 192, 158),
    'Neutral': discord.colour.Color.from_rgb(255, 255, 255)
}
GLADIUS_ICONS = {
    'biomass': '<:Biomass:1240218802831233118>', 'requisitions': '<:Requisitions:1240222555588268032>',
    'food': '<:Food:1240218818660532317>', 'ore': '<:Ore:1240218839644377181>',
    'energy': '<:Energy:1240221846343782501>', 'influence': '<:Influence:1240218825836728341>',
    'production': '<:Production:1240330971514011668>', 'research': '<:Research:1240218854152601640>',
    'loyalty': '<:Loyalty:1240222250230353921>', 'populationLimit': '<:PopulationLimit:1240218843138228284>',

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
    'production': '<:Production:1250986164626657383>', 'research': '<:Research:1250986242653556799>',
    'loyalty': '<:Loyalty:1250986098272894986>', 'populationLimit': '<:PopulationLimit:1250986103188750406>',

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


def operate(operand1: float, weaponStats: dict, key: str) -> float:
    try:
        operator = weaponStats[key]['operator']
        operand2 = weaponStats[key]['value']
    except KeyError:
        return operand1
    if operator in ('base', 'min', 'max'):
        return operand2
    elif operator == 'add':
        return operand1 + operand2
    elif operator == 'mul':
        return operand1 * (1 + operand2)


def calculate_gweapon_stats(range: str, weaponStats: dict,
                            unitStats: dict = {'meleeAccuracy': 6, 'rangedAccuracy': 6, 'meleeAttacks': 1, 'strengthDamage': 1}) -> dict:
    finalStats = {'attacks': 1, 'armorPen': 0, 'damage': 0, 'accuracy': 6}
    # Melee or ranged
    if range == 'Melee':
        prefix = 'melee'
    else:
        prefix = 'ranged'
    # Attacks
    if prefix == 'melee':
        finalStats['attacks'] = operate(
            unitStats['meleeAttacks'], weaponStats, 'meleeAttacks')
    finalStats['attacks'] = operate(
        finalStats['attacks'], weaponStats, 'attacks')
    # Armor penetration
    finalStats['armorPen'] = int(
        operate(finalStats['armorPen'], weaponStats, prefix + 'ArmorPenetration'))
    # Damage
    strengthDamage = operate(unitStats['strengthDamage'],
                             weaponStats, 'strengthDamage')
    damage = operate(strengthDamage, weaponStats, prefix + 'Damage')
    finalStats['damage'] = '{0:.2f}'.format(damage)
    # Accuracy
    accuracy = operate(unitStats[prefix + 'Accuracy'],
                       weaponStats, prefix + 'Accuracy')
    finalStats['accuracy'] = int(accuracy)
    return finalStats


def calculate_zweapon_stats(weaponStats: dict, unitAccuracy: int = 6) -> dict:
    finalStats = {'attacks': 0, 'armorPen': 0,
                  'damage': 0, 'accuracy': 6}
    finalStats['attacks'] = operate(
        finalStats['attacks'], weaponStats, 'attacks')
    finalStats['armorPen'] = int(operate(
        finalStats['armorPen'], weaponStats, 'armorPenetration'))
    finalStats['damage'] = operate(
        finalStats['damage'], weaponStats, 'damage')
    finalStats['accuracy'] = int(operate(
        unitAccuracy, weaponStats, 'accuracy'))
    return finalStats


def create_gaction_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)
    
    # Color
    embed.colour = GLADIUS_FACTION_COLORS[attrs['faction']]

    # Faction
    embed.add_field(name='Faction', value=attrs['faction'])

    # Cooldown
    if attrs['cooldown'] == 'Passive':
        embed.add_field(name='Cooldown', value='Passive', inline=False)
    else:
        embed.add_field(
            name='Cooldown', value=f"{GLADIUS_ICONS['cooldown']} {attrs['cooldown']}", inline=False)

    # Conditions
    embed.add_field(name=f"Required upgrade", value=str(
        attrs['conditions']['requiredUpgrade']))
    embed.add_field(name=f"Requires {GLADIUS_ICONS['actions']} AP?", value=str(
        attrs['conditions']['requiredActionPoints']))
    embed.add_field(name=f"Requires {GLADIUS_ICONS['movement']} movement?", value=str(
        attrs['conditions']['requiredMovement']))
    embed.add_field(name=f"Usable in {GLADIUS_ICONS['transport']} transport?", value=str(
        attrs['conditions']['usableInTransport']))
    embed.add_field(name=f"Consumes {GLADIUS_ICONS['actions']} AP?", value=str(
        attrs['conditions']['consumedActionPoints']))
    embed.add_field(name=f"Consumes {GLADIUS_ICONS['movement']} movement?", value=str(
        attrs['conditions']['consumedMovement']))

    # Modifiers
    if (modifiers := attrs['modifiers']):
        embed.add_field(name='Modifiers', value='\n'.join(modifiers)[:1024], inline=False)

    if verbose:
        # Raw XML
        if (rawXML := attrs['rawXML']):
            embed.add_field(name='Raw XML', value=rawXML[:1024], inline=False)

        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_zaction_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = ZEPHON_BRANCH_COLORS[attrs['branch']]

    # Branch
    embed.add_field(name='Branch', value=attrs['branch'], inline=False)

    # Cooldown
    if attrs['cooldown'] == 'Passive':
        embed.add_field(name='Cooldown', value='Passive', inline=False)
    else:
        embed.add_field(
            name='Cooldown', value=f"{ZEPHON_ICONS['turns']} {attrs['cooldown']}", inline=False)

    # Conditions
    embed.add_field(name=f"Required upgrade", value=str(
        attrs['conditions']['requiredUpgrade']))
    embed.add_field(name=f"Requires {ZEPHON_ICONS['actions']} AP?", value=str(
        attrs['conditions']['requiredActionPoints']))
    embed.add_field(name=f"Requires {ZEPHON_ICONS['movement']} movement?", value=str(
        attrs['conditions']['requiredMovement']))
    embed.add_field(name=f"Usable in {ZEPHON_ICONS['transport']} transport?", value=str(
        attrs['conditions']['usableInTransport']))
    embed.add_field(name=f"Consumes {ZEPHON_ICONS['actions']} AP?", value=str(
        attrs['conditions']['consumedActionPoints']))
    embed.add_field(name=f"Consumes {ZEPHON_ICONS['movement']} movement?", value=str(
        attrs['conditions']['consumedMovement']))

    # Modifiers
    if (modifiers := attrs['modifiers']):
        embed.add_field(name='Modifiers', value='\n'.join(modifiers)[:1024], inline=False)

    if verbose:
        # Raw XML
        if (rawXML := attrs['rawXML']):
            embed.add_field(name='Raw XML', value=rawXML[:1024], inline=False)

        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_gbuilding_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = GLADIUS_FACTION_COLORS[attrs['faction']]

    # Faction
    embed.add_field(name='Faction', value=attrs['faction'], inline=False)

    # Cost
    costText = []
    for costName, costValue in attrs['resourceCosts'].items():
        if costName[-4:] == 'Cost':
            costText.extend((' | ', GLADIUS_ICONS[costName[:-4]], ' ', costValue))
    if costText == []:
        costText = ['None']
    else:
        # delete initial ' | '
        del costText[0]
    embed.add_field(name="Cost", value=''.join(costText))

    # Upkeep
    upkeepText = []
    for upkeepName, upkeepValue in attrs['resourceCosts'].items():
        if upkeepName[-6:] == 'Upkeep':
            upkeepText.extend((' | ', GLADIUS_ICONS[upkeepName[:-6]], ' ', upkeepValue))
    if upkeepText == []:
        upkeepText = ['None']
    else:
        # delete initial ' | '
        del upkeepText[0]
    embed.add_field(name='Upkeep', value=''.join(upkeepText))

    # Output
    outputText = []
    for outputName, outputValue in attrs['resourceOutput'].items():
        outputText.extend((' | ', GLADIUS_ICONS[outputName], ' ', outputValue))
    if outputText == []:
        outputText = ['None']
    else:
        # delete initial ' | '
        del outputText[0]
    embed.add_field(name="Output", value=''.join(outputText))

    # Traits
    traitsText = []
    for trait in attrs['traits']:
        # if upgrade required
        if attrs['traits'][trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText))

    # Actions
    actionsText = []
    for action in attrs['actions']:
        # if upgrade required
        if attrs['actions'][action]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        actionsText.extend((action, upgrade, '\n'))
    if actionsText == []:
        actionsText = ['None']
    embed.add_field(name='Actions', value=''.join(actionsText))

    # Flavor
    if verbose:
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_zbuilding_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = ZEPHON_BRANCH_COLORS[attrs['branch']]

    # Branch
    embed.add_field(name='Branch', value=attrs['branch'], inline=False)

    # Cost
    costText = []
    for costName, costValue in attrs['resourceCosts'].items():
        if costName[-4:] == 'Cost':
            costText.extend((' | ', ZEPHON_ICONS[costName[:-4]], ' ', costValue))
    if costText == []:
        costText = ['None']
    else:
        # delete initial ' | '
        del costText[0]
    embed.add_field(name="Cost", value=''.join(costText))

    # Upkeep
    upkeepText = []
    for upkeepName, upkeepValue in attrs['resourceCosts'].items():
        if upkeepName[-6:] == 'Upkeep':
            upkeepText.extend((' | ', ZEPHON_ICONS[upkeepName[:-6]], ' ', upkeepValue))
    if upkeepText == []:
        upkeepText = ['None']
    else:
        # delete initial ' | '
        del upkeepText[0]
    embed.add_field(name='Upkeep', value=''.join(upkeepText))

    # Output
    outputText = []
    for outputName, outputValue in attrs['resourceOutput'].items():
        outputText.extend((' | ', ZEPHON_ICONS[outputName], ' ', outputValue))
    if outputText == []:
        outputText = ['None']
    else:
        # delete initial ' | '
        del outputText[0]
    embed.add_field(name="Output", value=''.join(outputText))

    # Traits
    traitsText = []
    for trait in attrs['traits']:
        # if upgrade required
        if attrs['traits'][trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText))

    # Actions
    actionsText = []
    for action in attrs['actions']:
        # if upgrade required
        if attrs['actions'][action]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        actionsText.extend((action, upgrade, '\n'))
    if actionsText == []:
        actionsText = ['None']
    embed.add_field(name='Actions', value=''.join(actionsText))

    # Flavor
    if verbose:
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_gitem_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    embed = discord.Embed(title=name, description=attrs['description'])

    # Color
    embed.colour = RARITY_COLORS[attrs['rarity']]

    # Rarity
    embed.add_field(name='Rarity', value=attrs['rarity'])

    # Influence cost
    embed.add_field(
        name='Cost', value=f"{GLADIUS_ICONS['influence']} {attrs['influenceCost']}")

    # Ability
    if (modifiers := attrs['modifiers']):
        embed.add_field(name='Ability', value='\n'.join(modifiers)[:1024], inline=False)

    if verbose:
        # Raw XML
        if (rawXML := attrs['rawXML']):
            embed.add_field(name='Raw XML', value=rawXML[:1024], inline=False)

        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_zitem_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = RARITY_COLORS[attrs['rarity']]

    # Rarity
    embed.add_field(name='Rarity', value=attrs['rarity'])

    # Branch
    embed.add_field(name='Branch', value=attrs['branch'])

    # Influence cost
    embed.add_field(
        name='Cost', value=f"{ZEPHON_ICONS['influence']} {attrs['influenceCost']}")

    # Buy condition
    if (buyCondition := attrs['buyCondition']):
        embed.add_field(name='Prerequisite', value=buyCondition)

    # Ability
    if (modifiers := attrs['modifiers']):
        embed.add_field(name='Ability', value='\n'.join(modifiers)[:1024], inline=False)

    if verbose:
        # Raw XML
        if (rawXML := attrs['rawXML']):
            embed.add_field(name='Raw XML', value=rawXML[:1024], inline=False)

        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_gtrait_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    try:
        embed.colour = GLADIUS_FACTION_COLORS[attrs['faction']]
    except KeyError:
        embed.colour = GLADIUS_FACTION_COLORS['Neutral']

    # Faction
    embed.add_field(name='Faction', value=attrs['faction'])

    # Modifiers
    if (modifiers := attrs['modifiers']):
        embed.add_field(name='Modifiers', value='\n'.join(modifiers)[:1024], inline=False)

    if verbose:
        # Raw XML
        if (rawXML := attrs['rawXML']):
            embed.add_field(name='Raw XML', value=rawXML[:1024], inline=False)

        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_ztrait_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = ZEPHON_BRANCH_COLORS[attrs['branch']]

    # Branch
    embed.add_field(name='Branch', value=attrs['branch'], inline=False)

    # Modifiers
    if (modifiers := attrs['modifiers']):
        embed.add_field(name='Modifiers', value='\n'.join(modifiers)[:1024], inline=False)

    if verbose:
        # Raw XML
        if (rawXML := attrs['rawXML']):
            embed.add_field(name='Raw XML', value=rawXML[:1024], inline=False)

        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_gunit_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = GLADIUS_FACTION_COLORS[attrs['faction']]

    # Faction
    embed.add_field(name='Faction', value=attrs['faction'])

    # DLC
    embed.add_field(name='DLC', value=DLCS[attrs['dlc']])

    # Placeholder for spacing
    embed.add_field(name='\u200b', value='\u200b')

    # Cost
    costText = [GLADIUS_ICONS['production'],
                ' ', attrs['resourceStats']['productionCost']]
    for resource in GLADIUS_RESOURCES:
        cost = attrs['resourceStats'][resource + 'Cost']
        if cost != '0':
            costText.extend((' | ', GLADIUS_ICONS[resource], ' ', cost))
    embed.add_field(name="Cost", value=''.join(costText))

    # Upkeep
    upkeepText = []
    for resource in GLADIUS_RESOURCES:
        upkeep = attrs['resourceStats'][resource + 'Upkeep']
        if upkeep != '0':
            upkeepText.extend(
                (' | ', GLADIUS_ICONS[resource], ' ', upkeep))
    if upkeepText == []:
        upkeepText = ['None']
    else:
        # delete initial ' | '
        del upkeepText[0]
    embed.add_field(name='Upkeep', value=''.join(upkeepText))

    # Stats
    statText = (f"**{attrs['combatStats']['groupSizeMax']} model(s)**\n"
                f"{GLADIUS_ICONS['armor']} {attrs['combatStats']['armor']} | {GLADIUS_ICONS['hitpoints']} {round(attrs['combatStats']['hitpointsMax'])} | "
                f"{GLADIUS_ICONS['morale']} {attrs['combatStats']['moraleMax']}\n {GLADIUS_ICONS['movement']} {attrs['combatStats']['movementMax']} | "
                f"{GLADIUS_ICONS['cargoSlots']} {attrs['combatStats']['cargoSlots']} | {GLADIUS_ICONS['itemSlots']} {attrs['combatStats']['itemSlots']}")
    embed.add_field(name='Stats', value=statText)

    # Weapons
    weaponsText = []
    for weapon in attrs['weapons']:
        # if upgrade required
        if attrs['weapons'][weapon]['requiredUpgrade']:
            upgrade = ' (U)'
        else:
            upgrade = ''
        # if weapon is secondary
        if attrs['weapons'][weapon]['secondary']:
            secondary = ' (S)'
        else:
            secondary = ''
        weaponsText.extend(
            f"{attrs['weapons'][weapon]['count']}x {weapon}{upgrade}{secondary}\n")
    if weaponsText == []:
        weaponsText = ['None']
    embed.add_field(name='Weapons', value=''.join(weaponsText))

    # Traits
    traitsText = []
    for trait in attrs['traits']:
        # if upgrade required
        if attrs['traits'][trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText))

    # Actions
    actionsText = []
    for action in attrs['actions']:
        # if upgrade required
        if attrs['actions'][action]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        actionsText.extend((action, upgrade, '\n'))
    if actionsText == []:
        actionsText = ['None']
    embed.add_field(name='Actions', value=''.join(actionsText))

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)
        embed.set_footer(text=('Traits/weapons marked with (U) require a researchable upgrade.\n'
                               'Weapons marked with (S) are secondary weapons.\n'
                               'Stat-changing traits like Fleet not taken into account.'))

    return embed


def create_zunit_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = ZEPHON_BRANCH_COLORS[attrs['branch']]

    # Branch
    embed.add_field(name='Branch', value=attrs['branch'], inline=False)

    # Cost
    costText = [ZEPHON_ICONS['production'],
                ' ', attrs['resourceStats']['productionCost']]
    for resource in ZEPHON_RESOURCES:
        cost = attrs['resourceStats'][resource + 'Cost']
        if cost != '0':
            costText.extend((' | ', ZEPHON_ICONS[resource], ' ', cost))
    embed.add_field(name='Cost', value=''.join(costText))

    # Upkeep
    upkeepText = []
    for resource in ZEPHON_RESOURCES:
        upkeep = attrs['resourceStats'][resource + 'Upkeep']
        if upkeep != '0':
            upkeepText.extend(
                (' | ', ZEPHON_ICONS[resource], ' ', upkeep))
    if upkeepText == []:
        upkeepText = ['None']
    else:
        # delete initial ' | '
        del upkeepText[0]
    embed.add_field(name='Upkeep', value=''.join(upkeepText))

    # Stats
    statText = (f"{ZEPHON_ICONS['groupSize']} {attrs['combatStats']['groupSizeMax']} | {ZEPHON_ICONS['accuracy']} {attrs['combatStats']['accuracy']}\n"
                f"{ZEPHON_ICONS['armor']} {attrs['combatStats']['armor']} | {ZEPHON_ICONS['hitpoints']} {attrs['combatStats']['hitpointsMax']} | "
                f"{ZEPHON_ICONS['morale']} {attrs['combatStats']['moraleMax']}\n {ZEPHON_ICONS['movement']} {attrs['combatStats']['movementMax']} | "
                f"{ZEPHON_ICONS['cargoSlots']} {attrs['combatStats']['cargoSlots']} | {ZEPHON_ICONS['itemSlots']} {attrs['combatStats']['itemSlots']}")
    embed.add_field(name='Stats', value=statText)

    # Weapons
    weaponsText = []
    for weapon in attrs['weapons']:
        # if upgrade required
        if attrs['weapons'][weapon]['requiredUpgrade']:
            upgrade = ' (U)'
        else:
            upgrade = ''
        # if weapon is secondary
        if attrs['weapons'][weapon]['secondary']:
            secondary = ' (S)'
        else:
            secondary = ''
        weaponsText.extend(
            f"{attrs['weapons'][weapon]['count']}x {weapon}{upgrade}{secondary}\n")
    if weaponsText == []:
        weaponsText = ['None']
    embed.add_field(name='Weapons', value=''.join(weaponsText))

    # Traits
    traitsText = []
    for trait in attrs['traits']:
        # if upgrade required
        if attrs['traits'][trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText))

    # Actions
    actionsText = []
    for action in attrs['actions']:
        # if upgrade required
        if attrs['actions'][action]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        actionsText.extend((action, upgrade, '\n'))
    if actionsText == []:
        actionsText = ['None']
    embed.add_field(name='Actions', value=''.join(actionsText))

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)
        embed.set_footer(text=('Traits/weapons marked with (U) require a researchable upgrade.\n'
                               'Weapons marked with (S) are secondary weapons.\n'
                               'Stat-changing traits like Fleet not taken into account.'))

    return embed


def create_gupgrade_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    try:
        embed.colour = GLADIUS_FACTION_COLORS[attrs['faction']]
    except KeyError:
        embed.colour = GLADIUS_FACTION_COLORS['Neutral']

    # Faction
    embed.add_field(name='Faction', value=attrs['faction'])

    # DLC
    embed.add_field(name='DLC', value=DLCS[attrs['dlc']])

    # Tier
    embed.add_field(name='Tier', value=attrs['tier'])

    # Required upgrades
    embed.add_field(name='Required Upgrades', value='\n'.join(
        attrs['requiredUpgrades']), inline=False)

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_zupgrade_embed(name: str, attrs: dict, verbose: bool) -> discord.Embed:
    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = ZEPHON_BRANCH_COLORS[attrs['branch']]

    # Branch
    embed.add_field(name='Branch', value=attrs['branch'])

    # Faction
    embed.add_field(name='Faction', value=attrs['faction'])

    # Tier
    embed.add_field(name='Tier', value=attrs['tier'])

    # Required upgrades
    embed.add_field(name='Required Upgrades', value='\n'.join(
        attrs['requiredUpgrades']), inline=False)

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)

    return embed


def create_gweapon_embed(name: str, attrs: dict, verbose: bool, unitName: str = None, unitDict: dict = None) -> discord.Embed:
    if unitDict:
        weaponStats = calculate_gweapon_stats(
            attrs['range'], attrs['innateStats'], unitDict['weaponStats'])
    else:
        weaponStats = calculate_gweapon_stats(
            attrs['range'], attrs['innateStats'])

    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = GLADIUS_FACTION_COLORS[attrs['faction']]

    # Faction
    embed.add_field(name='Faction', value=attrs['faction'])

    # Wielder
    if unitName:
        embed.add_field(name='Wielder', value=unitName)

    # Stats
    statText = (f"{GLADIUS_ICONS['damage']} {weaponStats['damage']} | {GLADIUS_ICONS['attacks']} {weaponStats['attacks']} | "
                f"{GLADIUS_ICONS['armorPenetration']} {weaponStats['armorPen']} | {GLADIUS_ICONS['accuracy']} {weaponStats['accuracy']} | "
                f"{GLADIUS_ICONS['range']} {attrs['range']}")
    embed.add_field(name='Stats', value=statText, inline=False)

    # Traits
    traitsText = []
    for trait in attrs['traits']:
        # if upgrade required
        if attrs['traits'][trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText), inline=False)

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)
        embed.set_footer(text=('Traits marked with (U) require a researchable upgrade.\n'
                               'Weapon stats depend on the unit wielding the weapon. Stat-changing traits like Twin-Linked not taken into account. '
                               'Values shown may not be accurate.'))

    return embed


def create_zweapon_embed(name: str, attrs: dict, verbose: bool, unitName: str = None, unitDict: dict = None) -> discord.Embed:
    if unitName:
        weaponStats = calculate_zweapon_stats(
            attrs['innateStats'], unitDict['combatStats']['accuracy'])
    else:
        weaponStats = calculate_zweapon_stats(attrs['innateStats'])

    # Name and Description
    if (description := attrs['description']):
        embed = discord.Embed(title=name, description=description)
    else:
        embed = discord.Embed(title=name)

    # Color
    embed.colour = ZEPHON_BRANCH_COLORS[attrs['branch']]

    # Branch
    embed.add_field(name='Branch', value=attrs['branch'], inline=False)

    # Wielder
    if unitName:
        embed.add_field(name='Wielder', value=unitName)

    # Stats
    statText = (f"{ZEPHON_ICONS['damage']} {weaponStats['damage']} | {ZEPHON_ICONS['attacks']} {weaponStats['attacks']} | "
                f"{ZEPHON_ICONS['armorPenetration']} {weaponStats['armorPen']} | {ZEPHON_ICONS['accuracy']} {weaponStats['accuracy']} | "
                f"{ZEPHON_ICONS['range']} {attrs['range']}")
    embed.add_field(name='Stats', value=statText, inline=False)

    # Traits
    traitsText = []
    for trait in attrs['traits']:
        # if upgrade required
        if attrs['traits'][trait]:
            upgrade = ' (U)'
        else:
            upgrade = ''
        traitsText.extend((trait, upgrade, '\n'))
    if traitsText == []:
        traitsText = ['None']
    embed.add_field(name='Traits', value=''.join(traitsText), inline=False)

    if verbose:
        # Flavor
        if (flavor := attrs['flavor']):
            embed.add_field(
                name='Flavor', value=f'*{flavor[:1024]}*', inline=False)
        embed.set_footer(text=('Traits marked with (U) require a researchable upgrade.\n'
                               'Weapon stats depend on the unit wielding the weapon. Stat-changing traits like Twin-Linked not taken into account. '
                               'Values shown may not be accurate.'))

    return embed
