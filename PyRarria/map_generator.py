import random
from settings import *
import time
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
map_width = 256
map_height = 128

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


def cave_generator(where, depth1, depth2, propability, go_d, go_l, go_r):  # generator cave seeda
    depth = random.randint(depth1, depth2)
    cave = []
    W = where[0]
    H = where[1]
    p = 0
    for j in range(depth):
        cave.append((W, H))
        more = random.randint(1, 100)
        if propability > more:
            here = (W, H)
            cave_generator(here, 15, 30, 0, 1, 3, 3)
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
        remove(t[0], t[1])


def remove(x, y):
    to_remove = (x, y)
    if to_remove in iron:
        iron.remove(to_remove)
    if to_remove in copper:
        copper.remove(to_remove)
    if to_remove in dirt:
        dirt.remove(to_remove)
    if to_remove in stone:
        stone.remove(to_remove)
    if to_remove in grass_dirt:
        grass_dirt.remove(to_remove)
    if to_remove in leaves:
        leaves.remove(to_remove)
    if to_remove in bone_dirt:
        bone_dirt.remove(to_remove)
    if to_remove in flint_dirt:
        flint_dirt.remove(to_remove)
    if to_remove in clay:
        clay.remove(to_remove)
    if to_remove in chrysoprase_clay:
        chrysoprase_clay.remove(to_remove)


def nbh(L,
        prop):  # funkcja pobierająca listę kolcków oraz prawdopodbieństwo dostawienia sąsiada z każdej strony każdego klocka na liście
    list = []
    for i in L:
        tmp = i
        p = random.randint(1, 100)
        l = random.randint(1, 100)
        g = random.randint(1, 100)
        d = random.randint(1, 100)
        if p < prop:
            tmp = (tmp[0] + 1, tmp[1])
            list.append(tmp)

        if l < prop:
            tmp = (tmp[0] - 1, tmp[1])
            list.append(tmp)

        if d < prop:
            tmp = (tmp[0], tmp[1] + 1)
            list.append(tmp)

        if g < prop:
            tmp = (tmp[0], tmp[1] - 1)
            list.append(tmp)

        list.append(i)
    return list


def surface_generator(anticraziness, flatness, start_height):  # anticrazines odpowiada za szybkość powrotu do płaskiego generowania, flatness odpowiada za rzadość występowania górek i dołków
    w = 0
    W = -1
    H = start_height
    a = int((100 - flatness) / 2)
    b = int((100 - anticraziness) / 2)
    for i in range(map_width):

        x = random.randint(0, 99)
        W += 1

        if w == 0:
            if a < x < 2 * a + 1:
                H += 1
                w = 1
            if x > a:
                H -= 1
                w = 2

        elif w == 1:
            H += 1
            if H > 60:
                H = 60
                w = 2
            else:
                if b < x < 2 * b + 1:
                    w = 0
                if x > 2 * b:
                    H -= 1
                    w = 2
        else:
            H -= 1
            if H < 20:
                H = 20
                w = 1
            else:
                if b < x < 2 * b + 1:
                    w = 0
                if x > 2 * b:
                    H += 1
                    w = 1
        surface.append((W, H))
        grass_dirt.append((W, H))


