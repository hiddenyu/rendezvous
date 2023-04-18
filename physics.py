from cmu_graphics import *

# collision detection concepts from http://jeffreythompson.org/collision-detection/rect-rect.php
def yCollide(self, app, tileMap, levelX):
    rows, cols = len(tileMap), len(tileMap[0])

    tileW = app.width / cols
    tileH = app.height / rows

    for row in range(rows):
        for col in range(cols):
            left, right = levelX + tileW*col, levelX + tileW + tileW*col
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

def xCollide(self, app, tileMap, levelX):
    rows, cols = len(tileMap), len(tileMap[0])

    tileW = app.width / cols
    tileH = app.height / rows

    for row in range(rows):
        for col in range(cols):
            left, right = levelX + tileW*col, levelX + tileW + tileW*col
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

def gravity(self, gravityForce, maxFall, delta):
    self.yVel += gravityForce
    self.yVel = min(self.yVel, maxFall)
    self.y += self.yVel / delta

def accel(self, maxSpeed, delta):
    if self.xVel < 0:
        sign = -1
    else:
        sign = 1
    self.xVel = sign * min(abs(self.xVel), maxSpeed)
    self.x += self.xVel / delta

def friction(self, frictionForce, delta):
    if self.xVel != 0:
        self.xVel *= frictionForce
        self.x += self.xVel / delta