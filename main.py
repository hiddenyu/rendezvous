#################################################
# term project: rendezvous
# name: Yujun Wu
# andrew id: yujunwu
#################################################

from cmu_graphics import *
from PIL import Image
from player import Player
import math, copy, time

def onAppStart(app):
    app.stepsPerSecond = Player.delta
    app.width, app.height = 1920, 1080
    app.player = Player(1000, 0)
    app.tileSize = 120
    app.tileMap = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

def redrawAll(app):
    drawImage(app.player.sprite, app.player.x, app.player.y)
    for row in range(len(app.tileMap)):
        for col in range(len(app.tileMap[0])):
            if app.tileMap[row][col] != 0:
                drawRect(app.tileSize*col, app.tileSize*row, app.tileSize,
                         app.tileSize, fill='red')
# can make a draw function inside player class to do this

def onStep(app):
    app.player.applyAccel()
    app.player.applyFriction()
    app.player.applyGravity()
    app.player.checkCollisions(app, app.tileMap)
    
# can combine these into a doStep inside player class

def onKeyPress(app, key):
    if key == 'space':
        app.player.jump()

def onKeyHold(app, keys):
    if 'd' in keys:
        app.player.moveRight()
    if 'a' in keys:
        app.player.moveLeft()

def main():
    runApp()

main()