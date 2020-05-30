import pygame
from settings import *


class HealthBar:
    def __init__(self, game):
        self.game = game
        self.current_max_health = MIN_HEALTH                                     # aktualne maksymalne zdrowie
        self.hp = MIN_HEALTH                                                     # zaczynamy z 5 serduszkami
        self.image = pygame.image.load("resources/images/heart.png").convert()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.image.set_colorkey((0, 0, 0))                                       # sprawia, że otoczenie ikony jest przezroczyste (super)
        font = pygame.font.SysFont("dejavusans", 15, 0, 10)
        self.health = font.render("Health", True, WHITE)

    def add_heart(self):
        if self.current_max_health < MAX_HEALTH:
            self.current_max_health += HEART_VALUE
        return self.increase_health(HEART_VALUE)

    def remove_heart(self):
        if self.current_max_health > MIN_HEALTH:              # minimalnie 5 serduszek może być
            self.current_max_health -= HEART_VALUE            # gdy zgarniemy jakąś pułapkę zmniejszamy liczbę serc i odejmujemy od życia punkty
        self.decrease_health(HEART_VALUE)

    def increase_health(self, recovery_value):
        if self.hp == self.current_max_health:                      # gdy mamy pełne życie, nie zwiększamy, potki się nie marnują
            return False
        elif self.hp + recovery_value <= self.current_max_health:   # normalny przpadek zwiększania życia
            self.hp += recovery_value
        else:
            self.hp = self.current_max_health                       # gdy zwiększamy życie i jednocześnie przekraczamy to ustawiamy wartośc na current_max_health (nie przekraczamy)
        return True

    def decrease_health(self, damage_value):
        if self.hp - damage_value <= 0:                     # gdy zejdziemy z życiem do 0 lub niżej koniec gry
            self.game.playing = False
        else:
            self.hp -= damage_value                         # jeśli nie normalnie odejmujemy

    def update(self):
        self.increase_health(HEALTH_RECOVERY_VALUE)         # w ciągu przebiegu gry stopniowo się regenerujemy (tylko do wartości current_max_health)

    def draw(self):
        self.game.screen.blit(self.health, (WIDTH - 200, 0))
        x = self.hp                                       # pomocnicze zmienna, aby rodzielić punkty życia na serduszko
        for k in range(int(self.current_max_health / HEART_VALUE)):    # obliczamy ilość serduszek
            c = 0                                         # c,d odpowiadają za układ serduszek na ekranie
            d = k % 10
            if k >= 10:
                c = 15
            if x >= HEART_VALUE:
                self.image.set_alpha(255)  # pełne serduszko
                x -= HEART_VALUE           # odejmujemy wartość pełnego serduszka od ogólnej puli życia
            else:
                self.image.set_alpha(60 + x)    # to co pozostało dajemy do kolejnego serduszka
                x = 0                           # i zerujemy, aby następne były już ,,puste''
            self.game.screen.blit(self.image, (WIDTH - 200 + 15 * d, 15 + c))


class ManaBar:
    def __init__(self, game):
        self.game = game
        self.current_max_mana = MIN_MANA                    # aktualna maksymalna mana
        self.mana = MIN_MANA                                # zaczynamy z 5 gwiazdeczkami
        self.image = pygame.image.load("resources/images/mana.png").convert()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.image.set_colorkey((0, 0, 0))                   # sprawia, że otoczenie ikony jest przezroczyste (super)
        font = pygame.font.SysFont("dejavusans", 15, 0, 10)
        self.star = font.render("Mana", True, WHITE)

    def add_star(self):
        if self.current_max_mana < MAX_MANA:             # maksymalnie 20 gwiazdek może być
            self.current_max_mana += STAR_VALUE          # gdy zgarniemy jakiś bonusik zwiększamy liczbę gwiazdek i dodajemy do many punkty
        return self.increase_mana(STAR_VALUE)

    def remove_star(self):
        if self.current_max_mana > MIN_MANA:             # minimalnie 5 gwiazdek może być
            self.current_max_mana -= STAR_VALUE                  # gdy zgarniemy jakąś pułapkę zmniejszamy liczbę gwiazdek i odejmujemy od many punkty
        self.decrease_mana(STAR_VALUE)

    def increase_mana(self, recovery_value):
        if self.mana == self.current_max_mana:                      # gdy pełna mana, nie zwiększamy
            return False
        elif self.mana + recovery_value <= self.current_max_mana:   # normalny przypadek zwiększania
            self.mana += recovery_value
        else:
            self.mana = self.current_max_mana                       # gdy przekroczymy wartość to ustalamy naszą mane na current_max_mana
        return True

    def decrease_mana(self, power_value):
        if self.mana - power_value < 0:                             # nie możemy użyć mocy bez wystarczająco dużo many
            return False
        else:
            self.mana -= power_value

    def update(self):
        self.increase_mana(MANA_RECOVERY_VALUE)                     # w ciągu przebiegu gry zwiększamy manę (tylko do wartości current_max_mana)

    def draw(self):
        self.game.screen.blit(self.star, (WIDTH - 40, 0))
        x = self.mana                                  # pomocnicze zmienna, aby rodzielić punkty many na gwiazdeczkę
        for k in range(int(self.current_max_mana / STAR_VALUE)):    # obliczamy ilość gwiazdek
            if x >= STAR_VALUE:
                self.image.set_alpha(255)              # pełna gwiazdeczka
                x -= STAR_VALUE                        # odejmujemy wartość pełnej gwiazdki od ogólnej puli many
            else:
                self.image.set_alpha(60 + x)           # to co pozostało dajemy do kolejnej gwiazdeczki
                x = 0                                  # i zerujemy, aby następne były już ,,puste''
            self.game.screen.blit(self.image, (WIDTH - 20, 15 + 15 * k))