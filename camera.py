from cmu_graphics import *
from player import *
from PIL import Image

class Camera:
    def __init__(self, app, x, y, left, right):
        self.x, self.y = x, y
        self.cameraLeft = left
        self.cameraRight = right
        self.width = app.level.width

    def scroll(self, object, player):
        if player.xVel > 0:
            sign = 1
        else:
            sign = -1

        # if player moves to right 
        if player.x > self.cameraRight and object.x > -self.cameraRight:
            player.x = self.cameraRight
            cameraDelta = sign * (abs(player.xVel) + Player.acceleration) / Player.delta
            if almostEqual(player.xVel, 0):
                cameraDelta = 0
            object.x -= cameraDelta
        
        # if player moves to left
        elif player.x < self.cameraLeft and object.x < -self.cameraLeft and object.x < 0:
            player.x = self.cameraLeft
            cameraDelta = sign * (abs(player.xVel) + Player.acceleration) / Player.delta
            if almostEqual(player.xVel, 0):
                cameraDelta = 0
            object.x -= cameraDelta
        
        # hitting edges
        if object.x >= 0:
            object.x = 0
        if object.x <= -self.width:
            object.x = -self.width

        return object.x
    
    def dashScroll(self, object, player):
        # if player dashes
        if player.xVel > 0 and object.x > -self.cameraRight:
            # player.x = self.cameraRight
            object.x -= Player.dashForce
        
        elif player.xVel < 0 and object.x < -self.cameraLeft and object.x < 0:
            # player.x = self.cameraLeft
            object.x += Player.dashForce
        
        # hitting edges
        if object.x >= 0:
            object.x = 0
        if object.x <= -self.width:
            object.x = -self.width

        return object.x
