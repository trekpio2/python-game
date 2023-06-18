import pygame as pg
from csv import reader
from settings import tileSize
from os import walk

def importFolder(path):
	"""
    Funkcja pobierajaca nazwy plikow z danego folderu i zwracajaca ich liste
    """
	surfaceList = []

	for _, __, imageFiles in walk(path):
		for image in imageFiles:
			fullPath = path + '/' + image
			imageSurface = pg.image.load(fullPath).convert_alpha()
			surfaceList.append(imageSurface)

	return surfaceList

def importCsvLayout(path):
	"""
	Funkcja odczytujaca dany plik csv i zwracajaca rozklad elementow
	"""
	terrainMap = []
	
	with open(path) as map:
		level = reader(map, delimiter = ',')
		
		for row in level:
			terrainMap.append(list(row))
	
		return terrainMap

def importCutGraphics(path):
	"""
	Funkcja wyodrebniajaca i tworzaca pojednycze sprite'y z pliku
	"""
	surface = pg.image.load(path).convert_alpha()
	tileNumberX = int(surface.get_size()[0] / tileSize)
	tileNumberY = int(surface.get_size()[1] / tileSize)

	cutTiles = []

	for row in range(tileNumberY):
		for col in range(tileNumberX):
			x = col * tileSize
			y = row * tileSize
			newSurface = pg.Surface((tileSize,tileSize), pg.SRCALPHA)
			newSurface.blit(surface,(0,0),pg.Rect(x,y,tileSize,tileSize))
			cutTiles.append(newSurface)

	return cutTiles
