from cmu_graphics import *
from player import *
from PIL import Image

class Camera:
    def __init__(self, app, x, y, left, right):
        self.x, self.y = x, y
        self.cameraLeft = left
        self.cameraRight = right
        self.width = app.level.width