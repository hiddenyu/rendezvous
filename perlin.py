from cmu_graphics import *
import random, math

# concepts from https://www.scratchapixel.com/lessons/procedural-generation-virtual-worlds/procedural-patterns-noise-part-1/creating-simple-1D-noise.html
def randomNoise(xVals):
    random.seed(1437)
    d = dict()
    for i in range(xVals):
        d[i] = random.random()
    return d

def lerp(a, b, t):
    return a * (1 - t) + b * t

def eval(app, x):
    x0 = int(x) % app.xVals
    if x0 == app.xVals - 1:
        x1 = 0
    else:
        x1 = x0 + 1
    t = x%app.xVals - x0
    ans = fade(app.noise[x0], app.noise[x1], t)
    return ans

def fade(a, b, t):
    if 0 <= t <= 1:
        t = 6 * t**5 - 15 * t**4 + 10 * t**3
    ans = lerp(a, b, t)
    return ans

def onAppStart(app):
    app.xVals = 256
    app.noise = randomNoise(app.xVals)
    app.range = 40

    app.array = []
    for i in range(app.range):
        app.array.append(0)

    for i in range(app.range):
        app.array[i] = eval(app, i)

def redrawAll(app):
    for i in range(app.range):
        noiseFactor = app.array[i]
        if noiseFactor > 0:
            drawRect(i * 10, 200, 10, 100, fill=rgb(255*noiseFactor, 255*noiseFactor, 255*noiseFactor))

def main():
    runApp()

main()