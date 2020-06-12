from items.tool import *
from items.food import *
from items.armour import *
from items.tree import *
import random
from items.block import *


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

    ITEMS_DICT["dirt"] = ItemInfo("dirt", "Wszedzie jej pelno.", "block", -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["stone"] = ItemInfo("stone", "Wszedzie jej pelno.", "block", -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["grass"] = ItemInfo("grass", "Wszedzie jej pelno.", "block", -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["iron"] = ItemInfo("iron", "Wszedzie jej pelno.", "block", -10, {"hp": 30, "probability": 0.5})
    ITEMS_DICT["copper"] = ItemInfo("copper", "Wszedzie jej pelno.", "block", -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["wood"] = ItemInfo("wood", "Wszedzie jej pelno.", "block", -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["leaf"] = ItemInfo("leaf", "Wszedzie jej pelno.", "block", -10, {"hp": 5, "probability": 0.5})
    ITEMS_DICT["diamond1"] = ItemInfo(
        "diamond1", "Najcenniejszy na świecie.", "block", -10, {"hp": 50, "probability": 0.5}
    )
    ITEMS_DICT["diamond2"] = ItemInfo("diamond2", "Błyszczy się jak....", "block", -10, {"hp": 50, "probability": 0.5})
    ITEMS_DICT["diamond3"] = ItemInfo(
        "diamond3", "Najtańczy z najdroższych.", "block", -10, {"hp": 50, "probability": 0.5}
    )
    ITEMS_DICT["glass"] = ItemInfo("glass", "Wszedzie jej pelno.", "block", -10, {"hp": 99999, "probability": 0.5})
    ITEMS_DICT["cloud"] = ItemInfo("cloud", "Wszedzie jej pelno.", "block", -10, {"hp": 1, "probability": 0.0})
    ITEMS_DICT["clump"] = ItemInfo("clump", "Wszedzie jej pelno.", "block", -10, {"hp": 1, "probability": 0.0})

    def __init__(self, game):
        self.game = game

    def create(self, name, x, y):
        """Create item and return it"""
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
        elif info.variety == "block":
            return self.create_placed_block(name, info, x, y)

    def create_food(self, info, x, y):
        """Return new food"""
        return Food(x, y, info, self.game)

    def create_tool(self, info, x, y):
        """Return new tool"""
        return Tool(x, y, info, self.game)

    def create_helmet(self, info, x, y):
        """Return new helmet"""
        return Helmet(x, y, info, self.game)

    def create_breastplate(self, info, x, y):
        """Return new breastplat"""
        return Breastplate(x, y, info, self.game)

    def create_boots(self, info, x, y):
        """Return new boots"""
        return Boots(x, y, info, self.game)

    def create_placed_block(self, name, info, x, y):
        """Return new block"""
        return Block(x, y, info, self.game)

    def create_placed_tree(self, name, info, x, y):
        """Return new tree"""
        return Tree(x, y, info, self.game)

    def add_random_item(self, x, y):
        """Add random item on (x, y) position (for example when creature dies)"""
        item_name = random.choice(list(self.ITEMS_DICT.keys()))
        item = self.create(item_name, x, y)
        self.game.items.add(item)
        self.game.all_sprites.add(item)

    def add_item(self, item_name, x, y):
        """Add item (using its name) on (x, y) position (for example when creature dies)"""
        item = self.create(item_name, x, y)
        self.game.items.add(item)
        self.game.all_sprites.add(item)
