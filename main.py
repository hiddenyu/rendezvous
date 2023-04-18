#################################################
# term project: rendezvous
# name: Yujun Wu
# andrew id: yujunwu
#################################################

from cmu_graphics import *
from PIL import Image
from player import *
from level import *
from item import *
from tilemaps import *
import math, copy, time, random
# time for timed events later on

# CHECKLIST :
# - win/lose condition
# - powerups
# - side scrolling
# - random terrain generation
#       - i think procedural is best?

def onAppStart(app):
    app.stepsPerSecond = Player.delta
    app.width, app.height = 1920, 1080
    app.player = Player(300, 0)
    app.tileMaps = Tilemaps()
    app.level = Level(app.tileMaps.tileMap1)
    app.onGround = False
    app.item = Item(800, 760, 1)

def redrawAll(app):
    app.player.draw()
    app.level.draw()
    app.item.draw()
    app.level.newPlatform()

def onStep(app):
    app.player.doStep(app, app.tileMaps.tileMap1)
    app.item.checkCollide(app.player)
    if app.player.yVel == 0:
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