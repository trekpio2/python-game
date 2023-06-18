import pygame as pg
from tiles import AnimatedTile

class Enemy(AnimatedTile):
    def __init__(self, size, x, y, currentLevel):
        super().__init__(size, x, y, 'graphics/enemies/' +str(currentLevel) + '/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = 4

    def move(self):
        """
        Funkcja przemieszczajaca wrogow
        """
        self.rect.x -= self.speed

    def reverseImage(self):
        """
        Funkcja odwracajaca wrogow na podstawie predkosci
        """
        if self.speed > 0:
            self.image = pg.transform.flip(self.image, True, False)

    def reverse(self):
        """
        Funkcja zmieniajaca znak predkosci - kierunku
        """
        self.speed *= -1

    def update(self, xShift):
        """
        Funkcja sterujaca mapa
        """
        self.rect.x += xShift
        self.animate()
        self.move()
        self.reverseImage()