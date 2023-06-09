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

        cameraDelta = 0
        # if player moves to right 
        if player.x > self.cameraRight and object.x > app.width - self.width:
            player.x = self.cameraRight
            cameraDelta = sign * (abs(player.xVel) + Player.acceleration) / Player.delta
            if almostEqual(player.xVel, 0):
                cameraDelta = 0
            object.x -= cameraDelta
        
        # if player moves to left
        elif player.x < self.cameraLeft and object.x < 0:
            player.x = self.cameraLeft
            cameraDelta = sign * (abs(player.xVel) + Player.acceleration) / Player.delta
            if almostEqual(player.xVel, 0):
                cameraDelta = 0
            object.x -= cameraDelta
        
        # hitting edges
        if object.x > 0:
            object.x = 0
            cameraDelta = 0
        if object.x <= app.width - self.width:
            object.x = app.width - self.width
            cameraDelta = 0

        return cameraDelta
    
    def dashScroll(self, object, player):
        # if player dashes
        dashDelta = 0
        if player.xVel > 0 and object.x > app.width - self.width:
            object.x -= Player.dashForce
            dashDelta = -Player.dashForce
        
        elif player.xVel < 0 and object.x < 0:
            object.x += Player.dashForce
            dashDelta = Player.dashForce
        
        # hitting edges
        if object.x > 0:
            object.x = 0
            dashDelta = 0
        if object.x <= app.width - self.width:
            object.x = app.width - self.width
            dashDelta = 0

        return dashDelta

    def randomScroll(self, object, player):
        cameraDelta = 0
        # if player moves to right 
        if player.x > self.cameraRight:
            player.x = self.cameraRight
            cameraDelta = (abs(player.xVel) + Player.acceleration) / Player.delta
            if almostEqual(player.xVel, 0):
                cameraDelta = 0
            object.x -= cameraDelta

        # hitting edges
        if player.x < 0:
            player.x = 0
            cameraDelta = 0
        # if object.x <= app.width - self.width:
        #     object.x = app.width - self.width
        #     cameraDelta = 0

        return cameraDelta
    
    def randomDashScroll(self, object, player):
        # if player dashes
        dashDelta = 0
        if player.xVel > 0:
            object.x -= Player.dashForce
            dashDelta = -Player.dashForce

        # hitting edges
        if player.x < 0:
            player.x = 0
            dashDelta = 0
        # if object.x <= app.width - self.width:
        #     object.x = app.width - self.width
        #     dashDelta = 0

        return dashDelta