import random
from settings import *

cloud = []
platformy = []
powierzchnia = []
copper = []
iron = []
tree = []
pas_rudy = []
wood = []
leaf = []
diamond1 = []
diamond2 = []
diamond3 = []
glass = []
stone = []
dirt = []
grass = []
cave_seed = []
clump = []
map_width = 256
map_height = 128

non_colision1 = ["wood", "leaf"]
non_colision2 = ["clump"]
NON_COLLISION_OBJECTS.append("clump")
NON_COLLISION_OBJECTS.append("leaf")
NON_COLLISION_OBJECTS.append("wood")


def cave_generator(where, depth1, depth2, propability, go_d, go_l, go_r):
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


def size_machine(power, p1, p2):
    size = random.randint(1, 100)
    tmpcave = sasiad(cave_seed, power)
    tmpcave = sasiad(tmpcave, power)
    if size < p2:
        tmpcave = sasiad(tmpcave, power)
    if size < p1:
        tmpcave = sasiad(tmpcave, power)
    for t in tmpcave:
        remove(t[0], t[1])


def remove(x, y):  #
    usun = (x, y)
    if usun in iron:
        iron.remove(usun)
    if usun in copper:
        copper.remove(usun)
    if usun in dirt:
        dirt.remove(usun)
    if usun in stone:
        stone.remove(usun)
    if usun in grass:
        grass.remove(usun)


def sasiad(
        L, prop
):  # funkcja pobierająca listę kolcków oraz prawdopodbieństwo dostawienia sąsiada z każdej strony każdego klocka na liście
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


def generuj():
    global ruda
    global leaf

    # generator powierzchni

    w = 0
    W = -1
    H = 40
    for i in range(256):
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
        powierzchnia.append((W, H))
        grass.append((W, H))
        for j in range(127):
            x = random.randint(5, 8)
            if j < x:
                dirt.append((W, H+j))  # generator ziemi
            elif H+j < map_height:
                stone.append((W, H+j))  # generator kamienia
            else:
                break


    # generator RUDY
    tmpruda = []
    for i in range(200):
        H = random.randrange(60, 127)  # generowanie rudy tylko na określonej wysokości
        W = random.randrange(0, map_width)
        tmpruda.append((W, H,))
        tmpruda = sasiad(tmpruda, 70)
        tmpruda = sasiad(tmpruda, 60)
        r = random.randint(0, 4)
        for j in tmpruda:
            if (j[0], j[1],) in stone:
                remove(j[0], j[1])
                if r > 1:
                    iron.append((j[0], j[1]))
                else:
                    copper.append((j[0], j[1]))
        tmpruda = []

    # generator jaskiń
    for i in range(9):  # ile jaskiń
        where = powierzchnia[random.randint(0, len(powierzchnia) - 1)]
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
        tmpcloud = sasiad(tmpcloud, 80)
        tmpcloud = sasiad(tmpcloud, 80)
        for j in tmpcloud:
            if 256 > j[0] > -1 and 13 > j[1] > -1:
                cloud.append(j)
        tmpcloud = []

    # generator drzew (pień)
    banned = []
    for i in range(20):
        where = grass[random.randint(0, len(grass) - 1)]
        W = where[0]
        H = where[1] - 1
        height = random.randint(3, 5)
        if W not in banned:
            for h in range(height):
                wood.append((W, H))
                H -= 1
                if h + 1 == height:
                    leaf.append((W, H,))
        banned.append(where[0])
        banned.append(where[0] - 1)
        banned.append(where[0] + 1)

    # generator drzew (liście)
    tmpleaf = []
    for l in leaf:
        for w in range(-2, 3):
            for h in range(-1, 3):
                if (
                        (w != -2 or h != -1)
                        and (w != 2 or h != -1)
                        and (w != -2 or h != 2)
                        and (w != 2 or h != 2)
                        and 256 > (l[0] + w) > -1
                        and (l[0] + w, l[1] + h) not in wood
                ):
                    tmpleaf.append((l[0] + w, l[1] + h))
    leaf = tmpleaf

    # generator kępek
    for i in grass:
        x = random.randint(1, 10)
        if x < 7 and ((i[0], i[1] - 1) not in wood):
            clump.append((i[0], i[1] - 1))

    # generator diamentów
    for i in range(200):
        H = random.randrange(80, 127)  # generowanie diamentów tylko na określonej wysokości
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


def dirtlist():
    return dirt


def diamond1list():
    return diamond1


def diamond2list():
    return diamond2


def diamond3list():
    return diamond3


def trees():
    return tree


def ironlist():
    return iron


def copperlist():
    return copper


def woodlist():
    return wood


def leaflist():
    return leaf


def grasslist():
    return grass


def glasslist():
    return glass


def cloudlist():
    return cloud


def stonelist():
    return stone


def clumplist():
    return clump


def create_world(grid, items_factory):
    for i in range(300):
        for j in range(-20, 300):
            grid[(i * BLOCK_SIZE, j * BLOCK_SIZE)] = None

    block_list = [items_factory.create("dirt", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in dirtlist()]
    for blok in block_list:
        grid[(blok.position.x, blok.position.y)] = blok

    stone_list = [items_factory.create("stone", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in stonelist()]
    for blok in stone_list:
        grid[(blok.position.x, blok.position.y)] = blok

    iron_list = [items_factory.create("iron", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in ironlist()]
    for blok in iron_list:
        grid[(blok.position.x, blok.position.y)] = blok

    copper_list = [items_factory.create("copper", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                   copperlist()]
    for blok in copper_list:
        grid[(blok.position.x, blok.position.y)] = blok

    wood_list = [items_factory.create("wood", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in woodlist()]
    for blok in wood_list:
        grid[(blok.position.x, blok.position.y)] = blok

    leaf_list = [items_factory.create("leaf", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in leaflist()]
    for blok in leaf_list:
        grid[(blok.position.x, blok.position.y)] = blok

    diamond1_list = [items_factory.create("diamond1", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                     diamond1list()]
    for blok in diamond1_list:
        grid[(blok.position.x, blok.position.y)] = blok

    diamond2_list = [items_factory.create("diamond2", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in
                     diamond2list()]
    for blok in diamond2_list:
        grid[(blok.position.x, blok.position.y)] = blok

    diamond3_list = [items_factory.create("diamond3", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in diamond3list()]
    for blok in diamond3_list:
        grid[(blok.position.x, blok.position.y)] = blok

    cloud_list = [items_factory.create("cloud", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in cloudlist()]
    for blok in cloud_list:
        grid[(blok.position.x, blok.position.y)] = blok

    clump_list = [items_factory.create("clump", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in clumplist()]
    for blok in clump_list:
        grid[(blok.position.x, blok.position.y)] = blok

    grass_list = [items_factory.create("grass", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in grasslist()]
    for blok in grass_list:
        grid[(blok.position.x, blok.position.y)] = blok

    glass_list = [items_factory.create("glass", block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE) for block in glasslist()]
    for blok in glass_list:
        grid[(blok.position.x, blok.position.y)] = blok
