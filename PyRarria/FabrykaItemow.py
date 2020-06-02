from tool import *
from food import *


class ItemInfo():
    def __init__(self, name, desc, zdj, typ, angle, attr):
        self.name = name
        self.description = desc
        self.zdj = zdj
        self.typ = typ
        self.angle = angle
        self.attr = attr


class Fabryka():
    ITEMS_DICT = {}
    ITEMS_DICT["ziemniak"] = ItemInfo("ziemniak", "Przepyszny ziemniak.", "example_tool_2.png", "food", -10,
                                      {"premia": 5})
    ITEMS_DICT["kilof"] = ItemInfo("kilof", "Potężny przedmiot, uważaj na niego.", "diaxowy.png", "tool", -30,
                                   {"dmg": 5, "odp": 10})

    def __init__(self, game):
        self.game = game

    def create(self, name, x, y):
        info = self.ITEMS_DICT[name]
        if info.typ == "food":
            return self.create_food(name, info, x, y)
        if info.typ == "tool":
            return self.create_tool(name, info, x, y)
        return self.create_item(name, info, x, y)

    def create_food(self, name, info, x, y):
        food = Food(x, y, info, self.game)
        food.premia = info.attr["premia"]
        return food

    def create_tool(self, name, info, x, y):
        tool = Tool(x, y, info, self.game)
        tool.damage = info.attr["dmg"]
        tool.odpornosc = info.attr["odp"]
        return tool