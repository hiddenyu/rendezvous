#################################################
# term project: rendezvous
# name: Yujun Wu
# andrew id: yujunwu
#################################################

from cmu_graphics import *
from player import Player
import math, copy

def onAppStart(app):
    app.width, app.height = 1920, 1080
    app.player = Player(1000, 500)

def redrawAll(app):
    drawRect(app.player.x, app.player.y, app.player.width, app.player.height, 
             fill='red')

def onStep(app):
    pass

def onKeyPress(app, key):
    if key == 'space':
        app.player.y -= 50

def onKeyHold(app, keys):
    if 'right' in keys:
        app.player.x += 10
    if 'left' in keys:
        app.player.x -= 10

def main():
    runApp()

main()