import numpy as np


class Game:
    def __init__(self):
        array = np.arange(19 * 19)
        game_content = np.zeros_like(array).reshape(19, 19)
        self.__game = game_content
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
        vertical = self.vertical()
        horizontal = self.horizontal()
        diagonal = self.diagonal()

        if vertical == 1 or horizontal == 1 or diagonal == 1:
            print("Player 1 wins")
            exit()
        elif vertical == 2 or horizontal == 2 or diagonal == 2:
            print("Player 2 wins")
            exit()
        else:
            return 0

    def horizontal(self):
        # self.__game[0,1:6] = 1
        for i in range(19):
            for j in range(15):
                if self.__game[i][j] == 1 and self.__game[i][j + 1] == 1 and self.__game[i][j + 2] == 1 and \
                        self.__game[i][j + 3] == 1 and self.__game[i][j + 4] == 1:
                    return 1
                elif self.__game[i][j] == 2 and self.__game[i][j + 1] == 2 and self.__game[i][j + 2] == 2 and \
                        self.__game[i][j + 3] == 2 and self.__game[i][j + 4] == 2:
                    return 2
        return 0

    def vertical(self):
        # self.__game[0:5, 0] = 1
        for i in range(15):
            for j in range(19):
                if self.__game[i][j] == 1 and self.__game[i + 1][j] == 1 and self.__game[i + 2][j] == 1 and \
                        self.__game[i + 3][j] == 1 and self.__game[i + 4][j] == 1:
                    return 1
                elif self.__game[i][j] == 2 and self.__game[i + 1][j] == 2 and self.__game[i + 2][j] == 2 and \
                        self.__game[i + 3][j] == 2 and self.__game[i + 4][j] == 2:
                    return 2
        return 0

    def diagonal(self):
        for i in range(15):
            for j in range(15):
                if self.__game[i][j] == 1 and self.__game[i + 1][j + 1] == 1 and self.__game[i + 2][j + 2] == 1 and \
                        self.__game[i + 3][j + 3] == 1 and self.__game[i + 4][j + 4] == 1:
                    return 1
                elif self.__game[i][j] == 2 and self.__game[i + 1][j + 1] == 2 and self.__game[i + 2][j + 2] == 2 and \
                        self.__game[i + 3][j + 3] == 2 and self.__game[i + 4][j + 4] == 2:
                    return 2
        for i in range(15):
            for j in range(4, 19):
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

            if x < 0 or x >= 19 or y < 0 or y >= 19:
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
