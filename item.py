from cmu_graphics import *
from camera import *
from PIL import Image

class Item:
    def __init__(self, x, y, index, icon):
        self.width, self.height = 50, 50
        self.x, self.y = x, y - self.height
        self.index = index
        self.sprite = CMUImage(Image.open(icon))
        self.isVisible = True
        
    def checkCollide(self, player):
        if self.isVisible:
            left, right = self.x, self.x + self.width
            top, bot = self.y, self.y + self.height

            playerLeft, playerTop = player.x, player.y
            playerRight = playerLeft + player.width
            playerBot = playerTop + player.height

            collided = False
            if playerRight >= left and playerLeft <= right:
                if playerBot >= top and playerTop <= bot:
                    player.collected.add(self.index)
                    collided = True
                    self.isVisible = False
        return collided

    def scroll(self, app):
        self.x -= app.cameraDelta
    
    def dashScroll(self, app):
        self.x += app.cameraDelta

    def randomScroll(self, app):
        self.x -= app.randCameraDelta
    
    def randomDashScroll(self, app):
        self.x += app.randCameraDelta

    def draw(self):
        if self.isVisible:
            drawImage(self.sprite, self.x, self.y, width=self.width, 
                    height=self.height)
    
    def __repr__(self):
        return f'Item({self.x}, {self.y}, {self.index})'