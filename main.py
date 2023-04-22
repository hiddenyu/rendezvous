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
import math, copy, random

# CHECKLIST :
# - add levels
# - random terrain generation (collisions have not worked)

def onAppStart(app):
    # app constants
    app.stepsPerSecond = Player.delta
    app.width, app.height = 1920, 1080

    # player constants
    app.player = Player(300, 0)

    # level constants
    app.tileMaps = Tilemaps()
    app.levels = [Level(app.tileMaps.tileMap0, 0, 5), Level(app.tileMaps.tileMap1, 1, 3), Level(app.tileMaps.tileMap2, 2, 4)]
    app.level = app.levels[0]
    app.tileSize = app.level.tileSize

    # item constants
    app.items = []
    for i in range(1, app.level.itemCount + 1):
        app.items.append(Item(100*i + 300, 900, i))

    # camera constants
    app.cameraLeft = 600
    app.cameraRight = app.level.width - app.width - app.cameraLeft
    app.camera = Camera(app, 0, 0, app.cameraLeft, app.cameraRight)

def redrawAll(app):
    app.player.draw()
    app.level.draw(app)
    for i in range(app.level.itemCount):
        app.items[i].draw()

def onStep(app):
    app.player.onGround = app.player.doStep(app, app.level)
    app.cameraDelta = app.camera.scroll(app.level, app.player)

    # portal checks
    app.level.portal.scroll(app)
    app.level.portal.checkCollide(app.player)
    if len(app.player.collected) == app.level.itemCount:
        app.level.portal.worldDone = True
    
    # item checks
    for item in app.items:
        item.checkCollide(app.player)
        app.player.giveAbilities()
        item.scroll(app)

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
            app.player.dash()
            app.camera.dashScroll(app.level, app.player)

def onKeyHold(app, keys):
    if 'd' in keys:
        app.player.moveRight()
    if 'a' in keys:
        app.player.moveLeft()

def main():
    runApp()

main()