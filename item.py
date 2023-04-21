from cmu_graphics import *
from PIL import Image

class Item:
    width, height = 50, 50

    def __init__(self, x, y, index):
        self.x, self.y = x, y - Item.height
        self.index = index
        self.sprite = CMUImage(Image.open('pfp.jpg'))
        self.isVisible = True
        
    def checkCollide(self, player):
        if self.isVisible:
            left, right = self.x, self.x + Item.width
            top, bot = self.y, self.y + Item.height

            playerLeft, playerTop = player.x, player.y
            playerRight = playerLeft + player.width
            playerBot = playerTop + player.height
            if playerRight >= left and playerLeft <= right:
                if playerBot >= top and playerTop <= bot:
                    player.collected.add(self.index)
                    self.isVisible = False

    def draw(self):
        if self.isVisible:
            drawImage(self.sprite, self.x, self.y, width=Item.width, 
                    height=Item.height)
    
    def __repr__(self):
        return f'Item({self.x}, {self.y}, {self.index})'