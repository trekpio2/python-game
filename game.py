import pygame as pg
from sys import exit
from settings import *
from level import Level
from world import World
from ui import UI
from menu import gameMenu

class Game:
    def __init__(self, savedUnlockedLevels ,savedHP, savedPoints):
        self.maxHP = 100
        self.currentHP = savedHP
        self.points = savedPoints

        self.levelsNumber = savedUnlockedLevels
        self.world = World(1, self.levelsNumber, screen, self.createLevel)
        self.status = 'world'
        
        music = pg.mixer.Sound('audio/music.mp3')
        music.set_volume(0.1)
        music.play(loops = -1)
        
        self.ui = UI(screen)

    def createLevel(self, currentLevel):
        """
        Funkcja tworzaca mape i ustawiajaca status gry w mapie
        """
        self.level = Level(currentLevel, screen, self.createWorld, self.changePoints, self.changeHP, self.save)
        self.status = 'level'

    def createWorld(self, currentLevel, newLevelsNumber):
        """
        Funkcja tworzaca swiat i ustawiajaca status gry w swiecie
        """
        if newLevelsNumber > self.levelsNumber:
            self.levelsNumber = newLevelsNumber
        self.world = World(currentLevel, self.levelsNumber, screen, self.createLevel)
        self.status ='world'

    def changePoints(self, amount):
        """
        Funkcja zmieniajaca ilosc punktow
        """
        self.points += amount

    def changeHP(self, amount):
        """
        Funkcja zmieniajaca ilosc zycia
        """
        self.currentHP += amount

    def checkGameOver(self):
        """
        Funkcja sprawdzajaca czy gracz zginal - jesli tak powrot do swiata i restartujaca statystyki gracza
        """
        if self.currentHP <= 0:
            self.currentHP = 100
            self.points = 0
            self.levelsNumber = 1
            
            self.save()
            
            self.world = World(1, self.levelsNumber, screen, self.createLevel)
            self.status ='world'
            
    def run(self):
        """
        Funkcja sterujaca gra
        """
        if self.status == 'world':
            self.world.run()
            self.ui.showPoints(self.points, 'world')
        else:
            self.level.run()
            self.ui.showHP(self.maxHP, self.currentHP)
            self.ui.showPoints(self.points, 'level')
            self.checkGameOver()

    def save(self):
        """
        Funkcja zapisujaca stan gry w pliku
        """
        dataToSave = str(self.levelsNumber) + '\n' + str(self.currentHP) + '\n' + str(self.points)
        saveFile = open('saves/save.txt', 'w')
        saveFile.write(dataToSave)

        saveFile.close()

started = gameMenu.started
saveData = gameMenu.saveData
del gameMenu

if started == True:
    pg.init()
    screen = pg.display.set_mode((screenWidth, screenHeight))
    pg.display.set_caption('Super Gra')

    clock = pg.time.Clock()
    game = Game(saveData[0], saveData[1], saveData[2])

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            
        screen.fill('lightblue')
        game.run()

        pg.display.update()
        clock.tick(60)

    del game