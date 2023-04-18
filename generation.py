from cmu_graphics import *
import random, math

def onAppStart(app):
    app.width, app.height = 1920, 1080
    app.map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    generatePlatform(app.map)

def generatePlatform(tileMap):
    length = random.randint(2, 5)
    x = random.randint(0, len(tileMap[0]) - length)
    y = random.randint(0, len(tileMap) - 1)
    index = random.randint(1, 5)
    for i in range(length):
        tileMap[y][x + i] = index
    print(x, y, length)

# for weights, generate num from 0 to 1 and then have a weight dict where you reassign values
# like dict could be 0 - 0.5 is red, 0.5 to 0.75 is green, and 0.75 to 1 is blue
# so red has higher weight value

def redrawAll(app):
    rows, cols = len(app.map), len(app.map[0])
    tileSize = app.width / len(app.map[0])
    colors = {0: None,
              1: 'red',
              2: 'blue',
              3: 'green',
              4: 'yellow',
              5: 'pink'}

    for row in range(rows):
        for col in range(cols):
            drawRect(col*tileSize, row*tileSize, tileSize, tileSize, 
                     fill=colors[app.map[row][col]])

def main():
    runApp()

main()