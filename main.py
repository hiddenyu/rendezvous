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
from platforms import *
from camera import *
import math, copy, time, random
# time for timed events later on

# CHECKLIST :
# - item creation per level, still doesnt scroll with level
# - win/lose condition
# - random terrain generation (collisions have not worked)
#       - i think procedural is best?

def onAppStart(app):
    # app constants
    app.stepsPerSecond = Player.delta
    app.width, app.height = 1920, 1080

    # player constants
    app.player = Player(300, 0)

    # level constants
    app.tileMaps = Tilemaps()
    app.level = Level(app.tileMaps.tileMap0, 0)
    app.tileSize = app.level.tileSize

    # item constants
    app.items = []
    for i in range(1, app.level.itemCount + 1):
        app.items.append(Item(100*i + 300, 900, i))

    # camera constants
    app.cameraLeft = 320
    app.cameraRight = app.level.width - app.width - app.cameraLeft
    app.camera = Camera(app, 0, 0, app.cameraLeft, app.cameraRight)

def redrawAll(app):
    app.player.draw()
    app.level.draw(app)
    for i in range(app.level.itemCount):
        app.items[i].draw()

def onStep(app):
    app.player.onGround = app.player.doStep(app, app.tileMaps.tileMap0, app.level)
    for item in app.items:
        item.checkCollide(app.player)
        app.player.giveAbilities()
    app.camera.scroll(app.level, app.player)

def onKeyPress(app, key):
    if key == 'space':
        if app.player.onGround:
            app.player.jump()
            app.player.canDoubleJump = True
        elif 'double jump' in app.player.abilities and app.player.canDoubleJump:
            app.player.jump()
            app.player.canDoubleJump = False
    if key == 'e':
        if 'dash' in app.player.abilities:
            app.player.dashed = True
            app.player.dash()
            app.player.dashed = False

def onKeyHold(app, keys):
    if 'd' in keys:
        app.player.moveRight()
    if 'a' in keys:
        app.player.moveLeft()

def main():
    runApp()

main()