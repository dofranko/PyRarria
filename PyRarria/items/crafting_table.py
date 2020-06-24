import pygame
from copy import deepcopy
from settings import *
from items.placeable import *
from math import hypot
from equipment import Equipment

vector = pygame.math.Vector2


class CraftingTable(Placeable):

    RULE_SETS = {}
    # TODO change it when table rdy
    RULE_SETS["green_sword"] = {"grass": 5, "dirt": 2}
    RULE_SETS["black_cat_helmet"] = {"green_sword": 1}

    def __init__(self, x, y, info, game, placed=True):
        super().__init__(x, y, info, game, placed)
        self.is_open = False
        self.table_squares = pygame.sprite.Group()
        self.square_image = pygame.image.load(IMAGES_LIST["crafting_table_square"])
        self.square_image = pygame.transform.scale(self.square_image, (32, 32))
        self.put_items = [[] for i in range(3) for j in range(3)]
        self.base_x = WIDTH // 3
        self.base_y = HEIGHT // 2
        self.base_size = 0
        self.use_range = 200
        self.__create_GUI()
        self.possible_items = []
        self.available_items = []
        self.button_down = False
        self.items_to_draw = pygame.sprite.Group()

    def __create_GUI(self):
        square_image = pygame.image.load(IMAGES_LIST["crafting_table_square"])
        square_image = pygame.transform.scale(square_image, (60, 60))
        self.base_size = square_image.get_width()
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_square = pygame.sprite.Sprite()
                new_square.image = square_image
                new_square.rect = new_square.image.get_rect()
                new_square.rect.x, new_square.rect.y = (
                    self.base_x + i * self.base_size,
                    self.base_y + j * self.base_size,
                )
                self.table_squares.add(new_square)

    def open(self):
        self.is_open = True

        player_items = self.get_player_items_to_dict(self.game.player)
        self.create_possible_items(player_items)
        self.create_available_items(player_items)
        self.prepare_possible_items()
        self.prepare_available_items()
        self.game.player.equipment.open()

    def close(self):
        self.is_open = False
        self.possible_items = []
        self.available_items = []
        self.items_to_draw = pygame.sprite.Group()
        self.game.player.equipment.close()

    def use(self):
        if self.is_open:
            self.close()
        else:
            self.open()

    def update(self):
        super().update()
        if self.game.handled_event:
            self.handle_mouse(self.game.handled_event)
        if self.is_open and (
            math.hypot(
                self.rect.center[0] - self.game.player.rect.center[0],
                self.rect.center[1] - self.game.player.rect.center[1],
            )
            > self.use_range
        ):
            self.close()

    def draw(self):
        super().draw()
        if self.is_open:
            self.items_to_draw.draw(self.game.screen)
            # self.draw_table_squares(self.game.screen)
            # self.draw_available_items(self.game.screen)
            # self.draw_possible_items(self.game.screen)
            # self.draw_items(self.game.screen)

    def handle_mouse(self, event):
        if not self.button_down and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.button_down = True
        elif self.button_down and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.button_down = False
            for craftable in self.items_to_draw:
                if craftable.rect.collidepoint(event.pos) and craftable.name in self.available_items:
                    self.craft(self.game.player.equipment, craftable.name)
                    break

    def draw_table_squares(self, screen):
        for i in range(len(self.possible_items) + len(self.available_items)):
            screen.blit(self.square_image, (i * 32, HEIGHT // 2))

    def prepare_possible_items(self):
        for i, item in enumerate(self.possible_items):
            image = self.square_image.copy()
            item_image = pygame.image.load(IMAGES_LIST[item])
            item_image = pygame.transform.scale(item_image, (32, 32))
            item_image.fill(GRAY, special_flags=pygame.BLEND_ADD)
            image.blit(item_image, (0, 0))

            item_sprite = pygame.sprite.Sprite()
            item_sprite.image = image
            item_sprite.rect = image.get_rect()
            item_sprite.rect.x, item_sprite.rect.y = (
                i * image.get_rect().width,
                HEIGHT // 2 + self.square_image.get_width(),
            )
            item_sprite.name = item
            self.items_to_draw.add(item_sprite)

    def prepare_available_items(self):
        for i, item in enumerate(self.available_items):
            image = self.square_image.copy()
            item_image = pygame.image.load(IMAGES_LIST[item])
            item_image = pygame.transform.scale(item_image, (32, 32))
            image.blit(item_image, (0, 0))

            item_sprite = pygame.sprite.Sprite()
            item_sprite.image = image
            item_sprite.rect = image.get_rect()
            item_sprite.rect.x, item_sprite.rect.y = (i * image.get_rect().width, HEIGHT // 2)
            item_sprite.name = item
            self.items_to_draw.add(item_sprite)

    def draw_items(self, screen):
        for pos in range(0, len(self.put_items)):
            i = pos % 3 - 1  # Położenie panelu na osi x
            j = pos // 3 - 1  # Położenie panelu na osi y
            if self.put_items[pos]:
                if pos != self.change_tool:  # nie rysujemy przedmiotu przenoszonego
                    item_image = self.put_items[pos][0].image
                    item_image = pygame.transform.scale(item_image, (self.base_size, self.base_size))
                    screen.blit(
                        item_image, (3 + self.base_x + i * self.base_size, 5 + self.base_y + j * self.base_size)
                    )
                    if len(self.collected_items[pos]) > 1:
                        num = str(len(self.collected_items[pos]))
                        number = self.font.render(num, True, WHITE)
                        screen.blit(
                            number,
                            (
                                3 + self.base_x + i * self.base_size + item_image.get_width() - 7 * len(num),
                                3 + self.base_y + j * self.base_size + item_image.get_height() - 15,
                            ),
                        )

    def destroy(self):
        self.close()
        super().destroy()

    @staticmethod
    def get_intersection_with_rule_sets(equipment: set):
        return [
            key
            for key, items in CraftingTable.RULE_SETS.items()
            if len(set(items.keys()).intersection(equipment)) == len(items.keys())
        ]

    def get_player_items_to_dict(self, player):
        player_items = {}
        for item_array in player.equipment:
            if not item_array:
                continue
            player_items[item_array[0].name] = len(item_array)
        return player_items

    def create_possible_items(self, player_items: dict):
        self.possible_items = self.get_intersection_with_rule_sets(player_items.keys())

    def create_available_items(self, player_items: dict):
        available_items = []
        for possible_item in self.possible_items:
            if self.check_avaibility_to_craft(player_items, possible_item):
                available_items.append(possible_item)
        for av in available_items:
            self.possible_items.remove(av)
            self.available_items.append(av)
        self.prepare_available_items()

    def check_avaibility_to_craft(self, player_items: dict, item_name: str):
        for required_item, required_number in self.RULE_SETS[item_name].items():
            if required_number > player_items[required_item]:
                break
        else:
            return True
        return False

    def craft(self, equipment: Equipment, item_to_craft: str):
        if item_to_craft not in self.available_items:
            pass
        elif not self.check_avaibility_to_craft(self.get_player_items_to_dict(self.game.player), item_to_craft):
            pass
        else:
            requirements = self.RULE_SETS[item_to_craft]
            for rq in requirements:
                for i in range(requirements[rq]):
                    if not equipment.remove_item(rq):
                        print("Cannot craft")
                        break
            else:
                equipment.add_item(self.game.items_factory.create(item_to_craft, 0, 0))
        self.close()
        self.open()
