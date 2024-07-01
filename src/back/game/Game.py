import numpy as np
import pandas as pd
import random
import csv
import matplotlib.pyplot as plt
import tkinter as tk
import os


class Game:
    def __init__(self):
        self.__game = np.zeros((15, 15), dtype=int)  # init the matrix
        self.__player = 1
        self.__current_game = True
        self.__filename = "game.csv"
        self.__game_id = self.get_next_game_id()  # Get the next game ID
        self.initialize_csv()

    def get_next_game_id(self):
        if not os.path.exists(self.__filename):
            return 1
        data = pd.read_csv(self.__filename)
        if data.empty:
            return 1
        return data['game_id'].max() + 1

    def get_game(self):
        return self.__game

    def set_game(self, x, y):
        self.__game[x][y] = self.__player
        self.export_move_to_csv(x, y)

    def analyze_game(self):
        vertical = self.column()  # vertical check
        horizontal = self.row()  # horizontal check
        diagonal = self.diagonal()  # diagonal check

        if vertical == 1 or horizontal == 1 or diagonal == 1:
            print("Player 1 wins")
            self.__current_game = False
            self.plot_statistics()  # Plot statistics after each game
            return 1
        elif vertical == 2 or horizontal == 2 or diagonal == 2:
            print("Player 2 wins")
            self.__current_game = False
            self.plot_statistics()  # Plot statistics after each game
            return 2
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
                if np.all(self.__game[j:j + 5, i] == 1):
                    return 1  # player 1 won
                elif np.all(self.__game[j:j + 5, i] == 2):
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
            for j in range(4, 15):
                if self.__game[i][j] == 1 and self.__game[i + 1][j - 1] == 1 and self.__game[i + 2][j - 2] == 1 and \
                        self.__game[i + 3][j - 3] == 1 and self.__game[i + 4][j - 4] == 1:
                    return 1
                elif self.__game[i][j] == 2 and self.__game[i + 1][j - 1] == 2 and self.__game[i + 2][j - 2] == 2 and \
                        self.__game[i + 3][j - 3] == 2 and self.__game[i + 4][j - 4] == 2:
                    return 2
        return 0

    def play(self):
        if not self.__current_game:
            return

        print("Player " + str(self.__player) + " turn")
        try:
            x = int(input("Enter the position to play x: "))
            y = int(input("Enter the position to play y: "))

            if x < 0 or x >= 15 or y < 0 or y >= 15:
                print("Invalid position! x et y must be between 0 et 14. Try again.")
                self.play()
        except ValueError:
            exit()

        # si le joueur a déjà joué
        if self.get_game()[x][y] != 0:
            print("Already played, try again")
            self.play()
        else:
            self.set_game(x, y)

        print(self.get_game())

        if self.analyze_game() == 0 and self.__current_game:
            self.__player = 2 if self.__player == 1 else 1
            if self.__player == 2:
                self.ia_play()
            self.play()

    def ia_play(self):
        try:
            data = pd.read_csv(self.__filename)
            empty_positions = np.argwhere(self.__game == 0)

            if len(empty_positions) > 0:
                if not data.empty:
                    winning_moves = data[data['player'] == 2]
                    move_counts = winning_moves.groupby(['x', 'y']).size()
                    if not move_counts.empty:
                        move_probabilities = move_counts / move_counts.sum()
                        move_choices = move_probabilities.sample(weights=move_probabilities.values).index.tolist()
                        x, y = move_choices[0]
                    else:
                        x, y = random.choice(empty_positions)
                else:
                    x, y = random.choice(empty_positions)

                self.set_game(x, y)
                print(f"IA played at position ({x}, {y})")
                self.analyze_game()
                self.__player = 1
        except pd.errors.EmptyDataError:
            print("No data available for the IA to learn from. Playing a random move.")
            empty_positions = np.argwhere(self.__game == 0)
            if len(empty_positions) > 0:
                x, y = random.choice(empty_positions)
                self.set_game(x, y)
                print(f"IA played at position ({x}, {y})")
                self.analyze_game()
                self.__player = 1

    # Initialiser le CSV
    def initialize_csv(self):
        if not os.path.exists(self.__filename):
            with open(self.__filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["game_id", "x", "y", "player"])

    # Exporter chaque coup dans le CSV
    def export_move_to_csv(self, x, y):
        with open(self.__filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.__game_id, x, y, self.__player])

    def plot_game(self):
        plt.imshow(self.__game, cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.show()

    def plot_statistics(self):
        data = pd.read_csv(self.__filename)
        if data.empty:
            return

        game_counts = data.groupby('game_id')['player'].count()
        game_counts.plot(kind='bar', color='blue')
        plt.title('Number of Moves per Game')
        plt.xlabel('Game ID')
        plt.ylabel('Number of Moves')
        plt.show()

    def to_dataframe(self):
        return pd.DataFrame(self.__game)


class GameGUI:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.canvas = tk.Canvas(master, width=600, height=600)
        self.canvas.pack()
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.click_event)

    def draw_grid(self):
        for i in range(15):
            for j in range(15):
                x0, y0 = i * 40, j * 40
                x1, y1 = x0 + 40, y0 + 40
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")

    def click_event(self, event):
        x, y = event.x // 40, event.y // 40
        if self.game.get_game()[x, y] == 0:
            self.game.set_game(x, y)
            self.draw_move(x, y, self.game._Game__player)
            if self.game.analyze_game() == 0:
                self.game._Game__player = 2 if self.game._Game__player == 1 else 1
                if self.game._Game__player == 2:
                    self.game.ia_play()
                    empty_positions = np.argwhere(self.game.get_game() == 0)
                    if len(empty_positions) > 0:
                        ia_move = random.choice(empty_positions)
                        self.draw_move(ia_move[0], ia_move[1], 2)
                    self.game._Game__player = 1

    def draw_move(self, x, y, player):
        color = "black" if player == 1 else "white"
        x0, y0 = x * 40, y * 40
        x1, y1 = x0 + 40, y0 + 40
        self.canvas.create_oval(x0, y0, x1, y1, fill=color)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game()
    app = GameGUI(root, game)
    root.mainloop()
