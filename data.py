from datetime import datetime

class Data:
    dataCount = 0

    def __init__(self, playerName, companyName, cash : float=0.0, noOfGamesMade=0, noOfDevsHired=0, firstCreationDate=datetime.now(), lastModifiedDate=datetime.now()) -> None:
        self.__id = Data.dataCount + 1
        self.__plrName = playerName
        self.__companyName = companyName
        self.__cash : float = cash
        self.__noOfGames = noOfGamesMade
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
        return self.__noOfGames

    def getNumberOfDevsHired(self):
        return self.__noOfDevs

    def getFirstCreationDate(self):
        return self.__firstCreated

    def getLastModifiedDate(self):
        return self.__lastModified

    def setPlayerName(self, playerName):
        self.__plrName = playerName

    def setCompanyName(self, companyName):
        self.__companyName = companyName

    def setCash(self, cash : float):
        self.__cash = cash

    def setNumberOfGamesMade(self, noOfGamesMade):
        self.__noOfGames = noOfGamesMade

    def setNumberOfDevsHired(self, noOfDevsHired):
        self.__noOfDevs = noOfDevsHired

    def updateModifiedDate(self):
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