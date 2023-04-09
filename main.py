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
    app.player = Player(1000, 500)

    app.isStopped = True

def redrawAll(app):
    drawImage(app.player.sprite, app.player.x, app.player.y)

def onStep(app):
    # app.player.applyGravity()
    app.player.applyAccel()
    if app.isStopped:
        app.player.applyFriction()

def onKeyPress(app, key):
    if key == 'space':
        app.player.jump()

# friction works only for right movement, left vel since vel alr neg, it = 0
def onKeyHold(app, keys):
    if 'd' in keys:
        app.player.moveRight()
        app.isStopped = False
    if 'a' in keys:
        app.player.moveLeft()
        app.isStopped = False

def onKeyRelease(app, key):
    if key == 'd' or key == 'a':
        app.isStopped = True

def main():
    runApp()

main()