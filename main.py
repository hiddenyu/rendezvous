#################################################
# term project: rendezvous
# name: Yujun Wu
# andrew id: yujunwu
#################################################

from cmu_graphics import *
from PIL import Image
from player import Player
import math, copy

def onAppStart(app):
    app.stepsPerSecond = Player.delta
    app.width, app.height = 1920, 1080
    app.player = Player(1000, 0)
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

def checkCollision(player, tileMap, tileW, tileH):
    rows, cols = len(tileMap), len(tileMap[0])
    for row in range(rows):
        for col in range(cols):
            if tileMap[row][col] != 0:
                left, right = 0 + 120*col, 120 + 120*col
                top, bot = 0 + 120*row, 120 + 120*row
                playerLeft, playerTop = app.player.x, app.player.y
                playerRight = playerLeft + app.player.width
                playerBot = playerTop + app.player.height

def main():
    runApp()

main()