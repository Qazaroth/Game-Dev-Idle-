from pathlib import Path
from data import Data
from datetime import datetime
from dateutil import parser
from os import listdir
from os.path import isfile, join

import os

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
            newGame()
        else:
            print("Data will be lost if you do not save!")
            toSave = input("(Y/N) Would you like to save? ")
            toSave = toSave.lower()

            if toSave in ["y", "n"]:
                if toSave == "y":
                    saveData = currGameData
                    fileName = "{}.saveDat".format(saveData.getDataID())
                    f = open("saves/{}".format(fileName), "w")
                    f.write(saveData.__str__())
                    f.close()
                    print("Data saved.")

def loadGame():
    print("Feature not implemented...")

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