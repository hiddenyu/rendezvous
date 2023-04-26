from cmu_graphics import *
from PIL import Image
from player import *
from item import *
from perlin import *
from platforms import *
import random

class Level:
    def __init__(self, tileMap, icon):
        self.x, self.y = 0, 0
        self.tileMap = tileMap
        self.tileSize = 60
        self.width = len(self.tileMap[0]) * self.tileSize
        self.sprite = CMUImage(Image.open(icon))

        # item constants
        self.items = []
        crystal1 = app.itemIcons[0]
        crystal2 = app.itemIcons[1]
        crystal3 = app.itemIcons[2]
        crystal4 = app.itemIcons[3]
        crystal5 = app.itemIcons[4]
        crystal6 = app.itemIcons[5]
        crystal7 = app.itemIcons[6]
        crystal8 = app.itemIcons[7]
        crystal9 = app.itemIcons[8]
        crystal10 = app.itemIcons[9]
        crystal11 = app.itemIcons[10]
        crystal12 = app.itemIcons[11]
        self.items = [Item(600, 960, 1, crystal1), Item(1200, 960, 2, crystal2),
                        Item(1500, 900, 3, crystal3), Item(2200, 780, 4, crystal4), Item(150, 600, 5, crystal5), 
                        Item(1440, 240, 6, crystal6), Item(2160, 480, 7, crystal7), Item(2760, 600, 8, crystal8),
                        Item(3360, 660, 9, crystal9), Item(3020, 300, 10, crystal10),
                        Item(3660, 720, 11, crystal11), Item(3690, 240, 12, crystal12)]

    def draw(self, app):
        # drawImage(self.sprite, self.x, self.y)
        rows, cols = len(self.tileMap), len(self.tileMap[0])
        for row in range(rows):
            for col in range(cols):
                xVal = self.x + self.tileSize*col
                yVal = self.y + self.tileSize*row

                # draw tiles
                if self.tileMap[row][col] == 1:
                    drawRect(xVal, yVal, self.tileSize, self.tileSize, fill='red')
    
    def __repr__(self):
        return f'Level {self.index}'