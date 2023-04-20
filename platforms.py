from cmu_graphics import *
from PIL import Image

class Platform:
    def __init__(self, x, y, width, tileSize):
        self.tileSize = tileSize
        self.x, self.y = x*self.tileSize, y*self.tileSize
        self.width = width*self.tileSize
    
    # collision concepts from http://jeffreythompson.org/collision-detection/rect-rect.php
    def yCollide(self, player):
        left, right = self.x, self.x + self.width
        top, bot = self.y, self.y + self.tileSize

        playerLeft, playerTop = player.x, player.y
        playerRight = playerLeft + player.width
        playerBot = playerTop + player.height

        onGround = False
        if not (playerLeft >= right or playerRight <= left):
            if playerBot >= top and playerTop <= bot:
                if player.yVel > 0: # if moving down
                    player.y = top - player.height
                    player.yVel = 0
                    onGround = True
                elif player.yVel < 0: # if moving up
                    player.y = bot
                    player.yVel = 0
                return onGround
    
    def xCollide(self, player):
        left, right = self.x, self.x + self.width
        top, bot = self.y, self.y + self.tileSize

        playerLeft, playerTop = player.x, player.y
        playerRight = playerLeft + player.width
        playerBot = playerTop + player.height

        if not (playerTop >= bot or playerBot <= top):
            if playerRight >= left and playerLeft <= right:
                if player.xVel > 0: # if moving to right
                    player.x = left - player.width
                    player.xVel = 0
                elif player.xVel < 0: # if moving to left
                    player.x = right
                    player.xVel = 0

    def __repr__(self):
        return f'Platform({self.x}, {self.y}, {self.width // self.tileSize})'

    def draw(self):
        drawRect(self.x, self.y, self.width, self.tileSize, fill='blue')