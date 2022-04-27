#!/usr/bin/env python3
import sys
import subprocess
import os
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'pandas'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'openpyxl'])
from graphics import *
import pandas as pd
import random
import math
import time

class Game:
    def __init__(self, username):

        # --- In here, you can change the values as you want them ---
        self.amount          = 10                                    # amount of circles that occur
        self.backgroundColor = '#000000'                            # background color
        self.circleColor     = 'red'                                # circle color
        self.textColor       = 'white'                              # text color
        self.minTimeBetween  = 1                                    # minimum time until next circle appears
        self.maxTimeBetween  = 3                                    # maximum time until next circle appears
        self.notUsedDistance = 40                                   # distance to the top, which is not used
        self.windowWidth     = 1200                                 # width of the window
        self.windowHeight    = math.floor(self.windowWidth/1.5)     # height of the window
        self.minSize         = math.floor(self.windowWidth/130)     # minimum size of the circles
        self.maxSize         = math.floor(self.windowWidth/65)      # maximum size if the circles
        # --- --------------------------------------------------- ---

        self.window = GraphWin("Click-A-Boo", width=self.windowWidth, height=self.windowHeight)
        self.running = True
        self.lastClick = None
        self.startTime = time.time()
        self.timeSinceLastClick = time.time()
        self.timeSinceLastCorrect = time.time()
        self.circles = []
        self.participant = username
        self.data = []
        self.removeOnMistake = True
        self.waitingTime = 0
    
    def createCirc(self):
        self.timeSinceLastCorrect = time.time()
        randTime = max(random.random() * self.maxTimeBetween, self.minTimeBetween)
        self.waitingTime = randTime
        time.sleep(randTime)
        # while time.time() < self.timeSinceLastCorrect + math.floor(randTime):
            # ...
        size = random.randint(self.minSize, self.maxSize)
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
            return not self.removeOnMistake

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

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
        
def main():
    clearConsole()
    username = input("Enter username: ")
    G = Game(username)
    G.participant = username
    G.window.setBackground(G.backgroundColor)
    t = Text(Point(G.window.width/2,G.window.height/2), "Hello " + G.participant + ".\nThanks for participating.\nClick anywhere to start.")
    t.setFill(G.textColor)
    t.draw(G.window)
    G.window.getMouse()
    t.undraw()
    G.startTime = time.time()
    G.timeSinceLastClick = G.startTime
    G.timeSinceLastCorrect = G.startTime
    for i in range(G.amount):
        G.createCirc()
        G.circles[-1].draw()
        while not G.checkMousePos():
            G.window.checkKey
            print(G.window.lastKey)
        G.circles[-1].delete()
    G.window.close()
    for circle in G.circles:
        data = [circle.size, len(circle.mistake), circle.duration]
        G.data.append(data)
    df = pd.DataFrame(G.data, columns=['size', 'mistakes', 'duration'], dtype=float)
    clearConsole()
    print('Data from user: ', G.participant)
    print('Values:\n', df, '\n')

    print('Statistics:\n', df.describe())
    with pd.ExcelWriter('results\\' + G.participant + '.xlsx') as writer:  
        df.to_excel(writer, sheet_name='Values')
        df.describe().to_excel(writer, sheet_name='Statistics')

    # with pd.ExcelWriter('results\\Values.xlsx') as writer:  
    #     df.to_excel(writer, sheet_name='Values')

    #values = pd.read_excel('results\\Values.xlsx', sheet_name='Values')
    #values.append(df)

    #with pd.ExcelWriter('results\\Values.xlsx') as writer:  
    #    df.to_excel(writer, sheet_name='Values')
        

if __name__ == "__main__":
    main()