from items.tool import *
from items.food import *
from items.armour import *


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
    ITEMS_DICT["bacon"] = ItemInfo("bacon", "Przepyszny bekon.", "food", -10, {"health_points": 300})

    ITEMS_DICT["pickaxe_diamond"] = ItemInfo(
        "pickaxe_diamond",
        "Potężny przedmiot, uważaj na niego.",
        "tool",
        -10,
        {"damage": 5, "durability": 50, "range": 120, "env_damage": 15},
    )
    ITEMS_DICT["green_sword"] = ItemInfo(
        "green_sword",
        "Podstawowy miecz srebrny na potwory. Przydalby sie jeszcze stalowy - tez na potwory.",
        "tool",
        -40,
        {"damage": 30, "durability": 30, "range": 150, "env_damage": 2},
    )

    ITEMS_DICT["mage_helmet"] = ItemInfo("mage_helmet", "Helm maga", "helmet", -10, {"defence": 3, "mana_power": 50})
    ITEMS_DICT["mage_breastplate"] = ItemInfo(
        "mage_breastplate", "Napiersciennik maga", "breastplate", -10, {"defence": 7}
    )
    ITEMS_DICT["mage_boots"] = ItemInfo(
        "mage_boots", "Buty maga", "boots", -10, {"defence": 2, "speed_value": 2, "double_jump": True}
    )

    ITEMS_DICT["fire_helmet"] = ItemInfo("fire_helmet", "Helm ognisty", "helmet", -10, {"defence": 6, "mana_power": 10})
    ITEMS_DICT["fire_breastplate"] = ItemInfo(
        "fire_breastplate", "Napiersciennik ognisty", "breastplate", -10, {"defence": 15}
    )
    ITEMS_DICT["fire_boots"] = ItemInfo(
        "fire_boots", "Buty ogniste", "boots", -10, {"defence": 7, "speed_value": 0, "double_jump": False}
    )

    ITEMS_DICT["black_helmet"] = ItemInfo(
        "black_helmet", "Helm czarny", "helmet", -10, {"defence": 13, "mana_power": -30}
    )
    ITEMS_DICT["black_breastplate"] = ItemInfo(
        "black_breastplate", "Napiersciennik czarny", "breastplate", -10, {"defence": 22}
    )
    ITEMS_DICT["black_boots"] = ItemInfo(
        "black_boots", "Buty czarne", "boots", -10, {"defence": 9, "speed_value": 3, "double_jump": True}
    )

    def __init__(self, game):
        self.game = game

    def create(self, name, x, y):
        info = self.ITEMS_DICT[name]
        if info.variety == "food":
            return self.create_food(info, x, y)
        elif info.variety == "tool":
            return self.create_tool(info, x, y)
        elif info.variety == "helmet":
            return self.create_helmet(info, x, y)
        elif info.variety == "breastplate":
            return self.create_breastplate(info, x, y)
        elif info.variety == "boots":
            return self.create_boots(info, x, y)

    def create_food(self, info, x, y):
        return Food(x, y, info, self.game)

    def create_tool(self, info, x, y):
        return Tool(x, y, info, self.game)

    def create_helmet(self, info, x, y):
        return Helmet(x, y, info, self.game)

    def create_breastplate(self, info, x, y):
        return Breastplate(x, y, info, self.game)

    def create_boots(self, info, x, y):
        return Boots(x, y, info, self.game)
