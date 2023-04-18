from cmu_graphics import *
from physics import *
from PIL import Image

class Player:
    jumpForce = 1000
    acceleration = 200
    gravityForce = 100
    frictionForce = 0.5
    maxSpeed = 500
    maxFall = 1000
    delta = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.load = [x, y]
        self.xVel = 0
        self.yVel = 0
        self.collected = []
        self.abilities = []
        self.completed = False
        self.sprite = CMUImage(Image.open('test.jpg'))
        self.width, self.height = getImageSize(self.sprite)
        self.width, self.height = self.width / 3, self.height / 3
    
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
        drawImage(self.sprite, self.x, self.y, width=self.width, 
                  height=self.height)

    def applyGravity(self):
        gravity(self, Player.gravityForce, Player.maxFall, Player.delta)
    
    def applyAccel(self):
        accel(self, Player.maxSpeed, Player.delta)
    
    def applyFriction(self):
        friction(self, Player.frictionForce, Player.delta)

    def moveRight(self):
        self.xVel += Player.acceleration
    
    def moveLeft(self):
        self.xVel -= Player.acceleration
    
    def jump(self):
        self.yVel = -Player.jumpForce

    # collision detection concepts from http://jeffreythompson.org/collision-detection/rect-rect.php
    def checkYCollide(self, app, tileMap):
        yCollide(self, app, tileMap)
    
    def checkXCollide(self, app, tileMap):
        xCollide(self, app, tileMap)

    def respawn(self):
        self.x = self.load[0]
        self.y = self.load[1]

    def doStep(self, app, tileMap):
        self.giveAbilities()
        self.applyGravity()
        self.checkYCollide(app, tileMap)
        self.applyAccel()
        self.applyFriction()
        self.checkXCollide(app, tileMap)
        if self.y > app.height:
            self.respawn()
        if self.x <= 0:
            self.x = 0

    def giveAbilities(self):
        if len(self.collected) == 5:
            self.abilities.append('dash')
        elif len(self.collected) == 8:
            self.abilities.append('double jump')
        elif len(self.collected) == 12:
            self.completed = True