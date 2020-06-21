from items.tool import *
from items.food import *
from items.armour import *
from items.block import *
from items.mineral import *
from items.ore import *
import random


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
    ITEMS_DICT["potato"] = ItemInfo("potato", "Przepyszny ziemniak.", Food, -10, {"health_points": 200})
    ITEMS_DICT["bacon"] = ItemInfo("bacon", "Przepyszny bekon.", Food, -10, {"health_points": 300})

    ITEMS_DICT["pickaxe_diamond"] = ItemInfo(
        "pickaxe_diamond",
        "Potężny przedmiot, uważaj na niego.",
        Tool,
        -10,
        {"damage": 5, "durability": 50, "range": 120, "env_damage": 15},
    )
    ITEMS_DICT["green_sword"] = ItemInfo(
        "green_sword",
        "Podstawowy miecz srebrny na potwory. Przydalby sie jeszcze stalowy - tez na potwory.",
        Tool,
        -40,
        {"damage": 30, "durability": 30, "range": 150, "env_damage": 2},
    )

    ITEMS_DICT["mage_helmet"] = ItemInfo("mage_helmet", "Helm maga", Helmet, -10, {"defence": 3, "mana_power": 50})
    ITEMS_DICT["mage_breastplate"] = ItemInfo(
        "mage_breastplate", "Napiersciennik maga", Breastplate, -10, {"defence": 7}
    )
    ITEMS_DICT["mage_boots"] = ItemInfo(
        "mage_boots", "Buty maga", Boots, -10, {"defence": 2, "speed_value": 2, "double_jump": True}
    )

    ITEMS_DICT["fire_helmet"] = ItemInfo("fire_helmet", "Helm ognisty", Helmet, -10, {"defence": 6, "mana_power": 10})
    ITEMS_DICT["fire_breastplate"] = ItemInfo(
        "fire_breastplate", "Napiersciennik ognisty", Breastplate, -10, {"defence": 15}
    )
    ITEMS_DICT["fire_boots"] = ItemInfo(
        "fire_boots", "Buty ogniste", Boots, -10, {"defence": 7, "speed_value": 0, "double_jump": False}
    )

    ITEMS_DICT["black_helmet"] = ItemInfo(
        "black_helmet", "Helm czarny", Helmet, -10, {"defence": 13, "mana_power": -30}
    )
    ITEMS_DICT["black_breastplate"] = ItemInfo(
        "black_breastplate", "Napiersciennik czarny", Breastplate, -10, {"defence": 22}
    )
    ITEMS_DICT["black_boots"] = ItemInfo(
        "black_boots", "Buty czarne", Boots, -10, {"defence": 9, "speed_value": 3, "double_jump": True}
    )

    ITEMS_DICT["black_cat_helmet"] = ItemInfo(
        "black_cat_helmet", "Helm czarnego kota", Helmet, -10, {"defence": 3, "mana_power": 10}
    )
    ITEMS_DICT["black_cat_breastplate"] = ItemInfo(
        "black_cat_breastplate", "Napiersciennik czarnego kota", Breastplate, -10, {"defence": 6}
    )
    ITEMS_DICT["black_cat_boots"] = ItemInfo(
        "black_cat_boots", "Buty czarnego kota", Boots, -10, {"defence": 2, "speed_value": 5.5, "double_jump": True}
    )

    ITEMS_DICT["dirt"] = ItemInfo("dirt", "Wszedzie jej pelno.", Block, -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["bone_dirt"] = ItemInfo("bone_dirt", "Wszedzie jej pelno.", Block, -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["flint_dirt"] = ItemInfo("flint_dirt", "Wszedzie jej pelno.", Block, -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["stone"] = ItemInfo("stone", "Wszedzie jej pelno.", Block, -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["grass"] = ItemInfo("grass", "Wszedzie jej pelno.", Block, -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["mushroom_brown"] = ItemInfo(
        "mushroom_brown", "Wszedzie jej pelno.", Block, -10, {"hp": 20, "probability": 0.5}
    )
    ITEMS_DICT["mushroom_red"] = ItemInfo(
        "mushroom_red", "Wszedzie jej pelno.", Block, -10, {"hp": 20, "probability": 0.5}
    )
    ITEMS_DICT["tall_grass"] = ItemInfo("tall_grass", "Wszedzie jej pelno.", Block, -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["iron"] = ItemInfo("iron", "Wszedzie jej pelno.", Ore, -10, {"hp": 30, "probability": 0.5})
    ITEMS_DICT["coal_ore"] = ItemInfo("coal_ore", "Wszedzie jej pelno.", Block, -10, {"hp": 30, "probability": 0.5})
    ITEMS_DICT["copper"] = ItemInfo("copper", "Wszedzie jej pelno.", Block, -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["log"] = ItemInfo("log", "Wszedzie jej pelno.", Block, -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["log_hole"] = ItemInfo("log_hole", "Wszedzie jej pelno.", Block, -10, {"hp": 20, "probability": 0.5})
    ITEMS_DICT["leaves"] = ItemInfo("leaves", "Wszedzie jej pelno.", Block, -10, {"hp": 5, "probability": 0.5})
    ITEMS_DICT["apple_leaves"] = ItemInfo(
        "apple_leaves", "Wszedzie jej pelno.", Block, -10, {"hp": 5, "probability": 0.5}
    )
    ITEMS_DICT["diamond1"] = ItemInfo(
        "diamond1", "Najcenniejszy na świecie.", Block, -10, {"hp": 50, "probability": 0.5}
    )
    ITEMS_DICT["diamond2"] = ItemInfo("diamond2", "Błyszczy się jak....", Block, -10, {"hp": 50, "probability": 0.5})
    ITEMS_DICT["diamond3"] = ItemInfo(
        "diamond3", "Najtańczy z najdroższych.", Block, -10, {"hp": 50, "probability": 0.5}
    )
    ITEMS_DICT["glass"] = ItemInfo("glass", "Wszedzie jej pelno.", Block, -10, {"hp": 99999, "probability": 0.5})
    ITEMS_DICT["cloud"] = ItemInfo("cloud", "Wszedzie jej pelno.", Block, -10, {"hp": 1, "probability": 0.0})
    ITEMS_DICT["grass_dirt"] = ItemInfo("grass_dirt", "Wszedzie jej pelno.", Block, -10, {"hp": 1, "probability": 0.0})
    ITEMS_DICT["clay"] = ItemInfo("clay", "Wszedzie jej pelno.", Block, -10, {"hp": 1, "probability": 0.0})
    ITEMS_DICT["chrysoprase_clay"] = ItemInfo(
        "chrysoprase_clay", "Wszedzie jej pelno.", Block, -10, {"hp": 1, "probability": 0.0}
    )

    ITEMS_DICT["iron_mineral"] = ItemInfo("iron_mineral", "Kryształ żelaza", Mineral, -10, {})

    def __init__(self, game):
        self.game = game

    def create(self, name, x, y):
        """Create item and return it"""
        info = self.ITEMS_DICT[name]
        return info.variety(x, y, info, self.game)

    def add_random_item(self, x, y):
        """Add random item on (x, y) position (for example when creature dies)"""
        item_name = random.choice(list(self.ITEMS_DICT.keys()))
        item = self.create(item_name, x, y)
        if item.variety == Block:
            Item.scale_item(item)
        self.game.items.add(item)

    def add_item(self, item_name, x, y):
        """Add item (using its name) on (x, y) position (for example when creature dies)"""
        item = self.create(item_name, x, y)
        if item.variety == Block:
            Item.scale_item(item)
        self.game.items.add(item)
