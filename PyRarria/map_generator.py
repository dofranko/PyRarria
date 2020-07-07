import random
from settings import *
import time

map_width = 2560
map_height = 128
MAP_MATRIX = [["XX"] * map_height for i in range(map_width)]
cloud = []
platformy = []
surface = []
copper = []
iron = []
tree = []
pas_rudy = []
log = []
log_hole = []
leaves = []
diamond1 = []
diamond2 = []
diamond3 = []
glass = []
stone = []
bone_dirt = []
flint_dirt = []
dirt = []
grass_dirt = []
cave_seed = []
grass = []
tall_grass = []
apple_leaves = []
coal_ore = []
mushroom_brown = []
mushroom_red = []
chrysoprase_clay = []
clay = []
cave = []
banned = []
ore_dictionary = {
    'copper': {"min_height": 20,
               "max_height": map_height - 1,
               "amount": 50,
               "size": 3,
               "propability": 30,
               "how_many": 40},

    'iron': {"min_height": 40,
             "max_height": map_height - 1,
             "amount": 40,
             "size": 3,
             "propability": 50,
             "how_many": 30},

    'coal': {"min_height": 10,
             "max_height": map_height - 1,
             "amount": 60,
             "size": 5,
             "propability": 20,
             "how_many": 60}
}

non_colision1 = ["log", "leaves"]
non_colision2 = ["grass"]
NON_COLLISION_OBJECTS.append("grass")
NON_COLLISION_OBJECTS.append("leaves")
NON_COLLISION_OBJECTS.append("log")
NON_COLLISION_OBJECTS.append("log_hole")
NON_COLLISION_OBJECTS.append("apple_leaves")
NON_COLLISION_OBJECTS.append("tall_grass")
NON_COLLISION_OBJECTS.append("mushroom_red")
NON_COLLISION_OBJECTS.append("mushroom_brown")


def nbh(L,
        prop):  # funkcja pobierająca listę kolcków oraz prawdopodbieństwo dostawienia sąsiada z każdej strony każdego klocka na liście
    list = []
    for i in L:
        tmp = i
        p = random.randint(0, 100)
        l = random.randint(0, 100)
        g = random.randint(0, 100)
        d = random.randint(0, 100)
        if p < prop and tmp[0] < map_width:
            tmp = (tmp[0] + 1, tmp[1])
            list.append(tmp)

        if l < prop and tmp[0] > 0:
            tmp = (tmp[0] - 1, tmp[1])
            list.append(tmp)

        if d < prop and tmp[1] < map_height:
            tmp = (tmp[0], tmp[1] + 1)
            list.append(tmp)

        if g < prop and tmp[1] > 0:
            tmp = (tmp[0], tmp[1] - 1)
            list.append(tmp)

        list.append(i)
    return list


def surface_generator(min_depth, max_depth, start_height, anticraziness, flatness):
    w = 0
    W = -1
    H = start_height
    a = (100 - flatness) / 2
    b = (100 - anticraziness)
    for i in range(map_width):
        x = random.randint(0, 99)
        W += 1

        if w == 0:
            if a - 1 < x < 2 * a:
                H += 1
                grass_dirt.append((W, H))
                MAP_MATRIX[W][H] = "01"
                surface.append((W, H))
                if (len(grass_dirt)) == map_width:
                    break
                W += 1
                w = 1

            elif x < a:
                H -= 1
                grass_dirt.append((W, H))
                MAP_MATRIX[W][H] = "01"
                surface.append((W, H))
                if (len(grass_dirt)) == map_width:
                    break
                W += 1
                w = 2

        elif w == 1:
            H += 1
            if H > max_depth:
                H = max_depth
                w = 2
            else:
                if x < b:
                    w = 0
                    grass_dirt.append((W, H))
                    MAP_MATRIX[W][H] = "01"
                    surface.append((W, H))
                    if (len(grass_dirt)) == map_width:
                        break
                    W += 1
        else:
            H -= 1
            if H < min_depth:
                H = min_depth
                w = 1
            else:
                if x < b:
                    w = 0
                    grass_dirt.append((W, H))
                    MAP_MATRIX[W][H] = "01"
                    surface.append((W, H))
                    if (len(grass_dirt)) == map_width:
                        break
                    W += 1
        grass_dirt.append((W, H))
        MAP_MATRIX[W][H] = "01"
        surface.append((W, H))
        if (len(grass_dirt)) == map_width:
            break


