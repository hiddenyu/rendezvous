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
# - win/lose condition
# - powerups
# - random terrain generation
#       - i think procedural is best?

def onAppStart(app):
    # app constants
    app.stepsPerSecond = Player.delta
    app.width, app.height = 1920, 1080

    # player constants
    app.player = Player(300, 0)
    app.onGround = False

    # level constants
    app.tileMaps = Tilemaps()
    app.level = Level(app.tileMaps.tileMap0, 0)
    app.tileSize = app.level.tileSize

    # item constants
    app.item = Item(800, 760, 1)

    # camera constants
    app.cameraLeft = 320
    app.cameraRight = app.level.width - app.width - app.cameraLeft
    app.camera = Camera(app, 0, 0, app.cameraLeft, app.cameraRight)

def redrawAll(app):
    app.player.draw()
    app.level.draw()
    app.item.draw()

def onStep(app):
    app.onGround = app.player.doStep(app, app.tileMaps.tileMap0, app.level)
    app.item.checkCollide(app.player)
    scroll(app.camera, app.item, app.player)
    scroll(app.camera, app.level, app.player)

def onKeyPress(app, key):
    if key == 'space' and app.onGround:
        app.player.jump()

def onKeyHold(app, keys):
    if 'd' in keys:
        app.player.moveRight()
    if 'a' in keys:
        app.player.moveLeft()

def scroll(camera, object, player):
    if player.xVel > 0:
        sign = 1
    else:
        sign = -1

    # if player moves to right 
    if player.x > camera.cameraRight and object.x > -camera.cameraRight:
        player.x = camera.cameraRight
        cameraDelta = sign * (abs(player.xVel) + Player.acceleration) / Player.delta
        if almostEqual(player.xVel, 0):
            cameraDelta = 0
        object.x -= cameraDelta
    
    # if player moves to left
    elif player.x < camera.cameraLeft and object.x < -camera.cameraLeft and object.x < 0:
        player.x = camera.cameraLeft
        cameraDelta = sign * (abs(player.xVel) + Player.acceleration) / Player.delta
        if almostEqual(player.xVel, 0):
            cameraDelta = 0
        object.x -= cameraDelta
    
    # hitting edges
    if camera.x >= 0:
        camera.x = 0
    if camera.x <= -camera.width:
        camera.x = -camera.width
    
    return object.x

def main():
    runApp()

main()