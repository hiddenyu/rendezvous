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
# - draw sparkling effect for crystals
# - crystal bar in top corner
# - mana bar for dash?
# - when dashing in random mode items get displaced

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

    # item constants
    app.itemIcons = [r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal1.png", 
                     r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal2.png",
                     r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal3.png",
                     r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal4.png",
                     r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal5.png",
                     r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal6.png", 
                     r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal7.png",
                     r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal8.png",
                     r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal9.png",
                     r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal10.png",
                     r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal11.png",
                     r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\crystal12.png"]

    # level constants
    app.tileMaps = Tilemaps()
    level0 = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\level0.png"
    app.levels = [Level(app.tileMaps.tileMap0, 0, 5, level0), Level(app.tileMaps.tileMap1, 1, 3, level0), 
                  Level(app.tileMaps.tileMap2, 2, 4, level0)]
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
            drawLabel('Choose a time limit', 960, 500, size=75)
            drawLabel('30', 760, 750, size=50)
            drawLabel('60', 960, 750, size=50)
            drawLabel('120', 1160, 750, size=50)
        else:
            app.randomLevel.draw()
            app.player.draw()
            drawLabel(f'{app.timer // app.stepsPerSecond}', 100, 100, size=50)
            drawLabel(f'Collected: {app.player.score}', 1500, 100, size=50)

    elif app.randomEndScreen:
        drawLabel('random done', 960, 500, size=75)
        drawLabel(f'Score: {app.player.score}', 960, 750, size=50)
        drawLabel('click to restart', 960, 900, size=25)

    ### end screen ###
    elif app.endScreen:
        drawLabel('finished', 960, 500, size=75)
        drawLabel('click to restart', 960, 900, size=25)

    ### start screen ###
    elif app.startScreen:
        drawLabel('rendezvous', 960, 250, size=150)
        drawLabel('start', 960, 600, size=50)
        drawLabel('random mode', 960, 750, size=50)

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
        # timer is running
        if app.timer > 0:
            app.timer -= 1

            app.player.onGround = app.player.doStepRandom(app, app.randomLevel)
            app.randCameraDelta = app.camera.randomScroll(app.randomLevel, app.player)
            for platform in app.randomLevel.platformList:
                platform.scroll(app)
            app.randomLevel.generate()

            # if there are not enough platforms
            if len(app.randomLevel.platformList) <= app.randomLevel.platCount:
                diff = app.randomLevel.platCount - len(app.randomLevel.platformList)
                for i in range(diff):
                    platLength = random.randint(3, 5)
                    tileSize = app.randomLevel.tileSize
                    y = random.randint(2, app.randomLevel.height // tileSize)
                    if app.randomLevel.perlinNoise[y % app.randomLevel.height // tileSize] > app.randomLevel.threshold:
                        newPlat = Platform(app.randomLevel.width//app.randomLevel.tileSize, y - 1, platLength, tileSize)
                        app.randomLevel.platformList.append(newPlat)
            
            # item checks
            app.randomLevel.newItems()
            for item in app.randomLevel.itemList:
                collided = item.checkCollide(app.player)
                if collided:
                    app.randomLevel.itemList.remove(item)
                item.randomScroll(app)
            app.player.score = len(app.player.collected)
        
        # timer stopped
        elif app.timer != -1:
            app.randomEndScreen = True
            app.randomMode = False

def onMousePress(app, mouseX, mouseY):
    if app.randomMode and app.timerChoice == 0:
        if 650 <= mouseY <= 850:
            if 700 <= mouseX <= 820:
                app.timerChoice = 30
            elif 900 <= mouseX <= 1020:
                app.timerChoice = 60
            elif 1100 <= mouseX <= 1220:
                app.timerChoice = 120
        app.timer = app.stepsPerSecond * app.timerChoice

    elif app.startScreen:
        if 800 <= mouseX <= 1200:
            if 550 <= mouseY <= 650:
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
    
    elif app.endScreen or app.randomEndScreen:
        reset(app)

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
                    for item in app.level.items:
                        item.randomDashScroll(app)
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