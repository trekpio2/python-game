import pygame as pg
from settings import screenWidth

class Bullet(pg.sprite.Sprite):
    def __init__(self, position, speed, direction):
        super().__init__()
        self.image = pg.Surface((20, 4))
        self.image.fill('Red')
        self.rect = self.image.get_rect(center = position)
        self.speed = speed
        self.direction = direction

        self.hitSound = pg.mixer.Sound('audio/hit.mp3')
        self.hitSound.set_volume(0.3)

    def destroy(self):
        """
        Funkcja sprawdzajaca czy pocisk wyszedl za mape - jesli tak niszczy go
        """
        if self.rect.y <= -50 or self.rect.y >= screenWidth + 50:
            self.kill()

    def update(self,):
        """
        Funkcja aktualizujaca pocisk - przesuwajaca pocisk w kierunku ustawionym w momencie stworzenia
        """
        if self.direction == True:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        self.destroy()