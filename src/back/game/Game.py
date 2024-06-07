import numpy as np


class Game:
    def __init__(self):
        self.__game = np.zeros((15, 15))  # init the matrix
        self.__player = 1
        self.__name_of_player = "JD"
        self.__current_game = True
        self.__filename = "game.csv"
        self.initialize_csv()

    def get_game(self):
        return self.__game

    def set_game(self, x, y):
        self.__game[x][y] = self.__player

    def analyze_game(self):
        vertical = self.column()  # vertical check
        horizontal = self.row()  # horizontal check
        diagonal = self.diagonal()  # diagonal check

        if vertical == 1 or horizontal == 1 or diagonal == 1:
            print("Player 1 wins")
            exit()
        elif vertical == 2 or horizontal == 2 or diagonal == 2:
            print("Player 2 wins")
            exit()
        else:
            return 0

    def row(self):
        for i in range(self.__game.shape[0]):  # column
            for j in range(self.__game.shape[1] - 4):  # row
                if np.all(self.__game[i, j:j + 5] == 1):
                    return 1  # player 1 won
                elif np.all(self.__game[i, j:j + 5] == 2):
                    return 2  # player 2 won
        return 0  # no one won

    def column(self):
        for i in range(self.__game.shape[1]):  # row
            for j in range(self.__game.shape[0] - 4):  # column
                if np.all(self.__game[i, j:j + 5] == 1):
                    return 1  # player 1 won
                elif np.all(self.__game[i, j:j + 5] == 2):
                    return 2  # player 2 won
        return 0  # no one won

    def diagonal(self):
        for i in range(11):
            for j in range(11):
                if self.__game[i][j] == 1 and self.__game[i + 1][j + 1] == 1 and self.__game[i + 2][j + 2] == 1 and \
                        self.__game[i + 3][j + 3] == 1 and self.__game[i + 4][j + 4] == 1:
                    return 1
                elif self.__game[i][j] == 2 and self.__game[i + 1][j + 1] == 2 and self.__game[i + 2][j + 2] == 2 and \
                        self.__game[i + 3][j + 3] == 2 and self.__game[i + 4][j + 4] == 2:
                    return 2
        for i in range(11):
            for j in range(11):
                if self.__game[i][j] == 1 and self.__game[i + 1][j - 1] == 1 and self.__game[i + 2][j - 2] == 1 and \
                        self.__game[i + 3][j - 3] == 1 and self.__game[i + 4][j - 4] == 1:
                    return 1
                elif self.__game[i][j] == 2 and self.__game[i + 1][j - 1] == 2 and self.__game[i + 2][j - 2] == 2 and \
                        self.__game[i + 3][j - 3] == 2 and self.__game[i + 4][j - 4] == 2:
                    return 2
        return 0

    def play(self):
        print("Player " + str(self.__player) + " turn")
        try:
            x = int(input("Enter the position to play x: "))
            y = int(input("Enter the position to play y: "))

            if x < 0 or x >= 15 or y < 0 or y >= 15:
                print("Invalid position! x and y must be between 0 and 18. Try again.")
                self.play()
        except ValueError:
            exit()

        # si le joueur a déjà joué
        if self.get_game()[x][y] != 0:
            print("already played, try again")
            self.play()
        else:
            self.set_game(x, y)

        print(self.get_game())

        self.export_game_to_csv()
        self.analyze_game()

        self.__player = 2 if self.__player == 1 else 1
        self.play()

    # export en csv apres chaque tour
    def initialize_csv(self):
        open(self.__filename, 'w').close()

    def export_game_to_csv(self):
        with open(self.__filename, 'a') as f:
            np.savetxt(f, self.__game, delimiter=",", fmt='%d')
            f.write("\n")
