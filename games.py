class Games():
    gamesCount = 0

    def __init__(self, name) -> None:
        self.__id = Games.gamesCount + 1
        self.__name = name

        Games.gamesCount += 1

    def getID(self):
        return self.__id

    def setID(self, id):
        self.__id = id

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name