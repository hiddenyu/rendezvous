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
from randomlevel import *
import math, copy, random

# CHECKLIST :
# - occasional glitch where items/portal get displaced when moving and dashing
# - random terrain generation (collisions have not worked)
# - finalize start screen
# - implement items and scores for random mode
# - crystal bar in top corner
# - mana bar for dash?

# - remember to change back constants!

def onAppStart(app):
    # app constants
    app.stepsPerSecond = Player.delta
    app.width, app.height = 1920, 1080
    app.startScreen = True
    app.gameScreen = False
    app.randomMode = True

    # player constants
    app.player = Player(100, 900)

    if app.gameScreen:
        app.player.abilities = set()
    elif app.randomMode:
        app.player.abilities = {'dash', 'double jump'}

    # level constants
    app.tileMaps = Tilemaps()
    app.levels = [Level(app.tileMaps.tileMap0, 0, 5, 'level0.png'), Level(app.tileMaps.tileMap1, 1, 3, 'level0.png'), 
                  Level(app.tileMaps.tileMap2, 2, 4, 'level0.png')]
    app.level = app.levels[0]
    app.tileSize = app.level.tileSize

    # camera constants
    app.cameraLeft = 600
    app.cameraRight = app.level.width - app.width - app.cameraLeft
    app.camera = Camera(app, 0, 0, app.cameraLeft, app.cameraRight)

    # random level constants
    app.randomLevel = RandomLevel()

def redrawAll(app):
    if app.level.index != 3 and app.gameScreen: # story mode
        app.level.draw(app)
        for i in range(app.level.itemCount):
            app.level.items[i].draw()
        if app.level.portal.worldDone:
            app.level.portal.draw()
        app.player.draw()

    elif app.randomMode: # randomly generated
        app.randomLevel.draw()
        app.player.draw()

    elif app.startScreen: # start screen
        drawLabel('start', 1000, 500)
        drawLabel('random mode', 1000, 750)

    else: # end screen
        drawLabel('finished', 1000, 500)

def onStep(app):
    if app.level.index != 3 and app.gameScreen: # story mode
        app.player.onGround = app.player.doStep(app, app.level)
        app.cameraDelta = app.camera.scroll(app.level, app.player)

        # portal checks
        app.level.portal.scroll(app)
        if len(app.player.collected) == app.level.totalItems - 1:
            app.level.portal.worldDone = True
        if app.level.portal.worldDone:
            app.level.portal.checkCollide(app.player)
        
        # item checks
        for item in app.level.items:
            item.checkCollide(app.player)
            app.player.giveAbilities()
            item.scroll(app)

    elif app.randomMode: # randomly generated
        app.player.onGround = app.player.doStepRandom(app, app.randomLevel)
        app.cameraDelta = app.camera.scroll(app.randomLevel, app.player)

        for platform in app.randomLevel.platformList:
            platform.scroll(app)
        app.randomLevel.generate()

        # # item checks
        # for item in app.level.items:
        #     item.checkCollide(app.player)
        #     app.player.giveAbilities()
        #     item.scroll(app)

def onMousePress(app, mouseX, mouseY):
    if app.startScreen:
        app.randomMode = True

def onKeyPress(app, key):
    if app.level.index != 3 and (app.gameScreen or app.randomMode):
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

                if app.gameScreen:
                    app.cameraDelta = app.camera.dashScroll(app.level, app.player)
                    for item in app.level.items:
                        item.dashScroll(app)
                        app.level.portal.dashScroll(app)

                elif app.randomMode:
                    app.cameraDelta = app.camera.dashScroll(app.randomLevel, app.player)
                    for platform in app.randomLevel.platformList:
                        platform.dashScroll(app)

def onKeyHold(app, keys):
    if app.level.index != 3 and (app.gameScreen or app.randomMode):
        if 'd' in keys:
            app.player.moveRight()
        if 'a' in keys:
            app.player.moveLeft()

def main():
    runApp()

main()