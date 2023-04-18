from cmu_graphics import *
from PIL import Image

class Item:
    width, height = 50, 50

    def __init__(self, x, y, index):
        self.x, self.y = x, y - Item.height
        self.index = index
        self.sprite = CMUImage(Image.open('pfp.jpg'))
        self.isVisible = True
        # get a way so only the visible item can be interacted with
        
    def checkCollide(self, player):
        if self.isVisible:
            left, right = self.x, self.x + Item.width
            top, bot = self.y, self.y + Item.height

            playerLeft, playerTop = player.x, player.y
            playerRight = playerLeft + player.width
            playerBot = playerTop + player.height
            if playerRight >= left and playerLeft <= right:
                if playerBot >= top and playerTop <= bot:
                    self.isVisible = False
                    player.collected.append(self.index)

    def draw(self):
        if self.isVisible:
            drawImage(self.sprite, self.x, self.y, width=Item.width, 
                    height=Item.height)