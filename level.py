from cmu_graphics import *
from PIL import Image
from player import *
from perlin import *
from platforms import *
import random

class Level:
    def __init__(self, tileMap, index):
        self.x, self.y = 0, 0
        self.tileMap = tileMap
        self.index = index
        self.tileSize = app.width / len(self.tileMap[0])
        self.sprites = None
        self.platformList = []

        # camera constants
        self.cameraRight = 1600
        self.cameraLeft = 320

        # platform constants
        self.seed = random.randint(0, 1000)
        self.xVals = 256
        self.threshold = 0.3
        self.startingThreshold = 17
        self.noise = randomNoise(self.seed, self.xVals)
        self.perlinNoise = []

        # for y in range(len(self.tileMap)): # for each y value
        #     self.perlinNoise.append(0) # make array of just 0s
        
        # for y in range(len(self.tileMap)): # create noise for each y value
        #     self.perlinNoise[y] = eval(self.noise, self.xVals, y)

        # self.generatePlatforms() # generate twice
        # self.seed = random.randint(0, 1000)
        # self.generatePlatforms()
        # self.startingPlat() # make sure there is a starting platform

        # for platform in self.platformList: # remove out of range plats
        #     if platform.y < 0:
        #         self.platformList.remove(platform)

    def startingPlat(self):
        count = 0
        for platform in self.platformList:
            if platform.y // self.tileSize >= self.startingThreshold:
                count += 1
            if platform.y <= 2:
                jumpablePlat = platform
                if count < 2:
                    x = random.randrange(jumpablePlat.x // self.tileSize - 2, 
                                        jumpablePlat.x // self.tileSize + 2)
                    self.platformList.append(Platform(x, random.randint(0, self.startingThreshold), 
                                                    random.randint(2, 5), self.tileSize))

    def generatePlatforms(self):
        for y in range(len(self.tileMap)):
            if self.perlinNoise[y] > self.threshold:
                platLength = random.randint(2, 5)
                x = random.randrange(0, len(self.tileMap[0]), platLength)
                self.platformList.append(Platform(x, y - 1, platLength, self.tileSize))

    def draw(self):
        rows, cols = len(self.tileMap), len(self.tileMap[0])
        for row in range(rows):
            for col in range(cols):
                if self.tileMap[row][col] != 0:
                    drawRect(self.x + self.tileSize*col, 
                             self.y + self.tileSize*row, self.tileSize, 
                             self.tileSize, fill='red')
        # for platform in self.platformList:
        #     platform.draw()
    
    def scroll(self, player):
        if player.xVel > 0:
            sign = 1
        else:
            sign = -1

        if player.x > self.cameraRight and self.x > -self.cameraRight:
            player.x = self.cameraRight
            cameraDelta = sign * (abs(player.xVel) + Player.acceleration) / Player.delta
            if almostEqual(player.xVel, 0):
                cameraDelta = 0
            self.x -= cameraDelta
        elif player.x < self.cameraLeft and -self.cameraLeft < self.x < 0:
            player.x = self.cameraLeft
            cameraDelta = sign * (abs(player.xVel) + Player.acceleration) / Player.delta
            if almostEqual(player.xVel, 0):
                cameraDelta = 0
            self.x -= cameraDelta
        elif self.x >= 0:
            self.x = 0