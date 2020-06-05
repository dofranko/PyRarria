from items.tool import *
from items.food import *


class ItemInfo:
    """A class representing item's informations - used by Factory"""

    def __init__(self, name, desc, variety, angle, attr):
        self.name = name
        self.description = desc
        self.variety = variety
        self.angle = angle
        self.attr = attr


class Factory:
    """A factory for creating items"""

    ITEMS_DICT = {}
    ITEMS_DICT["potato"] = ItemInfo("potato", "Przepyszny ziemniak.", "food", -10, {"health_points": 200})
    ITEMS_DICT["pickaxe_diamond"] = ItemInfo(
        "pickaxe_diamond",
        "Potężny przedmiot, uważaj na niego.",
        "tool",
        -30,
        {"damage": 30, "durability": 30, "range": 120},
    )

    def __init__(self, game):
        self.game = game

    def create(self, name, x, y):
        info = self.ITEMS_DICT[name]
        if info.variety == "food":
            return self.create_food(name, info, x, y)
        if info.variety == "tool":
            return self.create_tool(name, info, x, y)
        return self.create_item(name, info, x, y)

    def create_food(self, name, info, x, y):
        food = Food(x, y, info, self.game)
        return food

    def create_tool(self, name, info, x, y):
        tool = Tool(x, y, info, self.game)
        return tool
