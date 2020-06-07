import random

platformy = []
powierzchnia = []


def remove(x, y):
    usun = (x, y, 50, 50)
    if usun in platformy:
        platformy.remove(usun)


def generuj():

    # generator powierzchni
    w = 0
    W = 1000
    H = 1000
    for i in range(100):
        x = random.randint(
            0, 99
        )  # generator posiada "współczynnik załamania" ustawiony na 75%, jest to szansa na to, że zmieni się monotoniczność generwanego terenu (jeśli postawi klocek wyżej większa szansa będzie na to, że następny klocek też będzie wyżej)
        # zapobiega to generowniu losowego terenu, któy będzie wyglądał bardzo chaotycznie
        W += 50
        if w == 0:  # współczynnik ustawiony na 75% utrzymania płaskiego terenu
            if (x >= 76) and (x <= 87):
                H += 50
                w = 1
            if (x >= 88) and (x <= 99):
                H -= 50
                w = 2
        elif w == 1:  # współczynnik ustawiony na 75% wznoszenia terenu
            H += 50
            if H > 1000:
                H = 1000
            if (x >= 76) and (x <= 87):
                w = 0
            if (x >= 88) and (x <= 99):
                H -= 50
                w = 2
        else:  # współczynnik ustawiony na 75% opadania terenu
            H -= 50
            if H < 200:
                H = 200
            if (x >= 76) and (x <= 87):
                w = 0
            if (x >= 88) and (x <= 99):
                H += 50
                w = 1
        platformy.append((W, H, 50, 50))
        powierzchnia.append([W, H])
        for j in range(50):
            platformy.append((W, H + 50 * j, 50, 50))
        platformy.append((380, -500, 10, 10000))

    # GENERATOR JASKIŃ

    ilosc_jaskin = random.randint(5, 10)  # ile jaskiń
    for i in range(ilosc_jaskin):
        koordy_jaskin = powierzchnia[random.randint(0, len(powierzchnia) - 1)]  # - współrzędne jaskini
        x = koordy_jaskin[0]
        y = koordy_jaskin[1]
        remove(x, y)  # wejscie do jaskini tworzymy przes usunięcie kwadratu 3x3
        remove(x + 50, y)
        remove(x - 50, y)
        remove(x, y + 50)
        remove(x, y - 50)

        glebokosc_jaskin = random.randint(5, 30)  # głębokość jaskini

        for j in range(glebokosc_jaskin):
            kierunek_jaskin = random.randint(0, 4)
            szerokosc = random.randint(1, 15)  # zwraca losowych sąsiadów danego klocka, wszystkie możliwe kombinacje
            if kierunek_jaskin < 2:  # następny blok jest usunięty z dołu
                y = y + 50
                remove(x, y)
            elif kierunek_jaskin == 3:  # następny blok jest usunięty z prawej
                x = x + 50
                remove(x, y)
            elif kierunek_jaskin == 4:  # następny blok jest usunięty z lewej
                x = x - 50
                remove(x, y)
            if szerokosc in (1, 5, 7, 10, 12, 13, 14, 15):
                remove(x, y + 50)  # usuwa klocek nad
            if szerokosc in (2, 5, 8, 9, 11, 12, 14, 15):
                remove(x, y - 50)  # usuwa klocek pod
            if szerokosc in (3, 6, 8, 10, 11, 12, 13, 15):
                remove(x + 50, y)  # usuwa klocek po prawej
            if szerokosc in (4, 6, 7, 9, 11, 13, 14, 15):
                remove(x - 50, y)  # usuwa klocek po lewej

    return platformy

