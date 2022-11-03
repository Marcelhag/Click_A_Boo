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
        self.notUsedDistance: int       = args[6]
        self.size: int                  = args[7]
        self.participant: string        = key
        self.window = None
        self.running = False
        self.lastClick = Point(self.windowWidth/2,self.windowHeight/2)
        self.startTime = None
        self.timeSinceLastClick = None
        self.timeSinceLastCorrect = None
        self.circles = []
        self.data = []
        self.waitingTime = 0
        self.entries: Entry = []
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
        for i in range(self.amount):
            self.createCirc()
            self.circles[-1].draw()
            while not self.checkMousePos():
                self.window.checkKey
                print(self.window.lastKey)
            self.circles[-1].delete()
        print(self.entries)
        for entry in self.entries:
            data = [entry.isMistake, entry.size, entry.distanceToLastCircle, entry.distanceToLastClick, entry.distanceClickToCenter, entry.distanceClickToCircle, entry.duration,
              entry.id, entry.ip, entry.ipIfNoMistake]
            self.data.append(data)
        return self.data

    def createCirc(self):
        size = self.size
        x = self.lastClick.x
        y = self.lastClick.y
        while self.calculateDistance(x, y, self.lastClick.x, self.lastClick.y) < self.size*2:
            x = random.randint(size, self.window.width-size)
            y = random.randint(size + self.notUsedDistance, self.window.height-size)
        circEnt = CircleEntity(x, y, size, self)
        self.circles.append(circEnt)

    def checkMousePos(self):
        pos = self.window.checkMouse()
        if not pos or pos == self.lastClick:
            return False
        curTime = time.time()
        x = pos.x
        y = pos.y
        distanceClickToCenter = self.calculateDistance(x, y, self.circles[-1].x, self.circles[-1].y)
        duration = curTime - self.timeSinceLastClick
        distanceToLastCircle = 0
        distanceToLastClick = 0
        if len(self.entries) > 0:
            distanceToLastCircle = self.calculateDistance(self.entries[-1].circle.x, self.entries[-1].circle.y, self.circles[-1].x, self.circles[-1].y)
            distanceToLastClick = self.calculateDistance(self.entries[-1].clickPosition.x, self.entries[-1].clickPosition.y, self.circles[-1].x, self.circles[-1].y)
        else:
            distanceToLastCircle = self.calculateDistance(math.floor(self.windowWidth/2), math.floor(self.windowHeight/2), self.circles[-1].x, self.circles[-1].y)
            distanceToLastClick = distanceToLastCircle
        entry = Entry(self.circles[-1], distanceToLastCircle, distanceToLastClick, distanceClickToCenter, duration, pos)
        self.entries.append(entry)
        self.lastClick = pos
        self.timeSinceLastClick = curTime
        return True
    
    def calculateDistance(self, x1, y1, x2, y2):
        deltaX = abs(x2 - x1)
        deltaY = abs(y2 - y1)
        return math.sqrt(pow(deltaX,2) + pow(deltaY,2))


class Mistake:
    def __init__(self, distance, size, duration):
        self.distance = distance
        self.size = size
        self.distanceToCenter = distance + size
        self.duration = duration

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

class Entry:
    def __init__(self, circle: CircleEntity, distanceToLastCircle, distanceToLastClick, distanceClickToCenter, duration, clickPosition):
        self.circle: CircleEntity = circle
        self.distanceToLastCircle = distanceToLastCircle
        self.distanceToLastClick = distanceToLastClick
        self.distanceClickToCenter = distanceClickToCenter
        self.size = circle.size
        self.distanceClickToCircle = max(self.distanceClickToCenter - self.size, 0)
        self.isMistake = True if self.distanceClickToCircle > 0 else False
        self.duration = duration
        self.clickPosition = clickPosition
        self.id = math.log2(4 * self.distanceToLastClick / self.size) if self.size != 0 and self.distanceToLastClick != 0 else 0
        self.ip = self.id / (self.duration * (self.distanceClickToCircle +1)) if self.duration != 0 else 0
        self.ipIfNoMistake = None if self.isMistake else self.ip