def cave_generator(where, depth1, depth2, propability, go_d, go_l, go_r):  # generator cave seeda
    depth = random.randint(depth1, depth2)
    cave = []
    W = where[0]
    H = where[1]
    p = 0
    for j in range(depth):
        if -1 < W < map_width and -1 < H < map_height:
            MAP_MATRIX[W][H] = "XX"
        cave.append((W, H))
        more = random.randint(1, 100)
        if propability > more:
            here = (W, H)
            cave_generator(here, 30, 80, 1, 1, 3, 3)
        cave_seed.append((W, H))
        R = go_d + go_l + go_r
        direction = random.randint(0, R)
        if direction < go_d:
            H += 1
            p = 0
        elif go_d + go_l > direction > go_d - 1 and (p == 0 or p == 1):
            W += 1
            p = 1
        elif direction > go_d + go_l - 1 and (p == 0 or p == 2):
            p = 2
            W -= 1


def size_machine(power, p1, p2):  # powiększanie cave seeda
    size = random.randint(1, 100)
    tmpcave = nbh(cave_seed, power)
    tmpcave = nbh(tmpcave, power)
    if size < p2:
        tmpcave = nbh(tmpcave, power)
    if size < p1:
        tmpcave = nbh(tmpcave, power)
    for t in tmpcave:
        if t[1] < map_height + 1 and (-1 < t[0] < map_width + 1):
            cave.append(t)
            if -1<t[0]<map_width and -1<t[1]<map_height:
                MAP_MATRIX[t[0]][t[1]] = "XX"
            if t in grass_dirt:
                grass_dirt.remove(t)
                banned.append(t)


def dirt_generator(height, gradient, gradient_start):
    for i in grass_dirt:
        for j in range(1, gradient_start):
            dirt.append((i[0], i[1] + j))
            MAP_MATRIX[i[0]][i[1] + j] = "00"
        for j in range(gradient_start, height + 1):
            x = random.randint(0, 99)
            if gradient / j * height > x:
                dirt.append((i[0], i[1] + j))
                MAP_MATRIX[i[0]][i[1] + j] = "00"
            else:
                stone.append((i[0], i[1] + j))
                MAP_MATRIX[i[0]][i[1] + j] = "02"
    for i in grass_dirt:
        for j in range(height, map_height):
            if i[1] + j < map_height:
                stone.append((i[0], i[1] + j))
                MAP_MATRIX[i[0]][i[1] + j] = "02"
            else:
                break


def cloud_generator(min_height, max_height, size, propability, how_many):
    for i in range(how_many):
        w = random.randint(0, map_width)
        h = random.randint(max_height, min_height)
        cloud.append((w, h))
    for i in range(size):
        cloud.extend(nbh(cloud, propability))


def ore_generator(ore_dic, lista):
    L = random.choices(surface, k=ore_dic["how_many"])
    for i in L:
        h = random.randint(i[1] + ore_dic["min_height"], ore_dic["max_height"])
        lista.append((i[0], h))
    for i in range(ore_dic["size"]):
        # TODO Ciekawostka, jeśli użyjemy tutaj append zamiast extend funkcja zwróci nam listę z pierwszego append'u, nie drugiego
        lista.extend(nbh(lista, ore_dic["propability"]))


def singleblocks_generator(newlist, oldlist, propability):
    k = int(len(oldlist) * propability / 100)
    if k == 0:
        k = 1
    newlist.extend(random.sample(oldlist, k))


def multiblock_generator(newlist, oldlist, propability, size, nbhpropability):
    newlist.extend(random.sample(oldlist, int(len(oldlist) * propability / 100)))
    for i in range(size):
        tmp = []
        tmp.extend(nbh(newlist, nbhpropability))
        for j in tmp:
            if j in oldlist:
                newlist.append(j)


