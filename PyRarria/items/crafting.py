from settings import *
from items.item import *
from items_factory import Factory

BASE_RULE_SET = {}
BASE_RULE_SET["crafting_table"] = {"grass_dirt": 5}
BASE_RULE_SET["stick_with_shtt"] = {"stick": 1, "shtt": 2}


rule_sets = [BASE_RULE_SET]
possible_items = []
available_items = []
sprites_to_draw = pygame.sprite.Group()
base_x = 0
base_y = HEIGHT // 2
button_down = False
equipment = None


def add_rule_set(r_set):
    global equipment
    if r_set not in rule_sets:
        rule_sets.append(r_set)
    prepare_craftable_items(equipment)


def remove_rule_set(r_set):
    global equipment
    if r_set in rule_sets:
        rule_sets.remove(r_set)
    prepare_craftable_items(equipment)


def draw_craftable_items(screen: pygame.Surface):
    sprites_to_draw.draw(screen)


def handle_craft_mouse(event, equipment, items_factory):
    global button_down

    if not button_down and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        button_down = True
    elif button_down and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        button_down = False
        for craftable in sprites_to_draw:
            if craftable.rect.collidepoint(event.pos) and craftable.name in available_items:
                craft(equipment, craftable.name, items_factory)
                break


def _create_possible_items(player_items: dict):
    for r_set in rule_sets:
        for item in _get_intersection_with_rule_set(player_items.keys(), r_set):
            possible_items.append(item)


def _prepare_possible_sprites():
    for i, item in enumerate(possible_items):
        square_image = Item.load_image("crafting_table_square").copy()
        square_image = pygame.transform.scale(square_image, (32, 32))
        item_image = Item.load_image(item).copy()
        item_image = pygame.transform.scale(item_image, (32, 32))
        item_image.fill(GRAY, special_flags=pygame.BLEND_ADD)
        square_image.blit(item_image, (0, 0))

        item_sprite = pygame.sprite.Sprite()
        item_sprite.image = square_image
        item_sprite.rect = square_image.get_rect()
        item_sprite.rect.x, item_sprite.rect.y = (
            base_x + i * square_image.get_rect().width,
            base_y + square_image.get_width(),
        )
        item_sprite.name = item
        sprites_to_draw.add(item_sprite)


def _create_available_items(player_items: dict):
    temp_list = []
    for item in possible_items:
        if _check_avaibility_to_craft(player_items, item):
            temp_list.append(item)
    for av in temp_list:
        possible_items.remove(av)
        if av not in available_items:
            available_items.append(av)


def _prepare_available_sprites():
    for i, item in enumerate(available_items):
        square_image = Item.load_image("crafting_table_square").copy()
        square_image = pygame.transform.scale(square_image, (32, 32))
        item_image = Item.load_image(item).copy()
        item_image = pygame.transform.scale(item_image, (32, 32))
        square_image.blit(item_image, (0, 0))

        item_sprite = pygame.sprite.Sprite()
        item_sprite.image = square_image
        item_sprite.rect = square_image.get_rect()
        item_sprite.rect.x, item_sprite.rect.y = (
            base_x + i * square_image.get_rect().width,
            base_y,
        )
        item_sprite.name = item
        sprites_to_draw.add(item_sprite)


def _get_intersection_with_rule_set(equipment: set, rule_set: dict):
    return [
        key for key, rules in rule_set.items() if len(set(rules.keys()).intersection(equipment)) == len(rules.keys())
    ]


def _get_player_items_to_dict(equipment):
    player_items = {}
    for item_array in equipment:
        if not item_array:
            continue
        player_items[item_array[0].name] = len(item_array)
    return player_items


def _check_avaibility_to_craft(player_items: dict, item_name: str):
    rule_set = {}
    for r_set in rule_sets:
        if item_name in r_set:
            rule_set = r_set
            break
    for required_item, required_number in r_set[item_name].items():
        if required_number > player_items[required_item]:
            break
    else:
        return True
    return False


def craft(equipment, item_to_craft: str, items_factory: Factory):
    if item_to_craft not in available_items:
        pass
    elif _check_avaibility_to_craft(_get_player_items_to_dict(equipment), item_to_craft):
        for r_set in rule_sets:
            if item_to_craft in r_set:
                requirements = r_set[item_to_craft]
                break
        for rq in requirements:
            for i in range(requirements[rq]):
                if not equipment.remove_item(rq):
                    print("Cannot craft")
                    break
        else:
            equipment.add_item(items_factory.create(item_to_craft, 0, 0))
    prepare_craftable_items(equipment)


def prepare_craftable_items(equipment):
    global available_items
    global possible_items

    player_items = _get_player_items_to_dict(equipment)
    possible_items = []
    available_items = []
    sprites_to_draw.empty()
    _create_possible_items(player_items)
    _create_available_items(player_items)
    _prepare_possible_sprites()
    _prepare_available_sprites()


def get_sprites_group():
    return sprites_to_draw
