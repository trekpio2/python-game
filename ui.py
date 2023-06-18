import pygame as pg

class UI:
    def __init__(self, surface):
        self.displaySurface = surface

        self.HPBar = pg.image.load('graphics/ui/HPBar.png').convert_alpha()
        self.HPBarTopLeft = (71, 24)
        self.barMaxWidth = 194
        self.barHeight = 36

        self.font = pg.font.SysFont('Comic Sans MS', 36)

    def showHP(self, maxHP, currentHP):
        """
        Funkcja pokazujaca pasek zycia
        """
        self.displaySurface.blit(self.HPBar, (20, 10))
        currentHealthPart = currentHP / maxHP
        currentBarWidth = self.barMaxWidth * currentHealthPart
        HPBarRect = pg.Rect( self.HPBarTopLeft, (currentBarWidth, self.barHeight) )
        pg.draw.rect(self.displaySurface, '#f02727', HPBarRect)

    def showPoints(self, amount, place):
        """
        Funkcja pokazujaca punky w pozycji zaleznej od obecnosci w mapie lub w swiecie
        """
        position = (295, 42)
        if place == 'world':
           position = (24, 24)

        pointSurface = self.font.render('POINTS: ' + str(amount), False, 'Black')
        pointRect = pointSurface.get_rect(midleft = position)
        self.displaySurface.blit(pointSurface, pointRect)