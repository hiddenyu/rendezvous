from cmu_graphics import *
from camera import *
from PIL import Image

class Portal:
    width, height = 50, 100

    def __init__(self, x, y, index):
        self.x, self.y = x, y - Portal.height - 20
        self.index = index
        self.sprite = None
        self.worldDone = False
        
    def checkCollide(self, player):
        if self.worldDone:
            left, right = self.x, self.x + self.width
            top, bot = self.y, self.y + self.height

            playerLeft, playerTop = player.x, player.y
            playerRight = playerLeft + player.width
            playerBot = playerTop + player.height
            if playerRight >= left and playerLeft <= right:
                if playerBot >= top and playerTop <= bot:
                    if app.level.nextWorld == 3:
                        app.level.index = 3
                    else:
                        app.level = app.levels[app.level.nextWorld]
                        self.worldDone = False
                        app.player.x, app.player.y = 100, 800

    def scroll(self, app):
        self.x -= app.cameraDelta

    def dashScroll(self, app):
        self.x += app.cameraDelta

    def draw(self):
        if self.worldDone:
            drawRect(self.x, self.y, self.width, self.height, fill='blue')
    
    def __repr__(self):
        return f'Portal({self.x}, {self.y}, {self.index})'