#!/usr/bin/env python3
import sys
import subprocess
import os
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'pandas'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'openpyxl'])
import pandas as pd
from graphics import *
from game import Game

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def generateKey():
    day = input("Bitte gebe dein Geburtsdatum ein (DD.MM.YY): ")
    mother = input("Bitte gebe den Vornamen deiner Mutter an: ")
    father = input("Bitte gebe den Vornamen deines Vater an: ")
    place = input("Bitte gebe deinen Geburtsort ein: ")
    return (day[0:2] + mother[0] + father[-1] + place[0]).upper()

def getGamesArgs():
    gamesArgs = list()
    path= '.\\tests'
    for filename in os.listdir(path):
        gameArgs = list()
        path_data = [i.strip().split() for i in open(path + '\\' + filename).readlines()]
        amount = int(path_data[0][1])
        backgroundColor = path_data[1][1]
        circleColor = path_data[2][1]
        textColor = path_data[3][1]
        windowWidth = int(path_data[4][1])
        windowHeight = int(path_data[5][1])
        notUsedDistance = int(path_data[6][1])
        size = int(path_data[7][1])
        repeat = int(path_data[8][1])
        evaluate = int(path_data[9][1])
        gameArgs.append(amount)
        gameArgs.append(backgroundColor)
        gameArgs.append(circleColor)
        gameArgs.append(textColor)
        gameArgs.append(windowWidth)
        gameArgs.append(windowHeight)
        gameArgs.append(notUsedDistance)
        gameArgs.append(size)
        gamesArgs.append((gameArgs, repeat, filename, evaluate))
    return (gamesArgs)
        
def main():
    clearConsole()
    key = generateKey()
    gameArgs = getGamesArgs()
    window = GraphWin("Click-A-Boo", width=gameArgs[0][0][4], height=gameArgs[0][0][5])
    first = True
    for args in gameArgs:
        data = []
        G = Game(key, args[0])
        for i in range(args[1]):
            data = G.startGame(window, args[2][:-4], i, first)
            first = False
        if args[3] > 0:
            # df = pd.DataFrame(data, columns=['size', 'mistakes', 'duration'], dtype=float)
            df = pd.DataFrame(data, columns=['isMistake', 'size', 'distanceToLastCircle', 'distanceToLastClick', 'distanceClickToCenter', 'distanceClickToCircle', 'duration', 'id', 'ip','ipIfNoMistake'], dtype=float)
            df = df.round(2)
            if not os.path.exists('results\\' + G.participant):
                os.makedirs('results\\' + G.participant)
            with pd.ExcelWriter('results\\' + G.participant + '\\' + G.participant + '_' + args[2] + '.xlsx') as writer:  
                df.to_excel(writer, sheet_name='Values')
                df.describe().round(2).to_excel(writer, sheet_name='Statistics')
    window.close()


if __name__ == "__main__":
    main()