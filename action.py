from obj import Obj


class Action(Obj):
    def __init__(self, name: str, game: str):
        self.objClass = 'Actions'
        super().__init__(name, game)

    def get_action_tree(self, unit):
        pass
