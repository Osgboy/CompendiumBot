from __future__ import annotations
from lxml import etree as ET
from dataclasses import dataclass
from obj import Obj
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from unit import Unit

class ActionNotInUnitError(Exception):
    def __init__(self, actionName: str, unitName: str):
        self.actionName = actionName
        self.unitName = unitName

@dataclass
class ActionConditions:
    __slots__ = ['requiredActionPoints', 'requiredMovement', 'consumedActionPoints', 'consumedMovement', 'usableInTransport']
    requiredActionPoints: bool
    requiredMovement: bool
    consumedActionPoints: bool
    consumedMovement: bool
    usableInTransport: bool

class Action(Obj):
    OBJ_CLASS = 'Actions'

    def __init__(self, name: str):
        super().__init__(name)
        self.passive = False
        self.cooldown = '0'
        self.conditions: dataclass = ActionConditions(True, False, True, True, False)
        self.modifiers: str

    def get_tree(self, unit: Unit):
        try:
            for action in unit.tree.find('actions'):
                tag = action.tag
                tagName = tag[0].upper() + tag[1:]
                if tagName == self.internalID or action.get('name') == self.internalID:
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
        else:
            self.cooldown = self.tree.get('cooldown')

    def get_conditions(self):
        if self.passive:
            self.conditions = ActionConditions(*[False]*5)
        else:
            for conditionName in self.conditions.__slots__:
                if self.tree.get(conditionName) == '1':
                    setattr(self.conditions, conditionName, True)
                elif self.tree.get(conditionName) == '0':
                    setattr(self.conditions, conditionName, False)

    def get_modifiers(self):
        self.modifiers = ET.tostring(self.tree, encoding='unicode')[:1024]

class GAction(Action):
    GAME = 'Gladius'

    def __init__(self, name: str):
        super().__init__(name)

class ZAction(Action):
    GAME = 'Zephon'

    def __init__(self, name: str):
        super().__init__(name)
