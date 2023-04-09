from cmu_graphics import *
import test

class Player:
    jumpForce = 500
    acceleration = 50
    gravityForce = 15
    frictionForce = 25
    maxSpeed = 250
    maxFall = 250
    delta = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.sprite = 'test.jpg'
        self.width, self.height = getImageSize(self.sprite)
    
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
        self.yVel -= Player.jumpForce