import subprocess, sys

try:
    from InquirerPy import inquirer
except ModuleNotFoundError:
    subprocess.run(["pip install inquirerpy"])
    sys.exit(0)

from pathlib import Path
from data import Data
from games import Games

from datetime import datetime
from dateutil import parser

from utils import clear, printProgressBar

from os import listdir
from os.path import isfile, join
import os

import time, threading, shelve

saveFolder = os.getcwd() + "/saves"
dbFile = saveFolder + "/database.db"

db = shelve.open(dbFile, "c")
gameData = []

try:
    gameData = db["GameData"]
except:
    db["GameData"] = gameData
finally:
    Data.dataCount = len(gameData)
    print(Data.dataCount)
    db.close()

exitGame = False

baseDevCost = 100
devCost = baseDevCost
devCostMulti = 1.5 # 1.5 * baseDevCost * noOfDevs (0) [Lowest = 1]
cashPerGame = 10
cashPerMin = 5
rebirthMulti = 1.0


savePath = Path(saveFolder)
if not savePath.exists():
    Path(saveFolder).mkdir(parents=True, exist_ok=True)

saveFiles = [f for f in listdir(saveFolder) if isfile(join(saveFolder, f))]
Data.dataCount = len(saveFiles)

separator = "=" * 47
saveSeparator = "||"
title = "Game Dev Idle"
newGameTitle = "New Game"

currGameData : Data = None

def doNothing():
    print("Doing nothing...")

    newGame()

def developAGame():
    items = list(range(0, 100))
    l = len(items)
    progressBarPrefix = " Game Development Progress:"
    gameName = inquirer.text(
        message="What do you want the name of your game to be?"
    ).execute()
    #print(gameName)
    g = Games(gameName)

    #print(l)
    printProgressBar(0, l, progressBarPrefix, "Complete", length=50)
    for i, item in enumerate(items):
        time.sleep(0.1)
        printProgressBar(i + 1, l, progressBarPrefix, "Complete", length=50)
    currGameData.addGame(g)

    newGame()
    #print("Feature not implemented yet...")

def hireDev():
    print("Feature not implemented yet...")

actions = {
    "0": ["Do nothing", doNothing],
    "1": ["Develop a game", developAGame],
    "2": ["Hire developer", hireDev]
}

def newGame():
    global currGameData, gameData

    db = shelve.open(dbFile, "r")
    try:
        gameData = db["GameData"]
    except:
        gameData = []
    finally:
        Data.dataCount = len(gameData)
        db.close()

    clear()
    print(separator)
    if currGameData is None:
        length = int(len(separator)/2-len(newGameTitle)/2)
        print("{}{}".format(" "*length, newGameTitle))
    else:
        length = int(len(separator)/2-len(title)/2)
        print("{}{}".format(" "*length, title))
    print(separator)
    if currGameData is None:
        playerName = inquirer.text(
                message="What is your player name?"
        ).execute()
        companyName = inquirer.text(
                message="What is your company name?"
        ).execute()
        currGameData = Data(playerName, companyName)
    
    print("Player Name: {}".format(currGameData.getPlayerName()))
    print("Company Name: {}".format(currGameData.getCompanyName()))
    print("Cash: ${}".format(currGameData.getCash()))
    print(separator)
    print("Number of Games Developed: {}".format(currGameData.getNumberOfGamesMade()))
    print("Number of Developers Hired: {}".format(currGameData.getNumberOfDevsHired()))
    print(separator)

    continueQn = input("(Y/N) Continue playing? ")
    continueQn = continueQn.lower()

    if continueQn in ["y", "n"]:
        if continueQn == "y":
            print(separator)
            for key in actions:
                value = actions[key]
                label = value[0]

                print("{} - {}".format(key, label))
                #print(key, value)

            actionChoice = inquirer.text(
                message="(Numbers only) What do you want to do?"
            ).execute()
            
            try:
                actionChoice = int(actionChoice)
            except:
                actionChoice = 0
            
            actionData = actions.get(str(actionChoice), None)

            if actionData is not None:
                action = actionData[1]

                action()
            else:
                print("Action #{} has either not been properly implemented or it's invalid.".format(actionChoice))
        else:
            print("Data will be lost if you do not save!")
            toSave = input("(Y/N) Would you like to save? ")
            toSave = toSave.lower()

            if toSave in ["y", "n"]:
                if toSave == "y":
                    saveData = currGameData
                    saveData.updateModifiedDate()

                    db = shelve.open(dbFile, "w")
                    try:
                        gameData = db["GameData"]
                    except:
                        gameData = []
                    finally:
                        print("Data Count: {}".format(Data.dataCount))
                        print("Save Data ID: {}".format(saveData.getDataID()))

                        try:
                            gameData[saveData.getDataID()] = saveData
                        except:
                            gameData.append(saveData)
                        
                        db["GameData"] = gameData
                        db.close()

                    print("Data saved.")

            currGameData = None

def loadGame():
    global currGameData, gameData

    db = shelve.open(dbFile, "r")
    try:
        gameData = db["GameData"]
    except:
        gameData = []
    finally:
        db.close()

    Data.dataCount = len(gameData)
    
    if len(gameData) > 0:
        print("Format: \"Save #Number - Player Name [Company Name]\"")
        for tempData in gameData:
            print("Save #{} - {} [{}]".format(
                gameData.index(tempData), 
                tempData.getPlayerName(), 
                tempData.getCompanyName()
            ))

        saveChoice = input("(Number only) Which save would you like to choose? ")

        try:
            saveChoice = int(saveChoice)
        except:
            saveChoice = -1

        if saveChoice >= 0 and saveChoice < len(gameData):
            saveFile = gameData[saveChoice] or None
            print("Attempting to load Save #{}...".format(saveChoice))
            if saveFile is not None:
                saveData = gameData[saveChoice] or None
                currGameData = saveData

                Data.dataCount = len(gameData)

                print("Successfully loaded Save #{}".format(saveChoice))
                time.sleep(1.5)
                newGame()
            else:
                print("Unable to load Save #{}!!! Possibly a corrupted save?".format(saveChoice))
        else:
            print("Invalid save file chosen.")
    else:
        print("No save file available.")
    #print("Feature not fully implemented...")

def mainLoop():
    global exitGame

    while not exitGame:
        print(separator)
        length = int(len(separator)/2-len(title)/2)
        print("{}{}".format(" "*length, title))
        print(separator)
        print("1 - New game")
        print("2 - Load game")
        print("3 - Exit")
        choice = input("(Numbers only) What do you want to do? ")

        try:
            choice = int(choice)
        except:
            choice = 3

        if choice in [1,2,3]:
            if choice == 1:
                newGame()
            elif choice == 2:
                loadGame()
            else:
                print("Exiting...")
                exitGame = True
        else:
            print("Invalid choice")

def bgLoop():
    global exitGame

    maxTime = 30
    timeSleep = 1.0

    while not exitGame:
        if exitGame:
            break
        
        for i in range(maxTime):
            if exitGame:
                break

            time.sleep(timeSleep)

            if i >= maxTime - 1 and currGameData is not None:
                noOfGames = currGameData.getNumberOfGamesMade()
                cash = currGameData.getCash()

                cashGained = (noOfGames * cashPerGame) + cashPerMin
                newCash = cash + cashGained
                
                print("Gained ${}!".format(cashGained))
                currGameData.setCash(newCash)

threads = []

mainThread = threading.Thread(target=mainLoop)
bgThread = threading.Thread(target=bgLoop)

threads.append(mainThread)
threads.append(bgThread)

for t in threads:
    t.start()

for t in threads:
    t.join()
