import pygame as pg
from support import importCsvLayout, importCutGraphics
from settings import tileSize, screenWidth, screenHeight
from tiles import Tile, StaticTile, Crate, AnimatedTile
from enemy import Enemy
from player import Player
from levelsInfo import levels

class Level:
    def __init__(self, currentLevel, surface, createWorld, changePoints, changeHP, save):
        self.displaySurface = surface
        self.worldShift = 0

        self.createWorld = createWorld
        self.currentLevel = currentLevel
        levelData = levels[self.currentLevel]
        self.newLevelsNumber = levelData['unlock']

        playerLayout = importCsvLayout(levelData['player'])
        self.player = pg.sprite.GroupSingle()
        self.finish = pg.sprite.GroupSingle()
        
        self.changePoints = changePoints
        self.changeHP = changeHP
        self.save = save
        
        self.setPlayer(playerLayout, changeHP)

        terrainLayout = importCsvLayout(levelData['terrain'])
        self.terrainSprites = self.createTileGroup(terrainLayout, 'terrain')
        
        cratesLayout = importCsvLayout(levelData['crates'])
        self.cratesSprites = self.createTileGroup(cratesLayout, 'crates')
        
        bgDecorationsLayout = importCsvLayout(levelData['bgDecorations'])
        self.bgDecorationsSprites = self.createTileGroup(bgDecorationsLayout, 'bgDecorations')
  
        enemiesLayout = importCsvLayout(levelData['enemies'])
        self.enemiesSprites = self.createTileGroup(enemiesLayout, 'enemies')

        mapLimitsLayout = importCsvLayout(levelData['mapLimits'])
        self.mapLimitsSprites = self.createTileGroup(mapLimitsLayout, 'mapLimits')

    def createTileGroup(self, layout, type):
        """
        Funkcja tworzaca dany element swiata 
        """
        spriteGroup = pg.sprite.Group()

        for rowIndex, row in enumerate(layout):
            for colIndex, col in enumerate(row):
                if col != '-1':
                    x = colIndex * tileSize
                    y = rowIndex * tileSize
                    
                    if type == 'terrain':
                        terrainTileList = importCutGraphics('graphics/terrain/terrainTiles1.png')
                        tileSurface = terrainTileList[int(col)]
                        sprite = StaticTile(tileSize, x, y, tileSurface)
                    
                    if type == 'crates':
                        sprite = Crate(tileSize, x, y)

                    if type == 'bgDecorations':
                        decorationsTileList = importCutGraphics('graphics/terrain/Decorations1.png')
                        tileSurface = decorationsTileList[int(col)]
                        sprite = StaticTile(tileSize, x, y, tileSurface)

                    if type == 'enemies':
                        sprite = Enemy(tileSize, x, y, self.currentLevel)

                    if type == 'mapLimits':
                        mapLimitsSurface = pg.Surface((64, 64))
                        sprite = Tile(tileSize, x, y)

                    spriteGroup.add(sprite)

        return spriteGroup

    def setPlayer(self, layout, changeHP):
        """
        Funkcja tworzaca gracza i mete
        """
        for rowIndex, row in enumerate(layout):
            for colIndex, col in enumerate(row):
                x = colIndex * tileSize
                y = rowIndex * tileSize
                
                if col == '0':
                    sprite = Player((x, y), changeHP)
                    self.player.add(sprite)
                if col == '1':
                    crownSurface = pg.image.load('graphics/terrain/crown.png')
                    sprite = StaticTile(tileSize, x, y, crownSurface)
                    self.finish.add(sprite)

    def enemyCollisionReverse(self):
        """
        Funkcja odwracajaca wrogow po dotarciu do kranca
        """
        for enemy in self.enemiesSprites.sprites():
            if pg.sprite.spritecollide(enemy, self.mapLimitsSprites, False):
                enemy.reverse()

    def horizontalMovementCollision(self):
        """
        Funkcja odpowiadajaca za przesuwanie gracza oraz ustalenie czy gracz idzie w prawo czy w lewo i ustawiajaca go na dobrej pozycji wzgledem terenu
        """
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        collidableSprites = self.terrainSprites.sprites() + self.cratesSprites.sprites()

        for sprite in collidableSprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.onLeft = True
                    self.currentX = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.rect.right

        if player.onLeft == True and (player.rect.left < self.currentX or player.direction.x >= 0):
            player.onLeft = False
        if player.onRight == True and (player.rect.right > self.currentX or player.direction.x <= 0):
            player.onRight = False

    def verticalMovementCollision(self):
        """
        Funkcja ustalajaca czy gracz jest w powietrzu, na ziemi, czy dotyka sufitu i ustawiajaca go na dobrej pozycji wzgledem terenu oraz wlaczajaca grawitacje jesli jest w powietrzu
        """
        player = self.player.sprite
        player.addGravity()

        collidableSprites = self.terrainSprites.sprites() + self.cratesSprites.sprites()

        for sprite in collidableSprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True

        if player.onGround == True and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False
        if player.onCeiling == True and player.direction.y > 0:
            player.onCeiling = False

    def scrollX(self):
        """
        Funkcja odpowiadajaca za kamere - w odpowiednim momencie przesuwa wszystko w dana strone
        """
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x

        if playerX < screenWidth / 4 and directionX < 0:
            self.worldShift = 8
            player.speed = 0
        elif playerX > screenWidth - (screenWidth / 4) and directionX > 0:
            self.worldShift = -8
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 8

    def checkFall(self):
        """
        Funkcja sprawdzajaca czy gracz tak - jesli tak odejmuje punky, zapisuje gre i cofa gracza do swiata
        """
        if self.player.sprite.rect.top > screenHeight:
            self.changePoints(-50)
            self.save()
            self.createWorld(self.currentLevel, 0)

    def checkWin(self):
        """
        Funkcja sprawdzajaca czy gracz doszedl do mety - jesli tak odblokowuje kolejna mape, zapisuje gre i cofa gracza do swiata
        """
        if pg.sprite.spritecollide(self.player.sprite, self.finish, False):
            self.changePoints(30)
            self.changeHP(30)
            self.createWorld(self.currentLevel, self.newLevelsNumber)
            self.save()

    def checkEnemyCollisions(self):
        """
        Funkcja sprawdzajaca kolizje gracza z przeciwnikami - jesli wystepuje odejmuje zycie 
        """
        enemyCollisions = pg.sprite.spritecollide(self.player.sprite, self.enemiesSprites, False)
        if enemyCollisions:
            for enemy in enemyCollisions:
                self.player.sprite.getDamage()

    def checkBulletHit(self):
        """
        Funkcja sprawdzajaca kolizje pocisku z terenem - jesli wystepuje usuwa pocisk - i z przeciwnikami - jesli tak dodaje punkty i usuwa wroga
        """
        bulletsSprites = self.player.sprite.bullets.sprites()
        for bulletSprite in bulletsSprites:
            if pg.sprite.spritecollide(bulletSprite, self.terrainSprites, False):
                bulletSprite.kill()
            if pg.sprite.spritecollide(bulletSprite, self.enemiesSprites, True):
                bulletSprite.hitSound.play()
                self.changePoints(10)
                bulletSprite.kill()

    def run(self):
        """
        Funkcja sterujaca mapa
        """
        self.bgDecorationsSprites.update(self.worldShift)
        self.bgDecorationsSprites.draw(self.displaySurface)
      
        self.enemiesSprites.update(self.worldShift)    
        self.mapLimitsSprites.update(self.worldShift)
        self.enemyCollisionReverse()
        self.enemiesSprites.draw(self.displaySurface)

        self.terrainSprites.update(self.worldShift)
        self.terrainSprites.draw(self.displaySurface)
      
        self.player.sprite.bullets.draw(self.displaySurface)
        self.cratesSprites.update(self.worldShift)
        self.cratesSprites.draw(self.displaySurface)

        self.player.update()
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.scrollX()
        self.player.draw(self.displaySurface)
        self.finish.update(self.worldShift)
        self.finish.draw(self.displaySurface)

        self.checkFall()
        self.checkWin()
        
        self.checkBulletHit()
        self.checkEnemyCollisions()
