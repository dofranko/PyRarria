from creatures.sprites_tree.abstract_sprite import AbstractSprite
from creatures.hp_bar import HpBar
from creatures.physical_engine import *
from creatures.vector import PVector

ANIMATION = None
OBJECT = None


class Sprite(AbstractSprite):
    def __init__(self, x, y):
        super(Sprite, self).__init__(x, y)
        # self.create(x, y, **OBJECT)

    def create(self, x, y, manoeuvrability, maxspeed, maxforce, maxhp, mass, items, damage, defense):

        # variables
        self.radius = min(self.width, self.height)
        self.angle = 0.0
        self.mass = mass

        # limits
        self.maxspeed = maxspeed
        self.maxforce = maxforce
        self.maxhp = maxhp
        self.manoeuvrability = manoeuvrability

        # flags
        self.is_enemy = True
        self.is_hpbar = False
        self.is_hitbox = True
        self.is_fixpos = True

        # counters
        self.anim_count = 0
        self.bite_count = 0
        self.shot_count = 0

        # vectors
        self.position = PVector(x, y)
        self.velocity = PVector(0, 0.001)
        self.acceleration = PVector(0, 0)

        # body
        w, h = self.width, self.height
        self.rect = pg.rect.Rect(0, 0, w, h)
        self.rect.center = self.position.repr()
        self.body = pg.rect.Rect(self.rect)
        self.hpbar = HpBar(self.body.midtop)

        # sprite specific
        self.hp = maxhp
        self.items = items
        self.damage = damage
        self.defense = defense

    def draw(self, win):
        pass

    def hit(self, damage_value):
        self.hp -= damage_value

    def bite(self, player):
        if self.is_enemy and self.rect.colliderect(player):
            if self.bite_count > 0:
                self.bite_count -= 1
            else:
                player.hit(self.damage)
                direction = -1
                if self.position.x < player.position.x:
                    direction = 1
                player.push_away(direction, 4, 14)
                self.bite_count = 20

    def update(self, player, platforms, map_position):
        # dead
        if self.hp <= 0:
            self.die()
            return

        # alive
        self.update_forces(player, platforms)
        self.move(map_position)

    def update_forces(self, player, platforms):
        pass

    def move(self, map_position):
        # move
        self.velocity += self.acceleration
        self.velocity.xlimit(self.maxspeed)
        self.position += self.velocity
        self.acceleration.zero()

        # update body
        self.body.topleft = (self.position + map_position).repr()
        self.rect.topleft = (self.position + map_position).repr()
        self.hpbar.center(self.body.midtop)

        # update animation counter
        self.anim_count -= 1
        self.anim_count %= self.animation_ticks

    def apply_force(self, force):
        force.limit(self.maxforce)
        self.acceleration += force

    def die(self):
        print("die")
        self.kill()
