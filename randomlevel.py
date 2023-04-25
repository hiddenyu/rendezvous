from cmu_graphics import *
from PIL import Image
from perlin import *
from level import *
from player import *
import random, math

class RandomLevel:
    itemsCollected = 1

    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = app.width, app.height
        self.tileSize = 60

        self.cameraLeft = 600
        self.cameraRight = self.width - self.cameraLeft

        # platform constants
        self.platformList = []
        self.platCount = 15
        self.floorPlat = Platform(0, 17, self.width//self.tileSize, 60)
        self.seed = random.randint(0, 1000)
        self.xVals = 256
        self.threshold = 0.3
        self.noise = randomNoise(self.seed, self.xVals)
        self.perlinNoise = []

        # item constants
        self.itemList = []
        self.itemCount = 5

        for y in range(self.height): # for each y value
            self.perlinNoise.append(0) # make array of just 0s
        for y in range(self.height): # create noise for each y value
            self.perlinNoise[y] = eval(self.noise, self.xVals, y)
        self.newPlats()
        self.newItems()
        
        for platform in self.platformList: # remove out of range plats
            if platform.y < 0:
                self.platformList.remove(platform)
        for item in self.itemList: # remove out of range items
            if item.y < 0:
                self.itemList.remove(item)

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

    def newItems(self):
        diff = self.itemCount - len(self.itemList)
        for i in range(diff):
            platIndex = random.randint(0, len(self.platformList) - 1)
            spawnPlatform = self.platformList[platIndex]

            # # spawn items ahead of player
            # while spawnPlatform.x < app.player.x:
            #     platIndex = random.randint(0, len(self.platformList) - 1)
            #     spawnPlatform = self.platformList[platIndex]
            itemX = random.randint(math.floor(spawnPlatform.x), math.floor(spawnPlatform.x + spawnPlatform.width))

            iconIndex = random.randint(0, 11)
            icon = app.itemIcons[iconIndex]
            newItem = Item(itemX, spawnPlatform.y, RandomLevel.itemsCollected, icon)

            # check if new item is inside a platform or not
            for platform in self.platformList:
                left, right = platform.x, platform.x + platform.width
                top, bot = platform.y, platform.y + platform.tileSize

                itemLeft, itemTop = newItem.x, newItem.y
                itemRight = itemLeft + newItem.width
                itemBot = itemTop + newItem.height

                if not (itemLeft >= right or itemRight <= left):
                    if itemBot >= top and itemTop <= bot:
                        # if it is, spawn on top of that one
                        itemX = platform.x + (platform.width / 2)
                        newItem = Item(itemX, platform.y, RandomLevel.itemsCollected, icon)
            
            # # check if new item is close to existing one
            # for item in self.itemList:
            #     if abs(newItem.x - item.x) < 250 and newItem.y == item.y:
            #         self.itemList.remove(item)

            self.itemList.append(newItem)
            RandomLevel.itemsCollected += 1

        # if out of range
        for item in self.itemList:
            if item.x < 0:
                self.itemList.remove(item)

    def draw(self):
        self.floorPlat.draw()
        for platform in self.platformList:
            platform.draw()
        for item in self.itemList:
            item.draw()
