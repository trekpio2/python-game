import pygame as pg
from support import importFolder
from math import sin
from bullet import Bullet

class Player(pg.sprite.Sprite):
    def __init__(self, position, changeHP):
        super().__init__()
        self.importCharacterAssets()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(topleft = position)
        
        self.direction = pg.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jumpSpeed = -16

        self.status = 'idle'
        self.goingRight = True
        self.onGround = False
        self.onCeiling = False
        self.onLeft = False
        self.onRight = False

        self.changeHP = changeHP
        self.invincibility = False
        self.invincibilityDuration = 600
        self.hurtTime = 0

        self.ready = True
        self.shootTime = 0
        self.shootCooldown = 600

        self.bullets = pg.sprite.Group()
        self.shootSound = pg.mixer.Sound('audio/shoot.mp3')
        self.shootSound.set_volume(0.5)

    def importCharacterAssets(self):
        """
        Funkcja importujaca pliki z animacjami do odpowienich im kluczy ze slownika
        """
        characterPath = "graphics\character/Blue/"
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall': [], 'death':[]}

        for animation in self.animations.keys():
            fullPath = characterPath + animation
            self.animations[animation] = importFolder(fullPath)
        
    def animate(self):
        """
        Funkcja odpowiadajaca za animacje gracza
        """
        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0
            
        image = animation[int(self.frameIndex)]
        if self.goingRight == True:
            self.image = image
        else:
            flippedImage = pg.transform.flip(image, True, False)
            self.image = flippedImage

        if self.invincibility == True:
            alpha = self.waveValue()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        if self.onGround == True and self.onRight == True:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.onGround == True and self.onLeft == True:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.onGround == True:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.onCeiling == True and self.onRight == True:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.onCeiling == True and self.onLeft == True:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.onCeiling == True:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def getInput(self):
        """
        Funkcja sterujaca graczem na podstawie wcisnietych przyciskow
        """
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT]:
            self.direction.x = 1
            self.goingRight = True
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
            self.goingRight = False
        else:
            self.direction.x = 0
        
        if keys[pg.K_UP] and self.onGround == True:
            self.jump()

        if keys[pg.K_SPACE] and self.ready == True:
            self.shoot()
            self.ready = False
            self.shootTime = pg.time.get_ticks()

    def getStatus(self):
        """
        Funkcja ustalajaca status ruchu gracza
        """
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def addGravity(self):
        """
        Funkcja odpowiadajaca za grawitacje - przesuwa w dol w oparciu o ustalona wartosc
        """
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        """
        Funkcja przesuwajaca w gore o ustalona wartosc skoku
        """        
        self.direction.y = self.jumpSpeed

    def getDamage(self):
        """
        Funkcja odpowiadajaca za przyjecie obrazen od wrogow
        """
        if self.invincibility == False:
            self.changeHP(-10)
            self.invincibility = True
            self.hurtTime = pg.time.get_ticks()

    def invincibilityTimer(self):
        """
        Funkcja przelaczajaca niesmiertelnosc po otrzymaniu obrazen od wroga
        """
        if self.invincibility == True:
            currentTime = pg.time.get_ticks()
            if currentTime - self.hurtTime >= self.invincibilityDuration:
                self.invincibility = False

    def waveValue(self):
        """
        Funkcja zwracajaca wartosc przezroczystosci podczas niesmiertelnosci wzgledem czasu
        """
        value = sin(pg.time.get_ticks())
        
        if value >= 0:
            return 255
        else:
            return 0

    def recharge(self):
        """
        Funkcja odpowiadajaca za przeladowanie
        """
        if self.ready == False:
            currentTime = pg.time.get_ticks()
            if currentTime - self.shootTime >= self.shootCooldown:
                self.ready = True

    def shoot(self):
        """
        Funkcja odpowiadajaca za strzelanie - tworzy pocisk w danym kierunku i odtwarza dzwiek strzalu
        """
        self.bullets.add(Bullet(self.rect.center, self.speed, self.goingRight))
        self.shootSound.play()

    def update(self):
        """
        Funkcja aktualizujaca gracza i pocisk
        """
        self.getInput()
        self.getStatus()
        self.animate()
        self.recharge()

        for bullet in self.bullets.sprites():
            bullet.update()
        self.invincibilityTimer()