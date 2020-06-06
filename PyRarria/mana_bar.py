import pygame
from settings import *


class ManaBar:
    """A class representing mana points of player"""

    def __init__(self, game):
        self.game = game
        self.current_max_mana = MIN_MANA  # aktualna maksymalna mana
        self.mana = MIN_MANA  # zaczynamy z 5 gwiazdeczkami
        self.image = pygame.image.load(IMAGES_LIST["mana"]).convert()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.image.set_colorkey((0, 0, 0))  # sprawia, że otoczenie ikony jest przezroczyste (super)
        font = pygame.font.SysFont("dejavusans", 15, 0, 10)
        self.star = font.render("Mana", True, WHITE)

    def add_star(self):
        """Add star to player"""
        if self.current_max_mana < MAX_MANA:  # maksymalnie 20 gwiazdek może być
            # gdy zgarniemy jakiś bonusik zwiększamy liczbę gwiazdek i dodajemy do many punkty
            self.current_max_mana += STAR_VALUE
        return self.increase_mana(STAR_VALUE)

    def remove_star(self):
        """Remove star from player"""
        if self.current_max_mana > MIN_MANA:  # minimalnie 5 gwiazdek może być
            # gdy zgarniemy jakąś pułapkę zmniejszamy liczbę gwiazdek i odejmujemy od many punkty
            self.current_max_mana -= STAR_VALUE
        self.decrease_mana(STAR_VALUE)

    def increase_mana(self, recovery_value):
        """Add mana points to player"""
        if self.mana == self.current_max_mana:  # gdy pełna mana, nie zwiększamy
            return False
        elif self.mana + recovery_value <= self.current_max_mana:  # normalny przypadek zwiększania
            self.mana += recovery_value
        else:
            self.mana = self.current_max_mana  # gdy przekroczymy wartość to ustalamy naszą mane na current_max_mana
        return True

    def decrease_mana(self, power_value):
        """Decrease mana points from player"""
        if self.mana - power_value < 0:  # nie możemy użyć mocy bez wystarczająco dużo many
            return False
        else:
            if power_value > 0:
                self.mana -= power_value
            return True

    def update(self):
        """Regen slowly mana points"""
        # w ciągu przebiegu gry zwiększamy manę (tylko do wartości current_max_mana)
        self.increase_mana(MANA_RECOVERY_VALUE)

    def draw(self):
        """Draw stars"""
        self.game.screen.blit(self.star, (WIDTH - 40, 0))
        x = self.mana  # pomocnicze zmienna, aby rodzielić punkty many na gwiazdeczkę
        for k in range(int(self.current_max_mana / STAR_VALUE)):  # obliczamy ilość gwiazdek
            if x >= STAR_VALUE:
                self.image.set_alpha(255)  # pełna gwiazdeczka
                x -= STAR_VALUE  # odejmujemy wartość pełnej gwiazdki od ogólnej puli many
            else:
                self.image.set_alpha(60 + x)  # to co pozostało dajemy do kolejnej gwiazdeczki
                x = 0  # i zerujemy, aby następne były już ,,puste''
            self.game.screen.blit(self.image, (WIDTH - 20, 15 + 15 * k))
