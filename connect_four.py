import os
from minmax import Minmax
from players import *


class ConnectFour(object):
    """ Game object that holds state of Connect 4 grid and game values
    """
    _GRID_WIDTH = 7
    _GRID_HEIGHT = 6
    _grid = None
    _round = None
    _finished = False
    _winner = None
    _current_player = None
    _players = [None, None]
    _colors = ["x", "o"]

    def __init__(self):
        self._round = 1
        self._finished = False
        self._winner = None

        # do cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])
        # init players with their `colors`
        self._players[0] = HumanPlayer(self._colors[0])
        self._players[1] = ComputerPlayer(self._colors[1])
        # display players's status
        for i in xrange(0, 1):
            print("%s joue avec %s", self._players[i].type, self._colors[i])

        # x always goes first (arbitrary choice on my part)
        self._current_player = self._players[0]
        # init grid with white spaces
        self._grid = []
        for i in xrange(self._GRID_HEIGHT):
            self._grid.append([])
            for j in xrange(self._GRID_WIDTH):
                self._grid[i].append(' ')

    def start(self):
        """ Start a connect four
        """
        while not self._finished:
            self._next_move()

    def _switch_player(self):
        """ Switch the current player
        """
        if self._current_player == self._players[0]:
            self._current_player = self._players[1]
        else:
            self._current_player = self._players[0]

    def _next_move(self):
        # move is the column that player want's to play
        column = self._current_player.move(self._grid)

        for i in xrange(self._GRID_HEIGHT):
            if self._grid[i][column] == ' ':
                # Set the color in the grid
                self._grid[i][column] = self._current_player.color
                self._check_state()
                self._print_state()
                # swith player
                self._switch_player()
                # increment the round
                self._round += 1
                return

        # column selected is full
        print("Cette colonne est pleine. Veuillez selectionner une autre colonne.")
        return

    def _check_state(self):
        if self._is_full():
            self._finished = True
        elif self.is_connect_four():
            self._finished = True
            self._winner = self._current_player

    def _is_full(self):
        """ check if the grid is full
        """
        return self._round > 42

    def is_connect_four(self):
        # for each piece in the grid...
        for i in xrange(self._GRID_HEIGHT):
            for j in xrange(self._GRID_WIDTH):
                if self._grid[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self._check_for_vertical_four(i, j):
                        return True

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self._check_for_horizontal_four(i, j):
                        return True

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    if self._check_for_diagonal_four(i, j):
                        return True

        return False

    def _check_for_vertical_four(self, row, col):
        consecutive_count = 0

        if row + 3 < self._GRID_HEIGHT:
            for i in xrange(4):
                print("check vert")
                if self._grid[row][col].lower() == self._grid[row + i][col].lower():
                    consecutive_count += 1
                else:
                    break

            if consecutive_count == 4:
                if self._players[0].color.lower() == self._grid[row][col].lower():
                    self._winner = self._players[0]
                else:
                    self._winner = self._players[1]
                return True

        return False

    def _check_for_horizontal_four(self, row, col):
        consecutive_count = 0

        if col + 3 < self._GRID_WIDTH:
            for i in xrange(4):
                print("check hor")
                if self._grid[row][col].lower() == self._grid[row][col + i].lower():
                    consecutive_count += 1
                else:
                    break

            if consecutive_count == 4:
                if self._players[0].color.lower() == self._grid[row][col].lower():
                    self._winner = self._players[0]
                else:
                    self._winner = self._players[1]
                return True

        return False

    def _check_for_diagonal_four(self, row, col):
        consecutive_count = 0

        # check positive slope
        if row + 3 < self._GRID_HEIGHT and col + 3 < self._GRID_WIDTH:
            for i in xrange(4):
                if self._grid[row][col].lower() == self._grid[row + i][col + i].lower():
                    consecutive_count += 1
                else:
                    break

            if consecutive_count == 4:
                if self._players[0].color.lower() == self._grid[row][col].lower():
                    self._winner = self._players[0]
                else:
                    self._winner = self._players[1]
                return True

        # check negative slope
        if row - 3 >= 0 and col - 3 >= 0:
            for i in xrange(4):
                if self._grid[row][col].lower() == self._grid[row - i][col - i].lower():
                    consecutive_count += 1
                else:
                    break

            if consecutive_count == 4:
                if self._players[0].color.lower() == self._grid[row][col].lower():
                    self._winner = self._players[0]
                else:
                    self._winner = self._players[1]
                return True

        return False

    def _print_state(self):
        # cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])
        print("Round: " + str(self._round))

        for i in xrange(self._GRID_HEIGHT - 2, -1, -1):
            print("\t"),
            for j in xrange(self._GRID_WIDTH):
                print("| " + str(self._grid[i][j])),
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self._finished:
            print("Game Over!")
            if self._winner != None:
                print(str(self._winner.type) + " is the winner")
            else:
                print("Game was a draw")
