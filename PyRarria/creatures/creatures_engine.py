from PyRarria.creatures.sprites_tree.bird import Bird
from PyRarria.creatures.sprites_tree.skeleton import Skeleton
from PyRarria.creatures.test_global_settings import FPS
from pygame.sprite import Group

LIMITS = {
    'birds': 10,
    'skeletons': 5,
}

FREQUENCIES = {
    'birds': 1,
    'skeletons': 1,
}

CREATURES = {
    'bird': Bird,
    'skeleton': Skeleton,
}

NAMES = {
    'bird': 'birds',
    'skeleton': 'skeletons',
}

SPAWN_DISTANCE = 100


class CreaturesEngine:

    def __init__(self, window, platforms, player,
                 all_creatures, arrows):

        # window, clock
        self.window = window
        self.clock = 0

        # map, player, arrows
        self.platforms = platforms
        self.player = player

        # creatures, arrows
        self.all_creatures = all_creatures
        self.arrows = arrows

        # groups
        self.groups = {
            'birds': Group(),
            'skeletons': Group(),
        }

    def update(self):
        # clock
        self.clock += 1

        # hit
        for creature in self.all_creatures:
            creature.hit(self.player)

        # bite
        for creature in self.all_creatures:
            creature.bite(self.player)

        # shot
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

    def print_stats(self):
        for group, name in zip(self.groups.values(), NAMES):
            print(f'{name:10}:{len(group)}')
        print()
