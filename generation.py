from cmu_graphics import *
import random, math

def onAppStart(app):
    app.width, app.height = 1920, 1080
    app.chunk = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    length = random.randint(2, 5)
    app.xLo, app.yLo, app.platLength = None, None, None
    generatePlatform(app, app.chunk, 0, 5, 7, len(app.chunk) - 1, length)

def generatePlatform(app, tileMap, xLo, xHigh, yLo, yHigh, length):
    x = random.randint(max(xLo, 0), min(xHigh, len(app.chunk[0]) - length))
    y = random.randint(max(yLo, 0), min(yHigh, len(app.chunk) - 1))
    index = random.randint(1, 5)
    for i in range(length):
        tileMap[y][x + i] = index
    app.xLo, app.yLo, app.platLength = x, y, length

# for weights, generate num from 0 to 1 and then have a weight dict where you reassign values
# like dict could be 0 - 0.5 is red, 0.5 to 0.75 is green, and 0.75 to 1 is blue
# so red has higher weight value

def nextPlatform(app, tileMap, x, y, dx, dy):
    length = random.randint(2, 5)
    generatePlatform(app, tileMap, x-dx, x+dx, y-dy, y+dy, length)

def redrawAll(app):
    rows, cols = len(app.chunk), len(app.chunk[0])
    tileSize = app.width / len(app.chunk[0])
    colors = {0: None,
              1: 'red',
              2: 'blue',
              3: 'green',
              4: 'yellow',
              5: 'pink'}

    for row in range(rows):
        for col in range(cols):
            drawRect(col*tileSize, row*tileSize, tileSize, tileSize, 
                     fill=colors[app.chunk[row][col]])

def onKeyPress(app, key):
    if key == 'space':
        nextPlatform(app, app.chunk, app.xLo, app.yLo, 5, 2)

def main():
    runApp()

main()