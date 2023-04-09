from cmu_graphics import *
import test

class Player:
    jumpForce = 500
    acceleration = 25
    gravityForce = 10
    frictionForce = 5
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
        self.y += self.yVel / Player.delta
    
    def applyAccel(self):
        self.x += self.xVel / Player.delta
    
    def applyFriction(self):
        self.xVel -= Player.frictionForce
        if self.xVel <= 0:
            self.xVel = 0

    def moveRight(self):
        self.xVel += Player.acceleration
    
    def moveLeft(self):
        self.xVel -= Player.acceleration
    
    def jump(self):
        self.yVel -= Player.jumpForce