def littlegrass_generator(propability, grassP, tallgrassP, redmushroomP, mushroomchickenP):
    tmp = []
    tmp.extend(random.sample(grass_dirt, int(len(grass_dirt) * propability / 100)))
    for i in tmp:
        x = random.randint(0, grassP + tallgrassP + redmushroomP + mushroomchickenP)
        if x >= 0 and x < grassP:
            grass.append((i[0], i[1] - 1))
            MAP_MATRIX[i[0]][i[1] - 1] = "06"
        elif x >= grassP and x < grassP + tallgrassP:
            tall_grass.append((i[0], i[1] - 1))
            MAP_MATRIX[i[0]][i[1] - 1] = "07"
        elif x >= grassP + tallgrassP and x < grassP + tallgrassP + redmushroomP:
            mushroom_red.append((i[0], i[1] - 1))
            MAP_MATRIX[i[0]][i[1] - 1] = "08"
        else:
            mushroom_brown.append((i[0], i[1] - 1))
            MAP_MATRIX[i[0]][i[1] - 1] = "09"


def glass_generator():
    for i in range(-1, map_height + 1):
        for j in range(-1, map_width + 1):
            if j == -1 or j == map_width or i == -1 or i == map_height:
                glass.append((j, i))


def log_generator(min_hole, max_hole):
    x = 0
    while 1:
        i = random.randint(min_hole, max_hole)
        x += i
        if x >= map_width:
            break
        if surface[x] not in banned:
            t = surface[x]
            log.append((t[0], t[1] - 1))


def generuj():
    t0 = time.time()

    surface_generator(20, 60, 40, 40, 80)  # min/max wysokość, początkowa wysokość, wysokość górek, rzadkość górek
    dirt_generator(10, 40, 4)

    for i in range(6):  # ile jaskiń
        where = surface[random.randint(0, len(surface) - 1)]
        cave_generator(where, 80, 200, 5, 70, 33,
                       33)  # (TUPLE Z KOORDYNATORAMI POCZATKU JASKINI, MIN GŁĘBOKOŚĆ, MAX GŁĘBOKOŚĆ, SZANSA NA ODNOGĘ, SZANSA NA KLOCEK W DÓŁ/LEWO/PRAWO

    size_machine(40, 40,
                 15)  # powiększanie jaskini (moc powiększania, szansa na średnie powiększenie, szansa na duże powiększenie)
    glass_generator()
    log_generator(5, 10)
    ore_generator(ore_dictionary['copper'], copper)
    ore_generator(ore_dictionary['iron'], iron)
    ore_generator(ore_dictionary['coal'], coal_ore)
    t1 = time.time()
    cloud_generator(10, 0, 6, 7, 30)
    singleblocks_generator(bone_dirt, dirt, 2.5)
    singleblocks_generator(flint_dirt, dirt, 2.5)
    singleblocks_generator(diamond1, stone, 0.5)
    singleblocks_generator(diamond2, stone, 0.25)
    singleblocks_generator(diamond3, stone, 0.125)
    multiblock_generator(clay, dirt, 0.25, 4, 80)
    littlegrass_generator(60, 4, 3, 1, 1)
    singleblocks_generator(chrysoprase_clay, clay, 0.0001)
    print("czas generowania mapy: " + str(t1 - t0)[0:6] + "s")
    save_world()


def dirtlist():
    return dirt


def bone_dirtlist():
    return bone_dirt


def flint_dirtlist():
    return flint_dirt


def diamond1list():
    return diamond1


def diamond2list():
    return diamond2


def diamond3list():
    return diamond3


def chyrsoplase_claylist():
    return chrysoprase_clay


def claylist():
    return clay


def trees():
    return tree


def ironlist():
    return iron


def copperlist():
    return copper


def coal_orelist():
    return coal_ore


def loglist():
    return log


def log_holelist():
    return log_hole


def leaveslist():
    return leaves


def appleleaveslist():
    return apple_leaves


def grass_dirtlist():
    return grass_dirt


