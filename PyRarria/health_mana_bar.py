import pygame
from settings import *


class Health_bar():
    def __init__(self, game):
        self.game = game
        self.hp = 5 * 195  # zaczynamy z pełnym życiem
        self.max_health = 20 * 195  # 5 serduszek, każde ma 195 punktów, alpha w zakresie (60,255)
        self.image = pygame.image.load("resources/images/heart.png").convert()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.image.set_colorkey((0, 0, 0))  # sprawia, że otoczenie ikony jest przezroczyste (super)
        font = pygame.font.SysFont("dejavusans", 15, 0, 10)
        self.health = font.render("Life", True, WHITE)

    def add_heart(self):
        if self.max_health != 20 * 195:  # maksymalnie 20 serduszek może być
            self.max_health += 195  # gdy zgarniemy jakiś bonusik zwiększamy liczbę serc i dodajemy do życia punkty
            self.increase_health(195)

    def remove_heart(self):
        if self.max_health != 5 * 195:  # minimalnie 5 serduszek może być
            self.max_health -= 195  # gdy zgarniemy jakąś pułapkę zmniejszamy liczbę serc i odejmujemy od życia punkty
            self.decrease_health(195)

    def increase_health(self, recovery_value):
        if self.hp == self.max_health:                      # gdy mamy pełne życie, nie zwiększamy, potki się nie marnują
            return False
        elif self.hp + recovery_value <= self.max_health:   # normalny przpadek zwiększania życia
            self.hp += recovery_value
        else:
            self.hp = self.max_health                       # gdy zwiększamy życie i jednocześnie przekraczamy to ustawiamy wartośc na max (nie przekraczamy)
        return True

    def decrease_health(self, damage_value):
        if self.hp - damage_value <= 0:                     # gdy zejdziemy z życiem do 0 lub niżej koniec gry
            self.game.playing = False
        else:
            self.hp -= damage_value                         # jeśli nie normalnie odejmujemy

    def update(self):
        self.increase_health(1)                            # w ciągu przebiegu gry stopniowo się regenerujemy

    def draw(self):
        self.game.screen.blit(self.health, (WIDTH - 200, 0))
        x = self.hp  # pomocnicze zmienna, aby rodzielić punkty życia na serduszko
        for k in range(int(self.max_health / 195)):  # obliczamy ilość serduszek
            c = 0  # c,d odpowiadają za układ serduszek na ekranie
            d = k % 10
            if k >= 10:
                c = 15
            if x >= 195:
                self.image.set_alpha(255)  # pełne serduszko
                x -= 195  # odejmujemy wartość pełnego serduszka od ogólnej puli życia
            else:
                self.image.set_alpha(60 + x)  # to co pozostało dajemy do kolejnego serduszka
                x = 0  # i zerujemy, aby następne były już ,,puste''
            self.game.screen.blit(self.image, (WIDTH - 200 + 15 * d, 15 + c))


class Mana_bar():
    def __init__(self, game):
        self.game = game
        self.mana = 5 * 195  # zaczynamy z pełną maną
        self.max_mana = 20 * 195  # 5 gwiazdek, każda ma 195 punktów, alpha w zakresie (60,255)
        self.image = pygame.image.load("resources/images/mana.png").convert()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.image.set_colorkey((0, 0, 0))  # sprawia, że otoczenie ikony jest przezroczyste (super)
        font = pygame.font.SysFont("dejavusans", 15, 0, 10)
        self.star = font.render("Mana", True, WHITE)

    def add_star(self):
        if self.max_mana != 20 * 195:  # maksymalnie 20 gwiazdek może być
            self.max_mana += 195  # gdy zgarniemy jakiś bonusik zwiększamy liczbę gwiazdek i dodajemy do many punkty
            self.increase_mana(195)

    def remove_star(self):
        if self.max_mana != 5 * 195:  # minimalnie 5 gwiazdek może być
            self.max_mana -= 195  # gdy zgarniemy jakąś pułapkę zmniejszamy liczbę gwiazdek i odejmujemy od many punkty
            self.decrease_mana(195)

    def increase_mana(self, recovery_value):
        if self.mana == self.max_mana:                      # gdy pełna mana, nie zwiększamy
            return False
        elif self.mana + recovery_value <= self.max_mana:   # normalny przypadek zwiększania
            self.mana += recovery_value
        else:
            self.mana = self.max_mana                       # gdy przekroczymy wartość to ustalamy naszą mane na max
        return True

    def decrease_mana(self, power_value):
        if self.mana - power_value < 0:  # nie możemy użyć mocy bez wystarczająco dużo many
            return False
        else:
            self.mana -= power_value

    def update(self):
        self.increase_mana(1)                   # w ciągu przebiegu gry zwiększamy mane

    def draw(self):
        self.game.screen.blit(self.star, (WIDTH - 40, 0))
        x = self.mana  # pomocnicze zmienna, aby rodzielić punkty many na gwiazdeczkę
        for k in range(int(self.max_mana / 195)):  # obliczamy ilość gwiazdek
            if x >= 195:
                self.image.set_alpha(255)  # pełna gwiazdeczka
                x -= 195  # odejmujemy wartość pełnej gwiazdki od ogólnej puli many
            else:
                self.image.set_alpha(60 + x)  # to co pozostało dajemy do kolej gwiazdeczki
                x = 0  # i zerujemy, aby następne były już ,,puste''
            self.game.screen.blit(self.image, (WIDTH - 20, 15 + 15 * k))
