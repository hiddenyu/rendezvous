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
# - implement items and scores for random mode
# - for random mode, make it so set number of plats
# - crystal bar in top corner
# - mana bar for dash?

# - remember to change back constants!

def onAppStart(app):
    reset(app)

def reset(app):
    # app constants
    app.stepsPerSecond = Player.delta
    app.width, app.height = 1920, 1080
    app.startScreen = True
    app.gameScreen = False
    app.endScreen = False

    app.randomMode = False
    app.randomEndScreen = False

    # player constants
    app.player = Player(100, 900)

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

def redrawAll(app):
    ### story mode ###
    if app.gameScreen:
        app.level.draw(app)
        for i in range(app.level.itemCount):
            app.level.items[i].draw()
        if app.level.portal.worldDone:
            app.level.portal.draw()
        app.player.draw()

    ### random mode ###
    elif app.randomMode:
        if app.timerChoice == 0:
            drawLabel('30', 500, 500)
            drawLabel('60', 600, 500)
            drawLabel('120', 700, 500)
        else:
            app.randomLevel.draw()
            app.player.draw()
            drawLabel(f'{app.timer}', 100, 300)

    elif app.randomEndScreen:
        drawLabel('random done', 1000, 500)

    ### end screen ###
    elif app.endScreen:
        drawLabel('finished', 1000, 500)

    ### start screen ###
    elif app.startScreen:
        drawLabel('start', 1000, 500)
        drawLabel('random mode', 1000, 750)

def onStep(app):
    ### story mode ###
    if app.gameScreen:
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
        
        if app.level.index == 2 and app.player.completed:
            app.gameScreen = False
            app.endScreen = True

    ### random mode ###
    elif app.randomMode:
        if app.timer > 0:
            app.timer -= 1
            app.player.onGround = app.player.doStepRandom(app, app.randomLevel)
            app.randCameraDelta = app.camera.randomScroll(app.randomLevel, app.player)

            for platform in app.randomLevel.platformList:
                platform.scroll(app)
            app.randomLevel.generate()
        elif app.timer != -1:
            app.randomEndScreen = True
            app.randomMode = False

        # # item checks
        # for item in app.level.items:
        #     item.checkCollide(app.player)
        #     app.player.giveAbilities()
        #     item.scroll(app)

def onMousePress(app, mouseX, mouseY):
    if app.randomMode and app.timerChoice == 0:
        app.timerChoice = 30
        app.timer = app.stepsPerSecond * app.timerChoice

    elif app.startScreen:
        if 800 <= mouseX <= 1200:
            if 450 <= mouseY <= 550:
                app.gameScreen = True
                app.startScreen = False
                app.player.abilities = set()
            elif 700 <= mouseY <= 800:
                app.randomMode = True
                app.startScreen = False

                # random level constants
                app.randomLevel = RandomLevel()
                app.timerChoice = 0
                app.timer = -1
                app.player.abilities = {'dash', 'double jump'}

def onKeyPress(app, key):
    if (app.gameScreen or app.randomMode):
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
                    app.randCameraDelta = app.camera.randomDashScroll(app.randomLevel, app.player)
                    for platform in app.randomLevel.platformList:
                        platform.dashScroll(app)
    elif app.endScreen or app.randomEndScreen:
        if key == 'r':
            reset(app)

def onKeyHold(app, keys):
    if (app.gameScreen or app.randomMode):
        if 'd' in keys:
            app.player.moveRight()
        if 'a' in keys:
            app.player.moveLeft()

def main():
    runApp()

main()