def tall_grasslist():
    return tall_grass


def mushroom_redlist():
    return mushroom_red


def mushroom_brownlist():
    return mushroom_brown


def glasslist():
    return glass


def cavelist():
    return cave


def cloudlist():
    return cloud


def stonelist():
    return stone


def grasslist():
    return grass


def save_world():
    save = open("map_save", "w")
    for j in range(map_height):
        for i in range(map_width):
            save.write("%s" % MAP_MATRIX[i][j])
        save.write("\n")


def create_world(grid, items_factory):
    t0 = time.time()
    MAP = []
    map_width = 0
    map_height = 0
    with open('map_save') as f:
        lines = f.read().splitlines()
        for i in lines:
            map_height += 1
            line = []
            for j in range(int(len(i) / 2)):
                line.append(str(i[2 * j]) + str(i[2 * j + 1]))
                map_width += 1
            MAP.append(line)
    map_width = int(map_width / map_height)

    for j in range(map_height):
        for i in range(map_width):
            if MAP[j][i] == '00':
                block = items_factory.create("dirt", i * BLOCK_SIZE, j * BLOCK_SIZE)
                grid[(block.position.x, block.position.y)] = block
            elif MAP[j][i] == '01':
                block = items_factory.create("grass_dirt", i * BLOCK_SIZE, j * BLOCK_SIZE)
                grid[(block.position.x, block.position.y)] = block
            elif MAP[j][i] == '02':
                block = items_factory.create("stone", i * BLOCK_SIZE, j * BLOCK_SIZE)
                grid[(block.position.x, block.position.y)] = block
            elif MAP[j][i] == '03':
                block = items_factory.create("coal_ore", i * BLOCK_SIZE, j * BLOCK_SIZE)
                grid[(block.position.x, block.position.y)] = block
            elif MAP[j][i] == '04':
                block = items_factory.create("copper_ore", i * BLOCK_SIZE, j * BLOCK_SIZE)
                grid[(block.position.x, block.position.y)] = block
            elif MAP[j][i] == '05':
                block = items_factory.create("iron_ore", i * BLOCK_SIZE, j * BLOCK_SIZE)
                grid[(block.position.x, block.position.y)] = block
            elif MAP[j][i] == '06':
                block = items_factory.create("grass", i * BLOCK_SIZE, j * BLOCK_SIZE)
                grid[(block.position.x, block.position.y)] = block
            elif MAP[j][i] == '07':
                block = items_factory.create("tall_grass", i * BLOCK_SIZE, j * BLOCK_SIZE)
                grid[(block.position.x, block.position.y)] = block
            elif MAP[j][i] == '08':
                block = items_factory.create("mushroom_red", i * BLOCK_SIZE, j * BLOCK_SIZE)
                grid[(block.position.x, block.position.y)] = block
            elif MAP[j][i] == '09':
                block = items_factory.create("mushroom_brown", i * BLOCK_SIZE, j * BLOCK_SIZE)
                grid[(block.position.x, block.position.y)] = block
            elif MAP[j][i] == 'XX':
                grid[(i * BLOCK_SIZE, j * BLOCK_SIZE)] = None

    for j in range(-1, map_height + 1):
        for i in range(-1, map_width + 1):
            if i == -1 or i == map_width or j == -1 or j == map_height:
                block = items_factory.create("glass", i * BLOCK_SIZE, j * BLOCK_SIZE)
                grid[(block.position.x, block.position.y)] = block

    t1 = time.time()
    print("czas tworzenia świata: " + str(t1 - t0)[0:6] + "s")
#00 - dirt
#01 - grass_dirt
#02 - stone
#03 - coal_ore
#04 - copper_ore
#05 - iron_ore
#06 - grass
#07 - tall_grass
#08 - mushroom_red
#09 - mushroom_brown (chicken)
#0A - diamond1
#0B - diamond2
#0C - diamond3
#0D - clay
#0E - chrysoprase_clay
#0F - cloud
#10 - log
#11 - log_hole
#11 - leaves
#12 - apple_leaves
#12 - bone_dirt
#13 - flint_dirt