import pygame as pg
from levelsInfo import levels

class Node(pg.sprite.Sprite):
    def __init__(self, position, status, iconSpeed, graphic):
        super().__init__()
        self.image = pg.image.load(graphic).convert_alpha()
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'

        self.rect = self.image.get_rect(center = position)

        self.detectionZone = pg.Rect(self.rect.centerx - (iconSpeed / 2), self.rect.centery - (iconSpeed / 2), iconSpeed, iconSpeed)

    def update(self):
        """
        Funkcja sprawdzajaca czy wezel jest niedostepny - jesli tak zaczernia obrazek
        """
        if self.status == 'locked':
            blackedSurface = self.image.copy()
            blackedSurface.fill('Black', None, pg.BLEND_RGBA_MULT)
            self.image.blit(blackedSurface, (0, 0))

class Icon(pg.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pg.image.load('graphics/world/icon.png').convert_alpha()
        self.rect = self.image.get_rect(center = position)

    def update(self):
        """
        Funkcja aktualizujaca pozycje ikony
        """

        self.rect.center = self.position

class World:
    def __init__(self, startingLevel, levelsNumber, surface, createLevel):
        self.displaySurface = surface
        self.levelsNumber = levelsNumber
        self.currentLevel = startingLevel
        self.createLevel = createLevel

        self.moving = False
        self.moveDirection = pg.math.Vector2(0, 0)
        self.speed = 8

        self.setNodes()
        self.setIcon()

    def setNodes(self):
        """
        Funkcja ustawiajaca wezly z poszczegolnymi mapami w danym miejscu na ekranie
        """

        self.nodes = pg.sprite.Group()

        for index, nodeData in enumerate(levels.values()):
            if index <= self.levelsNumber:
                nodeSprite = Node(nodeData['nodePosition'], 'available', self.speed, nodeData['nodeGraphic'])
            else:
                nodeSprite = Node(nodeData['nodePosition'], 'locked', self.speed, nodeData['nodeGraphic'])
            self.nodes.add(nodeSprite)

    def drawPaths(self):
        """
        Funkcja rysujaca sciezki z poprzedniej do nastepnej mapy
        """
        points = [node['nodePosition'] for index, node in enumerate(levels.values()) if index <= self.levelsNumber]
        pg.draw.lines(self.displaySurface, 'Red', False, points , 6)

    def setIcon(self):
        """
        Funkcja tworzaca ikone odpowiadajaca za wybor mapy
        """
        self.icon = pg.sprite.GroupSingle()
        iconSprite = Icon(self.nodes.sprites()[self.currentLevel].rect.center)
        self.icon.add(iconSprite)

    def input(self):
        """
        Funkcja odpowiadajaca za poruszanie sie miedzy mapami
        """
        keys = pg.key.get_pressed()
        
        if self.moving == False:
            if keys[pg.K_RIGHT] and self.currentLevel < self.levelsNumber:
                self.moveDirection = self.getMovementData('next')
                self.currentLevel += 1
                self.moving = True
            elif keys[pg.K_LEFT] and self.currentLevel > 0:
                self.moveDirection = self.getMovementData('previous')
                self.currentLevel -= 1
                self.moving = True
            elif keys[pg.K_SPACE]:
                self.createLevel(self.currentLevel)

    def getMovementData(self, target):
        """
        Funkcja odpowiadajaca za ustalenie ruchu ikony na podstawie wybranego kierunku
        """
        start = pg.math.Vector2(self.nodes.sprites()[self.currentLevel].rect.center)
        
        if target == 'next':
            end = pg.math.Vector2(self.nodes.sprites()[self.currentLevel + 1].rect.center)
        else:
            end = pg.math.Vector2(self.nodes.sprites()[self.currentLevel - 1].rect.center)
        
        return (end - start).normalize()

    def updateIconPosition(self):
        """
        Funkcja zatrzymujaca ikone po dotarciu do docelowego wezla i sterujaca szybkoscia poruszania sie ikony pomiedzy wezlami
        """
        if self.moving == True and self.moveDirection:
            self.icon.sprite.position += self.moveDirection * self.speed
            targetNode = self.nodes.sprites()[self.currentLevel]
           
            if targetNode.detectionZone.collidepoint(self.icon.sprite.position):
                self.moving = False
                self.moveDirection = pg.math.Vector2(0, 0)

    def run(self):
        """
        Funkcja sterujaca swiatem
        """
        self.input()
        self.updateIconPosition()
        self.icon.update()
        self.nodes.update()

        self.drawPaths()
        self.nodes.draw(self.displaySurface)
        self.icon.draw(self.displaySurface)