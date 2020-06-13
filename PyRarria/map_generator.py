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
            H += 50
            p = 0
        elif go_d + go_l > direction > go_d - 1 and (p == 0 or p == 1):
            W += 50
            p = 1
        elif direction > go_d + go_l - 1 and (p == 0 or p == 2):
            p = 2
            W -= 50


def size_machine(power, p1, p2):
    size = random.randint(1, 100)
    tmpcave = sasiad(cave_seed, power)
    if size < p2:
        tmpcave = sasiad(tmpcave, power)
    if size < p1:
        tmpcave = sasiad(tmpcave, power)
    print(len(tmpcave))
    for t in tmpcave:
        remove(t[0], t[1])


def wejscie(x, y):
    remove(x, y)
    remove(x + 50, y)
    remove(x - 50, y)
    remove(x, y + 50)
    remove(x, y - 50)
    remove(x + 50, y + 50)
    remove(x - 50, y + 50)
    remove(x + 50, y - 50)
    remove(x - 50, y - 50)


def remove(x, y):  #
    usun = (x, y, 50, 50)
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
            tmp = (tmp[0] + 50, tmp[1], 50, 50)
            list.append(tmp)

        if l < prop:
            tmp = (tmp[0] - 50, tmp[1], 50, 50)
            list.append(tmp)

        if d < prop:
            tmp = (tmp[0], tmp[1] + 50, 50, 50)
            list.append(tmp)

        if g < prop:
            tmp = (tmp[0], tmp[1] - 50, 50, 50)
            list.append(tmp)

        list.append(i)
    return list


