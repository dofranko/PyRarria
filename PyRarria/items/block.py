import pygame
from settings import *
from items.placeable import *
from math import sqrt
from os import path

vector = pygame.math.Vector2

class Block(Placeable):
    def __init__(self, x, y, info, game, placed=True):
        super().__init__(x, y, info, game, placed)