def generuj():
    global ruda
    global leaves
    t0 = time.time()
    # generator powierzchni

    w = 0
    W = -1
    H = 40
    for i in range(map_width):
        x = random.randint(
            0, 99
        )  # generator posiada "współczynnik załamania" ustawiony na 75%, jest to szansa na to, że zmieni się monotoniczność generwanego terenu (jeśli postawi klocek wyżej większa szansa będzie na to, że następny klocek też będzie wyżej)
        # zapobiega to generowniu losowego terenu, któy będzie wyglądał bardzo chaotycznie
        W += 1

        if w == 0:  # współczynnik ustawiony na 75% utrzymania płaskiego terenu
            if 80 < x < 91:
                H += 1
                w = 1
            if x > 90:
                H -= 1
                w = 2

        elif w == 1:  # współczynnik ustawiony na 75% opadania terenu
            H += 1
            if H > 60:
                H = 60
                w = 2
            else:
                if 60 < x < 88:
                    w = 0
                if x > 87:
                    H -= 1
                    w = 2

        else:  # współczynnik ustawiony na 75% WZNOSZENIA terenu
            H -= 1
            if H < 20:
                H = 20
                w = 1
            else:
                if 60 < x < 88:
                    w = 0
                if x > 87:
                    H += 1
                    w = 1
        surface.append((W, H))
        grass_dirt.append((W, H))
        for j in range(127):
            x = random.randint(5, 8)
            y = random.randint(0, 99)
            if j < x:
                if y < 2:
                    bone_dirt.append((W, H + j))
                elif 1 < y < 4:
                    flint_dirt.append((W, H + j))
                else:
                    dirt.append((W, H + j))  # generator ziemi
            elif H + j < map_height:
                stone.append((W, H + j))  # generator kamienia
            else:
                break
    # generator gliny
    for i in range(3):
        x = random.randint(0, len(dirt) - 1)
        x = [((dirt[x][0]), (dirt[x][1]))]

        tmp = (nbh(x, 90))
        for j in range(5):
            tmp = (nbh(tmp, 90))
            for k in tmp:
                if k not in dirt:
                    tmp.remove(k)
        for j in tmp:
            if j in dirt or j in flint_dirt or j in bone_dirt or j in stone:
                remove(j[0], j[1])
                clay.append(j)

    for i in clay:
        x = random.randint(0, 999)
        if x < 18:
            remove(i[0], i[1])
            chrysoprase_clay.append((i[0], i[1]))

    # generator RUDY
    tmpruda = []
    for i in range(100):
        H = random.randrange(surface[H][1] + 20, 127)  # generowanie rudy tylko na określonej wysokości
        W = random.randrange(0, map_width)
        tmpruda.append((W, H,))
        tmpruda = nbh(tmpruda, 70)
        tmpruda = nbh(tmpruda, 60)
        r = random.randint(0, 99)
        for j in tmpruda:
            if (j[0], j[1],) in stone:
                remove(j[0], j[1])
                if r < 15:
                    iron.append((j[0], j[1]))
                elif 14 < r < 40:
                    copper.append((j[0], j[1]))
                else:
                    coal_ore.append((j[0], j[1]))
        tmpruda = []

    # generator jaskiń
    for i in range(6):  # ile jaskiń
        where = surface[random.randint(0, len(surface) - 1)]
        cave_generator(where, 50, 70, 5, 70, 33,
                       33)  # (TUPLE Z KOORDYNATORAMI POCZATKU JASKINI, MIN GŁĘBOKOŚĆ, MAX GŁĘBOKOŚĆ, SZANSA NA ODNOGĘ, SZANSA NA KLOCEK W DÓŁ/LEWO/PRAWO
    size_machine(40, 20,
                 5)  # powiększanie jaskini (moc powiększania, szansa na średnie powiększenie, szansa na duże powiększenie)

    # generator chmur
    tmpcloud = []
    for i in range(200):
        H = random.randrange(0, 12)  # generowanie rudy tylko na określonej wysokości
        W = random.randrange(0, 255)
        tmpcloud.append((W, H))
        tmpcloud = nbh(tmpcloud, 10)
        tmpcloud = nbh(tmpcloud, 10)
        for j in tmpcloud:
            if 256 > j[0] > -1 and 13 > j[1] > -1:
                cloud.append(j)
        tmpcloud = []

    # generator drzew (pień)
    banned = []
    for i in range(50):
        where = grass_dirt[random.randint(0, len(grass_dirt) - 1)]
        W = where[0]
        H = where[1] - 1
        height = random.randint(3, 5)
        if W not in banned:
            for h in range(height):
                x = random.randint(0, 99)
                if x < 20 and h > 1:
                    log_hole.append((W, H))
                else:
                    log.append((W, H))
                H -= 1
                if h + 1 == height:
                    leaves.append((W, H,))

        banned.append(where[0])
        banned.append(where[0] - 1)
        banned.append(where[0] + 1)

    # generator drzew (liście)
    tmpleaves = []
    for l in leaves:
        for w in range(-2, 3):
            for h in range(-1, 3):
                if (
                        (w != -2 or h != -1)
                        and (w != 2 or h != -1)
                        and (w != -2 or h != 2)
                        and (w != 2 or h != 2)
                        and 256 > (l[0] + w) > -1
                        and (l[0] + w, l[1] + h) not in log
                        and (l[0] + w, l[1] + h) not in log_hole
                ):
                    tmpleaves.append((l[0] + w, l[1] + h))
    leaves = tmpleaves
    for i in leaves:
        x = random.randint(1, 5)
        if x == 1:
            leaves.remove(i)
            apple_leaves.append(i)

    # generator kępek
    for i in grass_dirt:
        x = random.randint(1, 10)
        if x < 8 and ((i[0], i[1] - 1) not in log) and ((i[0], i[1] - 1) not in log_hole):
            x = random.randint(0, 99)
            if x < 45:
                grass.append((i[0], i[1] - 1))
            elif 44 < x < 90:
                tall_grass.append((i[0], i[1] - 1))
            elif 89 < x < 95:
                mushroom_brown.append((i[0], i[1] - 1))
            else:
                mushroom_red.append((i[0], i[1] - 1))

    # generator diamentów
    for i in range(200):
        H = random.randrange(80, 128)  # generowanie diamentów tylko na określonej wysokości
        W = random.randrange(0, map_width)
        r = random.randint(0, 10)
        if (W, H) in stone:
            remove(W, H)
            if 1 >= r >= 0:
                diamond1.append((W, H))
            elif 4 >= r >= 2:
                diamond2.append((W, H))
            else:
                diamond3.append((W, H))

    # generator akwarium
    W = 0
    H = 0
    for i in range(-1, map_height + 1):
        for j in range(-1, map_width + 1):
            if j == -1 or j == map_width or i == -1 or i == map_height:
                glass.append((j, i))
    t1 = time.time()
    print("czas generowania: " + str(t1-t0)[0:6]+"s")
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


