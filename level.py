from cmu_graphics import *
from PIL import Image

class Level:
    def __init__(self, tileMap):
        self.tileMap = tileMap
        self.tileSize = 60
        self.sprites = None

    def draw(self):
        rows, cols = len(self.tileMap), len(self.tileMap[0])
        for row in range(rows):
            for col in range(cols):
                if self.tileMap[row][col] != 0:
                    drawRect(self.tileSize*col, self.tileSize*row, 
                             self.tileSize, self.tileSize, fill='red')