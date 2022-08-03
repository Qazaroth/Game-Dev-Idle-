from datetime import datetime
from dateutil import parser
from pathlib import Path

from games import Games

class Data:
    dataCount = 0

    def __init__(self, playerName="", companyName="", cash : float=0.0, gamesMade=[], noOfDevsHired=0, firstCreationDate=datetime.now(), lastModifiedDate=datetime.now()) -> None:
        self.__id = Data.dataCount
        self.__plrName = playerName
        self.__companyName = companyName
        self.__cash : float = cash
        self.__gamesMade = gamesMade
        self.__noOfDevs = noOfDevsHired
        self.__firstCreated = firstCreationDate
        self.__lastModified = lastModifiedDate

        Data.dataCount += 1

    def getDataID(self):
        return self.__id

    def getPlayerName(self):
        return self.__plrName

    def getCompanyName(self):
        return self.__companyName

    def getCash(self) -> float:
        return self.__cash

    def getNumberOfGamesMade(self):
        return len(self.__gamesMade)

    def getNumberOfDevsHired(self):
        return self.__noOfDevs

    def getFirstCreationDate(self):
        return self.__firstCreated

    def getLastModifiedDate(self):
        return self.__lastModified

    def setDataID(self, id):
        self.__id = id

    def setPlayerName(self, playerName):
        self.__plrName = playerName

    def setCompanyName(self, companyName):
        self.__companyName = companyName

    def setCash(self, cash : float):
        self.__cash = cash

    def addGame(self, game : Games):
        self.__gamesMade.append(game)

    def setNumberOfDevsHired(self, noOfDevsHired):
        self.__noOfDevs = noOfDevsHired

    def updateModifiedDate(self):
        self.__lastModified = datetime.now()

    def importFromFile(self, file):
        f = Path(file)

        if f.exists():
            f = open(file, "r")
            fileData = f.read()
            f.close()

            fileDataList = fileData.split("||")
            
            self.__plrName = fileDataList[0]
            self.__companyName = fileDataList[1]
            self.__cash = float(fileDataList[2])
            self.__noOfGames = int(fileDataList[3])
            self.__noOfDevs = int(fileDataList[4])
            self.__firstCreated = parser.parse(fileDataList[5])
            self.__lastModified = datetime.now()

    def __repr__(self) -> str:
        return "{}||{}||{}||{}||{}||{}||{}".format(
            self.__plrName, 
            self.__companyName, 
            self.__cash,
            self.__noOfGames,
            self.__noOfDevs,
            self.__firstCreated,
            self.__lastModified)