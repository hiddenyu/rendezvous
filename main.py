#################################################
# term project: rendezvous
# name: Yujun Wu
# andrew id: yujunwu
#################################################

from cmu_graphics import *
from PIL import Image
from player import *
from tile import *
import math, copy, time
# time for timed events later on

def onAppStart(app):
    app.stepsPerSecond = Player.delta
    app.width, app.height = 1920, 1080
    app.player = Player(300, 0)
    app.tileMap = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    app.tiles = Tile(app.tileMap)
    app.onGround = False

def redrawAll(app):
    app.player.draw()
    app.tiles.draw()

def onStep(app):
    app.player.doStep(app, app.tileMap)
    if app.player.checkYCollide(app, app.tileMap) == True:
        app.onGround = True
    else:
        app.onGround = False

def onKeyPress(app, key):
    if key == 'space' and app.onGround:
        app.player.jump()

def onKeyHold(app, keys):
    if 'd' in keys:
        app.player.moveRight()
    if 'a' in keys:
        app.player.moveLeft()

def main():
    runApp()

main()