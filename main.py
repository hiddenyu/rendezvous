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

# all graphics are drawn by me

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
    app.randomLevelBG = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\randomlevel.png"
    app.randomLevelBG = CMUImage(Image.open(app.randomLevelBG))

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
    app.sparkles = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\sparkle.png"
    app.sparkles = CMUImage(Image.open(app.sparkles))
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
    app.sprite = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\char.png"
    app.sprite = CMUImage(Image.open(app.sprite))
    app.spriteRun = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\charRun.png"
    app.spriteRun = CMUImage(Image.open(app.spriteRun))
    app.spriteRunLeft = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\charRunLeft.png"
    app.spriteRunLeft = CMUImage(Image.open(app.spriteRunLeft))
    app.spriteJump = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\charJump.png"
    app.spriteJump = CMUImage(Image.open(app.spriteJump))
    app.playerRespawn = [100, 900]
    app.player = Player(100, 900)

    # graphics
    app.titleScreen = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\titlescreen.png"
    app.titleScreen = CMUImage(Image.open(app.titleScreen))

    app.tutorialText = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\instructions.png"
    app.tutorialText = CMUImage(Image.open(app.tutorialText))

    app.tutorialText2 = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\instructions2.png"
    app.tutorialText2 = CMUImage(Image.open(app.tutorialText2))

    app.timeChoiceText = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\timechoice.png"
    app.timeChoiceText = CMUImage(Image.open(app.timeChoiceText))

    app.plat3 = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\plat3.png"
    app.plat3 = CMUImage(Image.open(app.plat3))

    app.plat4 = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\plat4.png"
    app.plat4 = CMUImage(Image.open(app.plat4))

    app.plat5 = r"C:\Users\wuyj1\Downloads\s23\15112\term project\graphics\plat5.png"
    app.plat5 = CMUImage(Image.open(app.plat5))

def redrawAll(app):
    ### story mode ###
    if app.gameScreen:
        app.level.draw(app)
        for item in app.level.items:
            item.draw()
        drawLabel(f'crystals found: {len(app.player.collected)} / 12', 1700, 100, 
                  font='BaksoSapi', fill=rgb(206, 223, 212), size=25)
        app.player.draw()

        if app.tutorial:
            drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
            drawRect(960, 540, 500, 500, align='center', fill=rgb(118, 158, 131))
            drawImage(app.tutorialText, 960, 540, width=600, height=600, align='center')

        if app.dashAlert and app.dashAlertTimer > 0:
            drawRect(app.player.x + app.player.width/2, app.player.y - 75, 400, 50, fill=rgb(118, 158, 131), align='center')
            drawLabel('You gained dash! Press E to dash!', app.player.x + app.player.width/2, 
                      app.player.y - 75, size=20, font='BaksoSapi', fill=rgb(206, 223, 212))
        if app.dJumpAlert and app.dJumpAlertTimer > 0:
            drawRect(app.player.x + app.player.width/2, app.player.y - 75, 700, 50, fill=rgb(118, 158, 131), align='center')
            drawLabel('You gained double jump! Press space twice to double jump', 
                      app.player.x + app.player.width/2, app.player.y - 75, size=20, font='BaksoSapi', fill=rgb(206, 223, 212))

    ### random mode ###
    elif app.randomMode:
        if app.timerChoice == -1:
            drawImage(app.timeChoiceText, 0, 0)
        else:
            app.randomLevel.draw()
            app.player.draw()
            drawLabel(f'{app.timer // app.stepsPerSecond}', 100, 100, size=50, font='BaksoSapi', fill='white')
            drawLabel(f'collected: {app.player.score}', 1700, 100, font='BaksoSapi', fill='white', size=50)
            if app.randomTutorial:
                drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
                drawRect(960, 540, 500, 500, align='center', fill=rgb(118, 158, 131))
                drawImage(app.tutorialText2, 960, 540, width=600, height=600, align='center')

    elif app.randomEndScreen:
        drawRect(0, 0, app.width, app.height, fill=rgb(118, 158, 131))
        drawLabel(f'you collected {app.player.score} crystals!', 960, 540, size=75, font='BaksoSapi', fill=rgb(206, 223, 212))
        drawLabel('click anywhere to restart', 960, 750, font='BaksoSapi', size=25, fill=rgb(206, 223, 212))

    ### end screen ###
    elif app.endScreen:
        drawRect(0, 0, app.width, app.height, fill=rgb(118, 158, 131))
        drawLabel('you reunited LOONA!', 960, 540, size=75, font='BaksoSapi', fill=rgb(206, 223, 212))
        drawLabel('click anywhere to restart', 960, 750, size=25, font='BaksoSapi', fill=rgb(206, 223, 212))

    ### start screen ###
    elif app.startScreen:
        drawImage(app.titleScreen, 0, 0)
        drawLabel('rendezvous', 960, 400, size=150, font='BaksoSapi', fill='white')
        drawLabel('story mode', 960, 650, size=50, font='BaksoSapi', fill=rgb(206, 223, 212))
        drawLabel('challenge mode', 960, 750, size=50, font='BaksoSapi', fill=rgb(206, 223, 212))

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
        if 660 <= mouseY <= 780:
            if 690 <= mouseX <= 810:
                app.timerChoice = 30
                app.timer = app.stepsPerSecond * app.timerChoice
            elif 900 <= mouseX <= 1020:
                app.timerChoice = 60
                app.timer = app.stepsPerSecond * app.timerChoice
            elif 1100 <= mouseX <= 1220:
                app.timerChoice = 90
                app.timer = app.stepsPerSecond * app.timerChoice

    elif app.startScreen:
        if 760 <= mouseX <= 1160:
            if 600 <= mouseY <= 700:
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