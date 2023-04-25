from cmu_graphics import *
from PIL import Image
from player import *
from item import *
from portal import *

from perlin import *
from platforms import *
import random

class Level:
    def __init__(self, tileMap, index, itemCount, icon):
        self.x, self.y = 0, 0
        self.tileMap = tileMap
        self.index = index
        self.tileSize = 60
        self.width = len(self.tileMap[0]) * self.tileSize
        self.sprite = CMUImage(Image.open(icon))
        self.itemCount = itemCount

        # portal constants
        self.nextWorld = index + 1

        # item constants
        self.items = []
        if self.index == 0:
            start = 1
            crystal1 = app.itemIcons[0]
            crystal2 = app.itemIcons[1]
            crystal3 = app.itemIcons[2]
            crystal4 = app.itemIcons[3]
            crystal5 = app.itemIcons[4]
            self.items = [Item(1200, 960, 1, crystal1), Item(100, 600, 2, crystal2),
                          Item(1400, 240, 3, crystal3), Item(2750, 600, 4, crystal4), Item(3000, 300, 5, crystal5)]
            self.portal = Portal(3600, 240, self.nextWorld)
        elif self.index == 1:
            start = 6
            crystal6 = app.itemIcons[5]
            crystal7 = app.itemIcons[6]
            crystal8 = app.itemIcons[7]
            self.items = [Item(500, 1020, 6, crystal6), Item(1500, 1020, 7, crystal7), Item(3000, 1020, 8, crystal8)]
            self.portal = Portal(3600, 1020, self.nextWorld)
        elif self.index == 2:
            start = 9
            crystal9 = app.itemIcons[8]
            crystal10 = app.itemIcons[9]
            crystal11 = app.itemIcons[10]
            crystal12 = app.itemIcons[11]
            self.items = [Item(750, 1020, 9, crystal9), Item(1000, 1020, 10, crystal10),
                           Item(2000, 1020, 11, crystal11), Item(2750, 1020, 12, crystal12)]
            self.portal = Portal(3600, 1020, self.nextWorld)
        self.totalItems = start + self.itemCount

    def draw(self, app):
        drawImage(self.sprite, self.x, self.y)
        # rows, cols = len(self.tileMap), len(self.tileMap[0])
        # for row in range(rows):
        #     for col in range(cols):
        #         xVal = self.x + self.tileSize*col
        #         yVal = self.y + self.tileSize*row

        #         # draw tiles
        #         if self.tileMap[row][col] == 1:
        #             drawRect(xVal, yVal, self.tileSize, self.tileSize, fill='red')
    
    def __repr__(self):
        return f'Level {self.index}'