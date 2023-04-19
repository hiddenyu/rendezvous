from cmu_graphics import *
from PIL import Image

class Platform:
    def __init__(self, x, y, width, tileSize):
        self.tileSize = tileSize
        self.x, self.y = x*self.tileSize, y*self.tileSize
        self.width = width*self.tileSize
    
    # collision concepts from http://jeffreythompson.org/collision-detection/rect-rect.php
    def collide(self, player):
        left, right = self.x, self.x + self.width
        top, bot = self.y, self.y + self.tileSize

        playerLeft, playerTop = player.x, player.y
        playerRight = playerLeft + player.width
        playerBot = playerTop + player.height

        onGround = False
        if (playerTop < bot and playerBot > top and playerRight > left and 
            playerLeft < right):
            if player.yVel >= 0: # if moving down
                player.y = top - player.height
                player.yVel = 0
                onGround = True
                print('onGround', onGround)
                return onGround
            elif player.yVel < 0: # if moving up
                player.y = bot
                player.yVel = 0
            elif player.xVel > 0: # if moving to right
                player.x = left - player.width
                player.xVel = 0
            elif player.xVel < 0: # if moving to left
                player.x = right
                player.xVel = 0
        print('returning', onGround)
        return onGround

    def __repr__(self):
        return f'Platform({self.x}, {self.y}, {self.width // self.tileSize})'

    def draw(self):
        drawRect(self.x, self.y, self.width, self.tileSize, fill='blue')