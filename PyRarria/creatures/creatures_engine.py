from creatures.sprites_tree.bat import Bat
from creatures.sprites_tree.bird import Bird
from creatures.sprites_tree.chicken import Chicken
from creatures.sprites_tree.cow import Cow
from creatures.sprites_tree.sheep import Sheep
from creatures.sprites_tree.skeleton import Skeleton
from creatures.sprites_tree.walking_test import WalkingTest
from creatures.sprites_tree.zombie import Zombie
from pygame.sprite import Group
from settings import FPS

from creatures.vector import PVector

LIMITS = {
    "walking_test": 0,
    "birds": 5,
    "skeletons": 3,
    "zombies": 3,
    "cows": 3,
    "sheeps": 3,
    "bats": 3,
    "chickens": 3,
}


FREQUENCIES = {
    "walking_test": 1,
    "birds": 1,
    "skeletons": 1,
    "zombies": 1,
    "cows": 1,
    "sheeps": 1,
    "bats": 1,
    "chickens": 1,
}

CREATURES = {
    "walking_test": WalkingTest,
    "bird": Bird,
    "skeleton": Skeleton,
    "zombies": Zombie,
    "cows": Cow,
    "sheep": Sheep,
    "bats": Bat,
    "chickens": Chicken,
}

NAMES = {
    "walking_test": "walking_test",
    "bird": "birds",
    "skeleton": "skeletons",
    "zombies": "zombie",
    "cows": "cow",
    "sheeps": "sheep",
    "bats": "bat",
    "chickens": "chicken",
}


SPAWN_DISTANCE = 100


class CreaturesEngine:
    def __init__(self, game):

        # window, clock, main position
        self.game = game
        self.window = game.screen
        self.clock = 0
        self.map_position = PVector(0, 0)
        self.map_position_init = PVector(0, 0)

        # map, player, arrows
        self.platforms = game.platforms
        self.player = game.player

        # creatures, arrows
        self.all_creatures = game.all_creatures
        self.arrows = game.arrows

        # groups
        self.groups = {
            "walking_test": Group(),
            "birds": Group(),
            "skeletons": Group(),
            "zombies": Group(),
            "cows": Group(),
            "sheeps": Group(),
            "bats": Group(),
            "chickens": Group(),
        }

    def update(self):
        # update main position
        self.update_map_position()

        # clock
        self.clock += 1

        # hit
        # for creature in self.all_creatures:
        #     creature.hit(self.player)

        # bite (if doesn't bite nothing happens)
        for creature in self.all_creatures:
            creature.bite(self.player)

        # shot (if doesn't shoot nothing happens)
        for archer in self.all_creatures:
            archer.shoot(self.player, self.arrows)

        # update creatures
        for creature in self.all_creatures:
            creature.update(self.player, self.platforms, self.map_position)

        # update arrows
        for arr in self.arrows:
            arr.update(self.player, self.platforms, self.map_position)

        # spawn
        self.spawn()

        # print stats
        # self.print_stats()

    def draw(self):
        # redraw creatures
        for creature in self.all_creatures:
            creature.draw(self.window)

        # redraw arrows
        for arrow in self.arrows:
            arrow.draw(self.window)

    def spawn(self):
        for group, frequency, limit, Creature in zip(
            self.groups.values(), FREQUENCIES.values(), LIMITS.values(), CREATURES.values()
        ):

            if len(group) >= limit:
                continue

            if self.clock % (frequency * FPS) != 0:
                continue

            new_creature = Creature(400, 0)
            group.add(new_creature)
            self.all_creatures.add(new_creature)

    def update_map_position(self):
        dx, dy = self.game.get_main_stage_position()
        self.map_position.set(dx - self.map_position_init.x, dy - self.map_position_init.y)

    def print_stats(self):
        for group, name in zip(self.groups.values(), NAMES):
            print(f"{name:10}:{len(group)}")
        print()
