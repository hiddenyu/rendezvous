import random, math

# 1 dimensional perlin noise
# concepts from https://www.scratchapixel.com/lessons/procedural-generation-virtual-worlds/procedural-patterns-noise-part-1/creating-simple-1D-noise.html
# also read from https://www.cs.umd.edu/class/spring2018/cmsc425/Lects/lect12-1d-perlin.pdf
# and https://adrianb.io/2014/08/09/perlinnoise.html

# for weights, generate num from 0 to 1 and then have a weight dict where you reassign values
# like dict could be 0 - 0.5 is red, 0.5 to 0.75 is green, and 0.75 to 1 is blue
# so red has higher weight value

def randomNoise(seed, xVals):
    random.seed(seed)
    d = dict()
    for i in range(xVals):
        d[i] = random.random()
    return d

def lerp(a, b, t):
    return a * (1 - t) + b * t

# fade function from ken perlin
def fade(a, b, t):
    if 0 <= t <= 1:
        t = 6 * t**5 - 15 * t**4 + 10 * t**3
    ans = lerp(a, b, t)
    return ans

def eval(noise, xVals, x):
    x0 = int(x) % xVals
    if x0 == xVals - 1:
        x1 = 0
    else:
        x1 = x0 + 1
    t = x % xVals - x0
    ans = fade(noise[x0], noise[x1], t)
    return ans