def generuj():
    global ruda
    global leaf

    # generator powierzchni

    w = 0
    W = 0
    H = 500
    for i in range(255):
        x = random.randint(
            0, 99
        )  # generator posiada "współczynnik załamania" ustawiony na 75%, jest to szansa na to, że zmieni się monotoniczność generwanego terenu (jeśli postawi klocek wyżej większa szansa będzie na to, że następny klocek też będzie wyżej)
        # zapobiega to generowniu losowego terenu, któy będzie wyglądał bardzo chaotycznie
        W += 50

        if w == 0:  # współczynnik ustawiony na 75% utrzymania płaskiego terenu
            if 80 < x < 91:
                H += 50
                w = 1
            if x > 90:
                H -= 50
                w = 2

        elif w == 1:  # współczynnik ustawiony na 75% opadania terenu
            H += 50
            if H > 5000:
                H = 5000
                w = 2
            else:
                if 60 < x < 88:
                    w = 0
                if x > 87:
                    H -= 50
                    w = 2

        else:  # współczynnik ustawiony na 75% WZNOSZENIA terenu
            H -= 50
            if H < 400:
                H = 400
                w = 1
            else:
                if 60 < x < 88:
                    w = 0
                if x > 87:
                    H += 50
                    w = 1

        for j in range(10000):
            x = random.randint(3, 6)
            if j < x:
                dirt.append((W, H + 50 * j, 50, 50))  # generator ziemi
            elif H + 50 * j < 5600:
                stone.append((W, H + 50 * j, 50, 50))  # generator kamienia
            else:
                break
        powierzchnia.append((W, H))
        grass.append((W, H, 50, 50))
    print(len(powierzchnia))
    # generator RUDY

    tmpruda = []
    for i in range(200):
        H = random.randrange(1000, 5600, 50)  # generowanie rudy tylko na określonej wysokości
        W = random.randrange(0, 12750, 50)
        tmpruda.append((W, H, 50, 50))
        tmpruda = sasiad(tmpruda, 70)
        tmpruda = sasiad(tmpruda, 60)
        r = random.randint(0, 4)
        for j in tmpruda:
            if (j[0], j[1], 50, 50) in stone:
                remove(j[0], j[1])
                if r > 1:
                    iron.append((j[0], j[1], 50, 50))
                else:
                    copper.append((j[0], j[1], 50, 50))
        tmpruda = []

    # generator jaskiń
    for i in range(9):  # ile jaskiń
        where = powierzchnia[random.randint(0, len(powierzchnia) - 1)]
        wejscie(where[0], where[1])
        cave_generator(
            where, 50, 70, 5, 70, 33, 33
        )  # (TUPLE Z KOORDYNATORAMI POCZATKU JASKINI, MIN GŁĘBOKOŚĆ, MAX GŁĘBOKOŚĆ, SZANSA NA ODNOGĘ, SZANSA NA KLOCEK W DÓŁ/LEWO/PRAWO
    size_machine(
        40, 20, 5
    )  # powiększanie jaskini (moc powiększania, szansa na średnie powiększenie, szansa na duże powiększenie)

    # generator chmur
    tmpcloud = []
    for i in range(200):
        H = random.randrange(-750, 100, 50)  # generowanie rudy tylko na określonej wysokości
        W = random.randrange(0, 12750, 50)
        tmpcloud.append((W, H, 50, 50))
        tmpcloud = sasiad(tmpcloud, 80)
        tmpcloud = sasiad(tmpcloud, 80)
        for j in tmpcloud:
            if 12750 > j[0] > 0 and -750 < j[1]:
                cloud.append(j)
        tmpcloud = []

    # generator drzew (pień)
    banned = []
    for i in range(20):
        where = grass[random.randint(0, len(grass) - 1)]
        W = where[0]
        H = where[1] - 50
        height = random.randint(3, 5)
        if W not in banned:
            for h in range(height):
                wood.append((W, H, 50, 50))
                H -= 50
                if h + 1 == height:
                    leaf.append((W, H, 50, 50))
        banned.append(where[0])
        banned.append(where[0] - 50)
        banned.append(where[0] + 50)

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
                    and 12750 > (l[0] + w * 50) > 0
                    and (l[0] + w * 50, l[1] + 50 * h, 50, 50) not in wood
                ):
                    tmpleaf.append((l[0] + w * 50, l[1] + 50 * h, 50, 50))
    leaf = tmpleaf

    # generator kępek
    for i in grass:
        x = random.randint(1, 10)
        if x < 7 and ((i[0], i[1] - 50, 50, 50) not in wood):
            clump.append((i[0], i[1] - 50, 50, 50))

    # generator diamentów
    for i in range(1000):
        H = random.randrange(1500, 5600, 50)  # generowanie diamentów tylko na określonej wysokości
        W = random.randrange(0, 12750, 50)
        r = random.randint(0, 10)
        if (W, H, 50, 50) in stone:
            remove(W, H)
            if 1 >= r >= 0:
                diamond1.append((W, H, 50, 50))
            elif 4 >= r >= 2:
                diamond2.append((W, H, 50, 50))
            else:
                diamond3.append((W, H, 50, 50))

    # generator akwarium
    W = 0
    H = 500
    for i in range(128):
        for j in range(256):
            if i == 0 or i == 127 or j == 0 or j == 255:
                glass.append((W + 50 * j, H + 50 * (i - 25), 50, 50))


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

    block_list = [items_factory.create("dirt", block[0], block[1]) for block in dirtlist()]
    for blok in block_list:
        grid[(blok.position.x, blok.position.y)] = blok

    stone_list = [items_factory.create("stone", block[0], block[1]) for block in stonelist()]
    for blok in stone_list:
        grid[(blok.position.x, blok.position.y)] = blok

    grass_list = [items_factory.create("grass", block[0], block[1]) for block in grasslist()]
    for blok in grass_list:
        grid[(blok.position.x, blok.position.y)] = blok

    iron_list = [items_factory.create("iron", block[0], block[1]) for block in ironlist()]
    for blok in iron_list:
        grid[(blok.position.x, blok.position.y)] = blok

    copper_list = [items_factory.create("copper", block[0], block[1]) for block in copperlist()]
    for blok in copper_list:
        grid[(blok.position.x, blok.position.y)] = blok

    wood_list = [items_factory.create("wood", block[0], block[1]) for block in woodlist()]
    for blok in wood_list:
        grid[(blok.position.x, blok.position.y)] = blok

    leaf_list = [items_factory.create("leaf", block[0], block[1]) for block in leaflist()]
    for blok in leaf_list:
        grid[(blok.position.x, blok.position.y)] = blok

    diamond1_list = [items_factory.create("diamond1", block[0], block[1]) for block in diamond1list()]
    for blok in diamond1_list:
        grid[(blok.position.x, blok.position.y)] = blok

    diamond2_list = [items_factory.create("diamond2", block[0], block[1]) for block in diamond2list()]
    for blok in diamond2_list:
        grid[(blok.position.x, blok.position.y)] = blok

    diamond3_list = [items_factory.create("diamond3", block[0], block[1]) for block in diamond3list()]
    for blok in diamond3_list:
        grid[(blok.position.x, blok.position.y)] = blok

    glass_list = [items_factory.create("glass", block[0], block[1]) for block in glasslist()]
    for blok in glass_list:
        grid[(blok.position.x, blok.position.y)] = blok

    cloud_list = [items_factory.create("cloud", block[0], block[1]) for block in cloudlist()]
    for blok in cloud_list:
        grid[(blok.position.x, blok.position.y)] = blok

    clump_list = [items_factory.create("clump", block[0], block[1]) for block in clumplist()]
    for blok in clump_list:
        grid[(blok.position.x, blok.position.y)] = blok
