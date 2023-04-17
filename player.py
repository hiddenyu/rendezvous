from cmu_graphics import *
from PIL import Image

class Player:
    jumpForce = 500
    acceleration = 50
    gravityForce = 25
    frictionForce = 25
    maxSpeed = 500
    maxFall = 500
    delta = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.sprite = CMUImage(Image.open('test.jpg'))
        self.width, self.height = getImageSize(self.sprite)
    
    # to animate with sprite strip
    # app.sprites = []
    # for i in range(frames):
    #       frame = Image(sprite.crop((x1, y1, x2, y2)))
    #       app.sprites.append(frame)
    # app.spriteCounter = 0
    # onStep -> app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites) 
    # could use 2d list, each row being idle, run, etc.
    #
    # for gifs, use gif.seek(frame) by looping for frame in range(gif.n_frames)

    def draw(self):
        drawImage(self.sprite, self.x, self.y)

    def applyGravity(self):
        self.yVel += Player.gravityForce
        self.yVel = min(self.yVel, Player.maxFall)
        self.y += self.yVel / Player.delta
    
    def applyAccel(self):
        if self.xVel < 0:
            sign = -1
        else:
            sign = 1
        self.xVel = sign * min(abs(self.xVel), Player.maxSpeed)
        self.x += self.xVel / Player.delta
    
    def applyFriction(self):
        if self.xVel < 0:
            sign = 1
        else:
            sign = -1
        if self.xVel != 0:
            self.xVel += sign * Player.frictionForce
            self.x += self.xVel / Player.delta

    def moveRight(self):
        self.xVel += Player.acceleration
    
    def moveLeft(self):
        self.xVel -= Player.acceleration
    
    def jump(self):
        self.yVel = -Player.jumpForce

    # collision detection concepts from http://jeffreythompson.org/collision-detection/rect-rect.php
    def checkYCollide(self, app, tileMap):
        rows, cols = len(tileMap), len(tileMap[0])

        tileW = app.width / cols
        tileH = app.height / rows

        for row in range(rows):
            for col in range(cols):
                left, right = tileW*col, tileW + tileW*col
                top, bot = tileH*row, tileH + tileH*row

                playerLeft, playerTop = self.x, self.y
                playerRight = playerLeft + self.width
                playerBot = playerTop + self.height
                if tileMap[row][col] != 0:
                    if not (playerLeft >= right or playerRight <= left):
                        if playerBot >= top and playerTop <= bot:
                            if self.yVel > 0:
                                self.y = top - self.height
                                self.yVel = 0
                            elif self.yVel < 0:
                                self.y = bot
                                self.yVel = 0
                            return True
    
    def checkXCollide(self, app, tileMap):
        rows, cols = len(tileMap), len(tileMap[0])

        tileW = app.width / cols
        tileH = app.height / rows

        for row in range(rows):
            for col in range(cols):
                left, right = tileW*col, tileW + tileW*col
                top, bot = tileH*row, tileH + tileH*row

                playerLeft, playerTop = self.x, self.y
                playerRight = playerLeft + self.width
                playerBot = playerTop + self.height
                if tileMap[row][col] != 0:
                    if not (playerTop >= bot or playerBot <= top):
                        if playerRight >= left and playerLeft <= right:
                            if self.xVel > 0:
                                self.x = left - self.width
                                self.xVel = 0
                            elif self.xVel < 0:
                                self.x = right
                                self.xVel = 0
                            return True

    def doStep(self, app, tileMap):
        app.player.applyGravity()
        app.player.checkYCollide(app, app.tileMap)
        app.player.applyAccel()
        app.player.applyFriction()
        app.player.checkXCollide(app, app.tileMap)