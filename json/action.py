from __future__ import annotations
from lxml import etree as ET
from dataclasses import dataclass
from obj import Obj, ID2name
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from unit import Unit


class ActionNotInUnitError(Exception):
    def __init__(self, actionName: str, unitName: str):
        self.actionName = actionName
        self.unitName = unitName


@dataclass
class ActionConditions:
    __slots__ = ['requiredUpgrade', 'requiredActionPoints', 'requiredMovement',
                 'usableInTransport', 'consumedActionPoints', 'consumedMovement']
    requiredUpgrade: str
    requiredActionPoints: bool
    requiredMovement: bool
    usableInTransport: bool
    consumedActionPoints: bool
    consumedMovement: bool


class Action(Obj):
    OBJ_CLASS = 'Actions'

    def __init__(self, name: str):
        super().__init__(name)
        self.passive = False
        self.cooldown = '0'
        self.conditions: dataclass = ActionConditions(
            None, True, False, False, True, True)
        self.modifiers: str

    def get_tree(self, unit: Unit):
        try:
            for action in unit.tree.find('actions'):
                tag = action.tag
                tagName = tag[0].upper() + tag[1:]
                if tagName == self.internalID or action.get('name') == self.internalID:
                    if (model := action.find('model')):
                        action.remove(model)
                    self.tree = action
                    break
            else:
                raise ActionNotInUnitError(self.name, unit.name)
        # no actions
        except AttributeError:
            raise ActionNotInUnitError(self.name, unit.name)

    def get_cooldown(self):
        if self.tree.get('passive'):
            self.passive = True
        elif (cooldownMin := self.tree.get('cooldownMin')):
            cooldownMax = self.tree.get('cooldownMax')
            self.cooldown = cooldownMin + ' ... ' + cooldownMax
        elif (cooldown := self.tree.get('cooldown')):
            self.cooldown = cooldown

    def get_conditions(self):
        if self.passive:
            self.conditions = ActionConditions(None, False, False, False, False, False)
        else:
            for conditionName in self.conditions.__slots__:
                conditionValue = self.tree.get(conditionName)
                if conditionValue == '1':
                    setattr(self.conditions, conditionName, True)
                elif conditionValue == '0':
                    setattr(self.conditions, conditionName, False)
                elif conditionName == 'requiredUpgrade':
                    setattr(self.conditions, conditionName, ID2name(
                        conditionValue, self.GAME, 'Upgrades'))

    def get_modifiers(self):
        self.modifiers = ET.tostring(self.tree, encoding='unicode')


class GAction(Action):
    GAME = 'Gladius'

    def __init__(self, name: str):
        super().__init__(name)


class ZAction(Action):
    GAME = 'Zephon'

    def __init__(self, name: str):
        super().__init__(name)
