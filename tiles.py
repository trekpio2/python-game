import pygame as pg
from support import importFolder

class Tile(pg.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, xShift):
        """
        Funkcja przesuwajaca kafelki o dane przesuniecie
        """
        self.rect.x += xShift

class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class Crate(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pg.image.load('graphics/terrain/crate.png').convert_alpha())
      
        offsetY = y + size
        self.rect = self.image.get_rect(bottomleft = (x, offsetY))

class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = importFolder(path)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]

    def animate(self):
        """
        Funkcja odpowiadajaca za animacje
        """
        self.frameIndex += 0.15
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]

    def update(self, xShift):
        """
        Funkcja aktualizujaca animacje i przesuniecie
        """
        self.animate()
        self.rect.x += xShift

