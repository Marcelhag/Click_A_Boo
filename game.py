import string
from graphics import *
import random
import pandas as pd
import math

class Game:
    def __init__(self, key, args: list):
        self.amount: int                = args[0]
        self.backgroundColor: string    = args[1]
        self.circleColor: string        = args[2]
        self.textColor: string          = args[3]
        self.windowWidth: int           = args[4]
        self.windowHeight: int          = args[5]
        self.notUsedDistance: int       = math.floor(self.windowWidth/args[6])
        self.size: int               = math.floor(self.windowWidth/args[7])
        self.participant: string        = key
        self.window = None
        self.running = False
        self.lastClick = None
        self.startTime = None
        self.timeSinceLastClick = None
        self.timeSinceLastCorrect = None
        self.circles = []
        self.data = []
        self.waitingTime = 0
        self.results: pd.DataFrame = None

    def startGame(self, window, testname, number, first):
        self.data = []
        self.window = window
        self.running = True
        self.window.setBackground(self.backgroundColor)
        if first:
            t = Text(Point(self.window.width/2,self.window.height/2), "Hello.\nThanks for participating.\nClick anywhere to start with test\n" + testname + '_' + str(number+1) + '.')
        else:
            t = Text(Point(self.window.width/2,self.window.height/2), "Click anywhere to start with test\n" + testname + '_' + str(number+1) + '.')
        t.setFill(self.textColor)
        t.draw(self.window)
        self.window.getMouse()
        t.undraw()
        self.window.setBackground('#000000')
        self.startTime = time.time()
        self.timeSinceLastClick = self.startTime
        self.timeSinceLastCorrect = self.startTime
        for i in range(self.amount):
            self.createCirc()
            self.circles[-1].draw()
            while not self.checkMousePos():
                self.window.checkKey
                print(self.window.lastKey)
            self.circles[-1].delete()
        for circle in self.circles:
            data = [circle.size, len(circle.mistake), circle.duration]
            self.data.append(data)
        self.results = pd.DataFrame(self.data, columns=['size', 'mistakes', 'duration'], dtype=float)
        return self.data

    def createCirc(self):
        self.timeSinceLastCorrect = time.time()
        # randTime = max(random.random() * self.maxTimeBetween, self.minTimeBetween)
        # self.waitingTime = randTime
        # time.sleep(randTime)
        size = self.size
        x = random.randint(size, self.window.width-size)
        y = random.randint(size + self.notUsedDistance, self.window.height-size)
        circEnt = CircleEntity(x, y, size, self)
        self.circles.append(circEnt)

    def checkMousePos(self):
        pos = self.window.checkMouse()
        if not pos or pos == self.lastClick:
            return False
        curTime = time.time()
        self.timeSinceLastClick = curTime
        x = pos.x
        y = pos.y
        deltaX = abs(self.circles[-1].x - x)
        deltaY = abs(self.circles[-1].y - y)
        distance = math.sqrt(pow(deltaX,2) + pow(deltaY,2))
        if distance <= self.circles[-1].size:
            self.circles[-1].duration = curTime - self.timeSinceLastCorrect - self.waitingTime
            self.timeSinceLastCorrect = curTime
            return True
        else:
            mistake = Mistake(distance, distance + self.circles[-1].size, curTime - self.timeSinceLastClick - self.waitingTime)
            self.circles[-1].mistake.append(mistake)
            return True

class Mistake:
    def __init__(self, distance, size, duration):
        self.distance = 0
        self.size = size
        self.distanceToCenter = distance + size
        self.duration = 0

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class CircleEntity (Entity):
    def __init__(self, x, y, size, game):
        super().__init__(x, y)
        self.duration = 0
        self.size = size
        self.mistake = []
        self.circ = Circle(Point(self.x, self.y), self.size)
        self.game = game
    
    def draw(self):
        self.circ.setFill(self.game.circleColor)
        self.circ.draw(self.game.window)

    def delete(self):
        self.circ.undraw()