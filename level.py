from cmu_graphics import *
from PIL import Image

class Level:
    delta = 30

    def __init__(self, tileMap):
        self.x, self.y = 0, 0
        self.tileMap = tileMap
        self.tileSize = app.width / len(self.tileMap[0])
        self.sprites = None

    def draw(self):
        rows, cols = len(self.tileMap), len(self.tileMap[0])
        for row in range(rows):
            for col in range(cols):
                if self.tileMap[row][col] != 0:
                    drawRect(self.x + self.tileSize*col, 
                             self.y + self.tileSize*row, self.tileSize, 
                             self.tileSize, fill='red')
    
    def scroll(self, scrollVel):
        self.x += scrollVel / Level.delta