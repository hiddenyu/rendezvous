from cmu_graphics import *
from PIL import Image
from perlin import *
from level import *
from player import *
import random

class RandomLevel:
    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = app.width, app.height
        self.tileSize = 60

        self.cameraLeft = 600
        self.cameraRight = self.width - self.cameraLeft

        # platform constants
        self.platformList = []

        self.floorPlat = Platform(0, 17, self.width//self.tileSize, 60)

        self.seed = random.randint(0, 1000)
        self.xVals = 256
        self.threshold = 0.3
        self.noise = randomNoise(self.seed, self.xVals)
        self.perlinNoise = []

        for y in range(self.height): # for each y value
            self.perlinNoise.append(0) # make array of just 0s

        for y in range(self.height): # create noise for each y value
            self.perlinNoise[y] = eval(self.noise, self.xVals, y)

        self.newPlats()

        for platform in self.platformList: # remove out of range plats
            if platform.y < 0:
                self.platformList.remove(platform)

    def newPlats(self):
        for y in range(self.height // self.tileSize):
            if self.perlinNoise[y] > self.threshold:
                platLength = random.randint(3, 5)
                x = random.randrange(0, self.width // self.tileSize, platLength)
                self.platformList.append(Platform(x, y - 1, platLength, self.tileSize))

    def generate(self):
        for platform in self.platformList:
            if platform.x + platform.width < 0:
                # remove if too far left
                self.platformList.remove(platform)
                
                # add a new one
                platLength = random.randint(3, 5)
                y = random.randint(0, self.height // self.tileSize)
                if self.perlinNoise[y % self.height // self.tileSize] > self.threshold:
                    newPlat = Platform(self.width//self.tileSize, y - 1, platLength, self.tileSize)
                    self.platformList.append(newPlat)

    def draw(self):
        self.floorPlat.draw()
        for platform in self.platformList:
            platform.draw()
