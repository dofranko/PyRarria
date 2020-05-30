import pygame


# Klasa przechowująca info o animacjach obrazków
class SpriteSheet:
    def __init__(self, filename, cols, rows, frames):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.cols = cols
        self.rows = rows
        self.total = frames
        self.rect = self.sheet.get_rect()
        w = self.cell_width = self.rect.width / cols
        h = self.cell_height = self.rect.height / rows
        hw, hh = self.cell_center = (w/2, h/2)
        self.cells = list([(index % cols * w, index // cols * h, w, h) for index in range(self.total)])
        self.shift = [(0, 0), (-hw, 0), (-w, 0), (0, -hh), (-hw, -hh), (-w, -hh), (0, -h), (-hw, -h), (-w, -h)]