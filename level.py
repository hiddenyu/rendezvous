from cmu_graphics import *
from PIL import Image
import random

class Level:
    def __init__(self, tileMap):
        self.x, self.y = 0, 0
        self.tileMap = tileMap
        self.tileSize = app.width / len(self.tileMap[0])
        self.sprites = None

        # platform constants
        self.xLo = 0
        self.xHigh = 3
        self.yLo = 14
        self.yHigh = len(self.tileMap) - 2
        self.platLength = random.randint(2, 4)
        self.platCount = 6
        self.dx, self.dy = 5, 2

        self.generatePlatform(self.tileMap, self.xLo, self.xHigh, 
                              self.yLo, self.yHigh, self.platLength)
        for i in range(self.platCount):
            self.nextPlatform(self.tileMap, self.xLo, self.yLo, 
                              self.dx, self.dy)

    def generatePlatform(self, tileMap, xLo, xHigh, yLo, yHigh, length):
        overlap = True
        x, y = self.randomNum(self.tileMap, xLo, xHigh, yLo, yHigh, length)
        while overlap:
            for i in range(length):
                if tileMap[y][x + i] == 1:
                    x, y = self.randomNum(self.tileMap, xLo, xHigh, yLo, yHigh, length)
                    overlap = True
                else:
                    tileMap[y][x + i] = 1
                    overlap = False
        print(x, y, length)
        self.xLo, self.yLo, self.platLength = x, y, length
    
    def nextPlatform(self, tileMap, x, y, dx, dy):
        length = random.randint(2, 5)
        self.generatePlatform(tileMap, x, x+dx, y, y+dy, length)

    def randomNum(self, tileMap, xLo, xHigh, yLo, yHigh, length):
        x = random.randint(max(xLo, 0), min(xHigh, len(tileMap[0]) - length))
        y = random.randint(max(yLo, 0), min(yHigh, len(tileMap) - 1))
        return x, y

    def draw(self):
        rows, cols = len(self.tileMap), len(self.tileMap[0])
        for row in range(rows):
            for col in range(cols):
                if self.tileMap[row][col] != 0:
                    drawRect(self.x + self.tileSize*col, 
                             self.y + self.tileSize*row, self.tileSize, 
                             self.tileSize, fill='red')