import subprocess, sys

try:
    from InquirerPy import inquirer
except ModuleNotFoundError:
    subprocess.run(["pip install inquirerpy"])
    sys.exit(0)

from pathlib import Path
from data import Data

from datetime import datetime
from dateutil import parser

from os import listdir
from os.path import isfile, join
import os

import time

baseDevCost = 100
devCost = baseDevCost
devCostMulti = 1.5 # 1.5 * baseDevCost * noOfDevs (0) [Lowest = 1]
cashPerGame = 10
cashPerMin = 5
rebirthMulti = 1.0
saveFolder = os.getcwd() + "\saves"

savePath = Path(saveFolder)
if not savePath.exists():
    Path(saveFolder).mkdir(parents=True, exist_ok=True)

saveFiles = [f for f in listdir(saveFolder) if isfile(join(saveFolder, f))]
Data.dataCount = len(saveFiles)

separator = "=" * 47
saveSeparator = "||"
title = "Game Dev Idle"
newGameTitle = "New Game"

currGameData = None

def clear():
    command = "clear"
    if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
        command = "cls"

    os.system(command)

def printProgressBar(iteration, total, prefix="", suffix="", decimals=1, length=100, fill = "█", printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print("\r{} |{}| {}% {}".format(prefix, bar, percent, suffix), end=printEnd)
    if iteration == total:
        print()

def doNothing():
    print("Doing nothing...")

def developAGame():
    items = list(range(0, 100))
    l = len(items)
    progressBarPrefix = " Game Development Progress:"
    gameName = inquirer.text(
        message="What do you want the name of your game to be?"
    ).execute()
    print(gameName)

    printProgressBar(0, l, progressBarPrefix, "Complete", length=50)
    for i, item in enumerate(items):
        time.sleep(0.1)
        printProgressBar(i + 1, l, progressBarPrefix, "Complete", length=50)
    #print("Feature not implemented yet...")

def hireDev():
    print("Feature not implemented yet...")

actions = {
    "0": doNothing,
    "1": developAGame,
    "2": hireDev
}

def newGame():
    global currGameData
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
        playerName = input("What is your player name? ")
        companyName = input("What is your company name? ")
        currGameData = Data(playerName, companyName)
    
    print("Player Name: {}".format(currGameData.getPlayerName()))
    print("Company Name: {}".format(currGameData.getCompanyName()))
    print("Number of Games Developed: {}".format(currGameData.getNumberOfGamesMade()))
    print("Number of Developers Hired: {}".format(currGameData.getNumberOfDevsHired()))

    continueQn = input("(Y/N) Continue playing? ")
    continueQn = continueQn.lower()

    if continueQn in ["y", "n"]:
        if continueQn == "y":
            print(separator)
            print("0 - Do nothing")
            print("1 - Develop a game")
            print("2 - Hire more developers")
            actionChoice = inquirer.text(
                message="(Numbers only) What do you want to do?"
            ).execute()
            
            try:
                actionChoice = int(actionChoice)
            except:
                actionChoice = 0
            
            action = actions.get(str(actionChoice))

            if action is not None:
                action()
            else:
                print("Action #{} has either not been properly implemented or it's invalid.".format(actionChoice))
            # newGame()
        else:
            print("Data will be lost if you do not save!")
            toSave = input("(Y/N) Would you like to save? ")
            toSave = toSave.lower()

            if toSave in ["y", "n"]:
                if toSave == "y":
                    saveData = currGameData
                    saveData.updateModifiedDate()
                    fileName = "{}.saveDat".format(saveData.getDataID())
                    f = open("saves/{}".format(fileName), "w")
                    f.write(saveData.__str__())
                    f.close()
                    print("Data saved.")

def loadGame():
    global currGameData

    saveFiles = [f for f in listdir(saveFolder) if isfile(join(saveFolder, f))]
    savesData = []
    print("Format: \"Save #Number - Player Name [Company Name]\"")
    for f in saveFiles:
        tempData = Data()
        tempData.setDataID(saveFiles.index(f)+1)
        tempData.importFromFile("{}/{}".format(saveFolder, f))
        savesData.append(tempData)
        print("Save #{} - {} [{}]".format(saveFiles.index(f), tempData.getPlayerName(), tempData.getCompanyName()))

    saveChoice = input("(Number only) Which save would you like to choose? ")

    try:
        saveChoice = int(saveChoice)
    except:
        saveChoice = -1

    if saveChoice >= 0 and saveChoice < len(saveFiles):
        saveFile = saveFiles[saveChoice] or None
        print("Attempting to load Save #{}...".format(saveChoice))
        if saveFile is not None:
            saveData = savesData[saveChoice] or None
            currGameData = saveData
            print("Successfully loaded Save #{}".format(saveChoice))
            time.sleep(1.5)
            newGame()
        else:
            print("Unable to load Save #{}!!! Possibly a corrupted save?".format(saveChoice))
    else:
        print("Invalid save file chosen.")

    #print("Feature not fully implemented...")

def main():
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
            exit(0)
    else:
        print("Invalid choice")

main()