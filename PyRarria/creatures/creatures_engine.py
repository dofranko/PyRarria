from PyRarria.creatures.sprites_tree.bird import Bird
from PyRarria.creatures.sprites_tree.skeleton import Skeleton
from PyRarria.creatures.sprites_tree.zombie import Zombie
from PyRarria.creatures.test_global_settings import FPS
from pygame.sprite import Group

LIMITS = {
    'birds': 0,
    'skeletons': 0,
    'zombies': 1,
}

FREQUENCIES = {
    'birds': 1,
    'skeletons': 1,
    'zombies': 1,
}

CREATURES = {
    'bird': Bird,
    'skeleton': Skeleton,
    'zombies': Zombie,

}

NAMES = {
    'bird': 'birds',
    'skeleton': 'skeletons',
    'zombies': 'zombie',
}

SPAWN_DISTANCE = 100


class CreaturesEngine:

    def __init__(self, game):

        # window, clock, main coords
        self.window = game.screen
        self.clock = 0
        self.main_position = game.main_position

        # map, player, arrows
        self.platforms = game.platforms
        self.player = game.player

        # creatures, arrows
        self.all_creatures = game.all_creatures
        self.arrows = game.arrows

        # groups
        self.groups = {
            'birds': Group(),
            'skeletons': Group(),
            'zombies': Group(),
        }

    def update(self):
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
            creature.update(self.player, self.platforms)

        # update arrows
        for arr in self.arrows:
            arr.update(self.player, self.platforms)

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
                self.groups.values(),
                FREQUENCIES.values(),
                LIMITS.values(),
                CREATURES.values()):

            if len(group) >= limit:
                continue

            if self.clock % (frequency*FPS) != 0:
                continue

            new_creature = Creature(self.player.location.x, self.player.location.y)
            group.add(new_creature)
            self.all_creatures.add(new_creature)

            self.print_stats()

    def map_move(self, delta):
        for creature in self.all_creatures:
            creature.map_move(delta)

    def print_stats(self):
        for group, name in zip(self.groups.values(), NAMES):
            print(f'{name:10}:{len(group)}')
        print()