def cloudlist():
    return cloud


def stonelist():
    return stone


def grasslist():
    return grass


def create_world(grid, items_factory):
    for i in range(300):
        for j in range(-20, 300):
            grid[(i * BLOCK_SIZE, j * BLOCK_SIZE)] = None

    dirt_list = [items_factory.create("dirt", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in dirtlist()]
    for blok in dirt_list:
        grid[(blok.position.x, blok.position.y)] = blok

    bone_dirt_list = [items_factory.create("bone_dirt", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                      bone_dirtlist()]
    for blok in bone_dirt_list:
        grid[(blok.position.x, blok.position.y)] = blok

    flint_dirt_list = [items_factory.create("flint_dirt", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                       flint_dirtlist()]
    for blok in flint_dirt_list:
        grid[(blok.position.x, blok.position.y)] = blok

    chrysoprase_clay_list = [items_factory.create("chrysoprase_clay", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for
                             block in chyrsoplase_claylist()]
    for blok in chrysoprase_clay_list:
        grid[(blok.position.x, blok.position.y)] = blok

    clay_list = [items_factory.create("clay", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in claylist()]
    for blok in clay_list:
        grid[(blok.position.x, blok.position.y)] = blok

    stone_list = [items_factory.create("stone", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in stonelist()]
    for blok in stone_list:
        grid[(blok.position.x, blok.position.y)] = blok

    iron_list = [items_factory.create("iron", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in ironlist()]
    for blok in iron_list:
        grid[(blok.position.x, blok.position.y)] = blok

    mushroom_brown_list = [items_factory.create("mushroom_brown", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for
                           block in mushroom_brownlist()]
    for blok in mushroom_brown_list:
        grid[(blok.position.x, blok.position.y)] = blok

    mushroom_red_list = [items_factory.create("mushroom_red", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for
                         block in mushroom_redlist()]
    for blok in mushroom_red_list:
        grid[(blok.position.x, blok.position.y)] = blok

    coal_ore_list = [items_factory.create("coal_ore", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                     coal_orelist()]
    for blok in coal_ore_list:
        grid[(blok.position.x, blok.position.y)] = blok

    copper_list = [items_factory.create("copper", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                   copperlist()]
    for blok in copper_list:
        grid[(blok.position.x, blok.position.y)] = blok

    log_list = [items_factory.create("log", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in loglist()]
    for blok in log_list:
        grid[(blok.position.x, blok.position.y)] = blok

    log_hole_list = [items_factory.create("log_hole", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                     log_holelist()]
    for blok in log_hole_list:
        grid[(blok.position.x, blok.position.y)] = blok

    diamond1_list = [items_factory.create("diamond1", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                     diamond1list()]
    for blok in diamond1_list:
        grid[(blok.position.x, blok.position.y)] = blok

    diamond2_list = [items_factory.create("diamond2", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                     diamond2list()]
    for blok in diamond2_list:
        grid[(blok.position.x, blok.position.y)] = blok

    diamond3_list = [items_factory.create("diamond3", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                     diamond3list()]
    for blok in diamond3_list:
        grid[(blok.position.x, blok.position.y)] = blok

    cloud_list = [items_factory.create("cloud", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in cloudlist()]
    for blok in cloud_list:
        grid[(blok.position.x, blok.position.y)] = blok

    grass_list = [items_factory.create("grass", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in grasslist()]
    for blok in grass_list:
        grid[(blok.position.x, blok.position.y)] = blok

    grass_dirt_list = [items_factory.create("grass_dirt", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                       grass_dirtlist()]
    for blok in grass_dirt_list:
        grid[(blok.position.x, blok.position.y)] = blok

    tall_grass_list = [items_factory.create("tall_grass", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                       tall_grasslist()]
    for blok in tall_grass_list:
        grid[(blok.position.x, blok.position.y)] = blok

    leaves_list = [items_factory.create("leaves", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                   leaveslist()]
    for blok in leaves_list:
        grid[(blok.position.x, blok.position.y)] = blok

    apple_leaves_list = [items_factory.create("apple_leaves", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                         appleleaveslist()]
    for blok in apple_leaves_list:
        grid[(blok.position.x, blok.position.y)] = blok

    glass_list = [items_factory.create("glass", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in glasslist()]
    for blok in glass_list:
        grid[(blok.position.x, blok.position.y)] = blok
