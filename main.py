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
# - tutorial! 

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
    app.tutorial = False
    app.randomTutorial = False

    app.randomMode = False
    app.randomEndScreen = False

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
    app.dashAlert = False
    app.alertSeconds = 3
    app.dashAlertTimer = app.stepsPerSecond * app.alertSeconds
    app.dJumpAlert = False
    app.dJumpAlertTimer = app.stepsPerSecond * app.alertSeconds

    # level constants
    app.tileMaps = Tilemaps()
    level0 = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\level0.png"
    app.level = Level(app.tileMaps.tileMap0, level0)
    app.tileSize = app.level.tileSize

    # camera constants
    app.cameraLeft = 600
    app.cameraRight = app.level.width - app.width - app.cameraLeft
    app.camera = Camera(app, 0, 0, app.cameraLeft, app.cameraRight)

    # player constants
    app.playerRespawn = [100, 900]
    app.player = Player(100, 900)

    # graphics
    app.title = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\title.png"
    app.tutorialText = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\instructions.png"
    app.tutorialText2 = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\instructions2.png"

def redrawAll(app):
    ### story mode ###
    if app.gameScreen:
        app.level.draw(app)
        for item in app.level.items:
            item.draw()
        app.player.draw()

        if app.tutorial:
            drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
            drawRect(960, 540, 500, 500, align='center', fill=rgb(118, 158, 131))
            drawImage(app.tutorialText, 960, 540, width=600, height=600, align='center')

        if app.dashAlert and app.dashAlertTimer > 0:
            drawLabel('You gained dash! Press E to dash!', app.player.x + app.player.width/2, app.player.y - 75, size=15)
        if app.dJumpAlert and app.dJumpAlertTimer > 0:
            drawLabel('You gained double-jump! Press space twice to double jump', app.player.x + app.player.width/2, app.player.y - 75, size=15)

    ### random mode ###
    elif app.randomMode:
        if app.timerChoice == -1:
            drawLabel('Choose a time limit', 960, 500, size=75)
            drawLabel('30', 760, 750, size=50)
            drawLabel('60', 960, 750, size=50)
            drawLabel('120', 1160, 750, size=50)
        else:
            app.randomLevel.draw()
            app.player.draw()
            drawLabel(f'{app.timer // app.stepsPerSecond}', 100, 100, size=50)
            drawLabel(f'Collected: {app.player.score}', 1500, 100, size=50)
            if app.randomTutorial:
                drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
                drawRect(960, 540, 500, 500, align='center', fill=rgb(118, 158, 131))
                drawImage(app.tutorialText2, 960, 540, width=600, height=600, align='center')

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
        drawRect(0, 0, app.width, app.height, fill=rgb(118, 158, 131))
        drawImage(app.title, 960, 450, width=4723/10, height=631/10, align='center')
        drawLabel('start', 960, 600, size=50)
        drawLabel('random mode', 960, 750, size=50)

def onStep(app):
    ### story mode ###
    if app.gameScreen:
        if not app.tutorial:
            app.player.onGround = app.player.doStep(app, app.level)
            app.cameraDelta = app.camera.scroll(app.level, app.player)
            
            # item checks
            for item in app.level.items:
                item.checkCollide(app.player)
                app.player.giveAbilities()
                item.scroll(app)
            
            if app.player.completed:
                app.gameScreen = False
                app.endScreen = True
        if app.dashAlert and app.dashAlertTimer > 0:
            app.dashAlertTimer -= 1
        if app.dJumpAlert and app.dJumpAlertTimer > 0:
            app.dJumpAlertTimer -= 1

    ### random mode ###
    elif app.randomMode:
        # timer is running
        if app.timer > 0 and not app.randomTutorial:
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
        elif app.timer <= 0 and app.timer != -1:
            app.randomEndScreen = True
            app.randomMode = False

def onMousePress(app, mouseX, mouseY):
    if app.randomMode and app.timerChoice == -1:
        if 650 <= mouseY <= 850:
            if 700 <= mouseX <= 820:
                app.timerChoice = 30
                app.timer = app.stepsPerSecond * app.timerChoice
            elif 900 <= mouseX <= 1020:
                app.timerChoice = 60
                app.timer = app.stepsPerSecond * app.timerChoice
            elif 1100 <= mouseX <= 1220:
                app.timerChoice = 120
                app.timer = app.stepsPerSecond * app.timerChoice

    elif app.startScreen:
        if 800 <= mouseX <= 1200:
            if 550 <= mouseY <= 650:
                # story mode chosen
                app.gameScreen = True
                app.startScreen = False
                app.tutorial = True
                app.player.abilities = set()

            elif 700 <= mouseY <= 800:
                # random mode chosen
                app.randomMode = True
                app.startScreen = False
                app.randomTutorial = True

                # random level constants
                app.randomLevel = RandomLevel()
                app.timerChoice = -1
                app.timer = -1
                app.player.abilities = {'dash', 'double jump'}

    elif app.endScreen or app.randomEndScreen:
        reset(app)

def onKeyPress(app, key):
    if app.tutorial or app.randomTutorial:
        if key == 'space':
            app.tutorial = False
            app.randomTutorial = False

    if app.gameScreen or app.randomMode:
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

                elif app.randomMode:
                    for platform in app.randomLevel.platformList:
                        app.camera.randomDashScroll(platform, app.player)
                    for item in app.randomLevel.itemList:
                        app.randCameraDelta = app.camera.randomDashScroll(item, app.player)
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