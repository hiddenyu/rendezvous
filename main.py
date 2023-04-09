#################################################
# term project: rendezvous
# name: Yujun Wu
# andrew id: yujunwu
#################################################

from cmu_graphics import *
from player import Player
import math, copy

def onAppStart(app):
    app.stepsPerSecond = Player.delta
    app.width, app.height = 1920, 1080
    app.player = Player(1000, 0)

def redrawAll(app):
    drawImage(app.player.sprite, app.player.x, app.player.y)

def onStep(app):
    app.player.applyGravity()
    app.player.applyAccel()
    app.player.applyFriction()

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