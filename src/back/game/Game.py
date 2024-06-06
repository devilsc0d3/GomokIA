import numpy as np


class Game:
    def __init__(self):
        array = np.arange(19 * 19)
        game_content = np.zeros_like(array).reshape(19, 19)
        self.__game = game_content

    def get_game(self):
        return self.__game

    def analyze_game(self):
        pass

    def horizontal(self):

        # self.__game[0,1:6] = 1
        for i in range(19):
            for j in range(15):
                if self.__game[i][j] == 1 and self.__game[i][j+1] == 1 and self.__game[i][j+2] == 1 and self.__game[i][j+3] == 1 and self.__game[i][j+4] == 1:
                    return 1
                elif self.__game[i][j] == 2 and self.__game[i][j+1] == 2 and self.__game[i][j+2] == 2 and self.__game[i][j+3] == 2 and self.__game[i][j+4] == 2:
                    return 2
        return 0


game = Game()
print(game.horizontal())
print(game.get_game())
