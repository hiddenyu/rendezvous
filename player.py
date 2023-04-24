from cmu_graphics import *
from physics import *
from platforms import *
from PIL import Image

class Player:
    # physics constants
    jumpForce = 1000
    acceleration = 150
    gravityForce = 100
    frictionForce = 0.5
    maxSpeed = 500
    maxFall = 1000
    delta = 30
    dashForce = 200

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.load = [x, y]
        self.xVel = 0
        self.yVel = 0
        self.score = 0

        # ability constants
        self.collected = set()
        self.abilities = set()
        self.completed = False
        self.onGround = False
        self.canDoubleJump = False

        self.sprite = CMUImage(Image.open('test.jpg'))
        self.width, self.height = 60, 60
    
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
    def checkYCollide(self, app, tileMap, levelX):
        return yCollide(self, app, tileMap, levelX)
    
    def checkXCollide(self, app, tileMap, levelX):
        xCollide(self, app, tileMap, levelX)

    def respawn(self):
        self.x = self.load[0]
        self.y = self.load[1]

    def doStep(self, app, level):
        tileMap = level.tileMap
        self.giveAbilities()
        self.applyGravity()
        onGround = self.checkYCollide(app, tileMap, level.x)

        self.applyAccel()
        self.applyFriction()
        self.checkXCollide(app, tileMap, level.x)

        if self.y > app.height:
            self.respawn()
        if self.x <= 0:
            self.x = 0
        if self.x >= app.width - self.width:
            self.x = app.width - self.width

        return onGround

    def doStepRandom(self, app, level):
        self.giveAbilities()
        self.applyGravity()

        onGround = False
        for platform in level.platformList:
            if platform.yCollide(self):
                onGround = True

        self.applyAccel()
        self.applyFriction()
        for platform in level.platformList:
            platform.xCollide(self)

        # if self.y > app.height:
        #     self.respawn()
        if self.x <= 0:
            self.x = 0
        if self.x >= app.width - self.width:
            self.x = app.width - self.width
        
        return onGround

    def giveAbilities(self):
        if self.collected == {1, 2, 3, 4, 5}:
            self.abilities.add('dash')
        elif self.collected == {1, 2, 3, 4, 5, 6, 7, 8}:
            self.abilities.add('double jump')
        elif self.collected == {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}:
            self.completed = True
    
    def dash(self):
        if self.xVel > 0 or almostEqual(self.xVel, 0):
            self.x += Player.dashForce
        else:
            self.x -= Player.dashForce