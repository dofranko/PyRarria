import pygame
from settings import *


class HealthBar:
    """A class representing health points of player"""

    def __init__(self, game):
        self.game = game
        self.current_max_health = MIN_HEALTH  # aktualne maksymalne zdrowie
        self.hp = MIN_HEALTH  # zaczynamy z 5 serduszkami
        self.image = pygame.image.load(IMAGES_LIST["heart"]).convert()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.image.set_colorkey((0, 0, 0))  # sprawia, że otoczenie ikony jest przezroczyste (super)
        font = pygame.font.SysFont("dejavusans", 15, 0, 10)
        self.health = font.render("Health", True, WHITE)

    def add_heart(self):
        """Adding more hearts to player"""
        if self.current_max_health < MAX_HEALTH:
            self.current_max_health += HEART_VALUE
        return self.increase_health(HEART_VALUE)

    def remove_heart(self):
        """Removing hearts from player"""
        if self.current_max_health > MIN_HEALTH:  # minimalnie 5 serduszek może być
            # gdy zgarniemy jakąś pułapkę zmniejszamy liczbę serc i odejmujemy od życia punkty
            self.current_max_health -= HEART_VALUE
        self.decrease_health(HEART_VALUE)

    def increase_health(self, recovery_value):
        """Incrase value of health points"""
        if self.hp == self.current_max_health:  # gdy mamy pełne życie, nie zwiększamy, potki się nie marnują
            return False
        elif self.hp + recovery_value <= self.current_max_health:  # normalny przpadek zwiększania życia
            self.hp += recovery_value
        else:
            # gdy zwiększamy życie i jednocześnie przekraczamy to ustawiamy wartośc na current_max_health
            self.hp = self.current_max_health
        return True

    def decrease_health(self, damage_value):
        """Decrease value of health points"""
        if self.hp - damage_value <= 0:  # gdy zejdziemy z życiem do 0 lub niżej koniec gry
            self.game.playing = False
        else:
            self.hp -= damage_value  # jeśli nie normalnie odejmujemy

    def update(self):
        """Slowly regenering health points"""
        # w ciągu przebiegu gry stopniowo się regenerujemy (tylko do wartości current_max_health)
        self.increase_health(HEALTH_RECOVERY_VALUE)

    def draw(self):
        """Drawing hearts (visible and shadowed ones)"""
        self.game.screen.blit(self.health, (WIDTH - 200, 0))
        x = self.hp  # pomocnicze zmienna, aby rodzielić punkty życia na serduszko
        for k in range(int(self.current_max_health / HEART_VALUE)):  # obliczamy ilość serduszek
            c = 0  # c,d odpowiadają za układ serduszek na ekranie
            d = k % 10
            if k >= 10:
                c = 15
            if x >= HEART_VALUE:
                self.image.set_alpha(255)  # pełne serduszko
                x -= HEART_VALUE  # odejmujemy wartość pełnego serduszka od ogólnej puli życia
            else:
                self.image.set_alpha(60 + x)  # to co pozostało dajemy do kolejnego serduszka
                x = 0  # i zerujemy, aby następne były już ,,puste''
            self.game.screen.blit(self.image, (WIDTH - 200 + 15 * d, 15 + c))
