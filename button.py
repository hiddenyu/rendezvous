# Simple button demo
# mdtaylor 4/18

from cmu_graphics import *
import time

#---Button class-------------------------------------
class Button:
    def __init__(self, x, y, r, fun):
        # You'll probably want some more / different parameters
        self.x = x
        self.y = y
        self.r = r
        self.fun = fun #<--- This is a function!

    def draw(self):
        # This button looks like garbage
        drawCircle(self.x, self.y, self.r, fill = 'green')

    def checkForPress(self, app, mX, mY):
        # Might want to change this if you want a non-circular button
        if ((mX - self.x)**2 + (mY-self.y)**2)**0.5 <= self.r:
            self.fun(app)


#---Button functions---------------------------------
def myButtonFunction(app):
    print(f'The time is: {time.time()}')

def myOtherButtonFunction(app):
    print(">>( o  u  o )<<")

#---Animation functions---------------------------------
def onAppStart(app):
    app.myButton = Button(100, 200, 50, myButtonFunction)
    app.myOtherButton = Button(200, 100, 50, myOtherButtonFunction)

def onMousePress(app, mouseX, mouseY):
    app.myButton.checkForPress(app, mouseX, mouseY)
    app.myOtherButton.checkForPress(app, mouseX, mouseY)

def redrawAll(app):
    app.myButton.draw()
    app.myOtherButton.draw()

runApp(width = 400, height = 400)