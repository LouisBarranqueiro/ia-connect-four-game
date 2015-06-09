import os
from abc import ABCMeta, abstractmethod
import random


class ConnectFour(object):
    """ Connect Four game
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

        # cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])
        # init players with their "colors"
        self._players[0] = _HumanPlayer(self._colors[0])
        self._players[1] = _ComputerPlayer(self._colors[1])
        # display players's status
        for i in xrange(1):
            print('%s joue avec %s ' % (self._players[i]._type, self._colors[i]))

        # x always goes first
        self._current_player = self._players[0]
        # init grid with white spaces
        self._grid = []
        for i in xrange(self._GRID_HEIGHT):
            self._grid.append([])
            for j in xrange(self._GRID_WIDTH):
                self._grid[i].append(' ')

    def start(self):
        """ Start the game
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
        """ Handle the next move
        """
        # get the "move" (column) that the player played
        column = self._current_player.get_move(self._grid)
        # search the available line in the selected column
        for i in xrange(self._GRID_HEIGHT):
            if self._grid[i][column] == ' ':
                # set the color in the grid
                self._grid[i][column] = self._current_player._color
                self._check_status()
                self._print_state()
                # swith player
                self._switch_player()
                # increment the round
                self._round += 1
                return

        # column selected is full
        print("This column is full. Please choose an other column")
        return

    def _check_status(self):
        """ Check and update the status of the game
        """
        if self._is_full():
            self._finished = True
        elif self._is_connect_four():
            self._finished = True
            self._winner = self._current_player

    def _is_full(self):
        """
        Check if the grid is full
        :return: Boolean
        """
        # the number of round can't be superior to the number of case of the grid
        return self._round > self._GRID_WIDTH * self._GRID_HEIGHT

    def _is_connect_four(self):
        """
        Check if there is a connect four in the grid
        :return: Boolean
        """
        # for each piece in the grid...
        for i in xrange(self._GRID_HEIGHT):
            for j in xrange(self._GRID_WIDTH):
                if self._grid[i][j] != ' ':
                    # check for vertical connect four
                    if self._check_for_vertical_four(i, j):
                        return True

                    # check for horizontal connect four
                    if self._check_for_horizontal_four(i, j):
                        return True

                    # check for diagonal connect four
                    if self._check_for_diagonal_four(i, j):
                        return True

        return False

    def _check_for_vertical_four(self, row, col):
        """
        Check for vertical connect four starting at index [row][col] of the grid
        :param row: row of the grid
        :param col: column of the grid
        :return: Boolean
        """
        consecutive_count = 0

        if row + 3 < self._GRID_HEIGHT:
            # search a connect four
            for i in xrange(4):
                if self._grid[row][col].lower() == self._grid[row + i][col].lower():
                    consecutive_count += 1
                else:
                    break

            # define the winner
            if consecutive_count == 4:
                if self._players[0]._color.lower() == self._grid[row][col].lower():
                    self._winner = self._players[0]
                else:
                    self._winner = self._players[1]
                return True

        return False

    def _check_for_horizontal_four(self, row, col):
        """
        Check for horizontal connect four starting at index [row][col] of the grid
        :param row: row of the grid
        :param col: column of the grid
        :return: Boolean
        """
        consecutive_count = 0

        if col + 3 < self._GRID_WIDTH:
            # search a connect four
            for i in xrange(4):
                if self._grid[row][col].lower() == self._grid[row][col + i].lower():
                    consecutive_count += 1
                else:
                    break

            # define the winner
            if consecutive_count == 4:
                if self._players[0]._color.lower() == self._grid[row][col].lower():
                    self._winner = self._players[0]
                else:
                    self._winner = self._players[1]
                return True

        return False

    def _check_for_diagonal_four(self, row, col):
        """
        Check for diagonal connect four starting at index [row][col] of the grid
        :param row: row of the grid
        :param col: column of the grid
        :return: Boolean
        """
        consecutive_count = 0

        # check positive slope
        if row + 3 < self._GRID_HEIGHT and col + 3 < self._GRID_WIDTH:
            # search a connect four
            for i in xrange(4):
                if self._grid[row][col].lower() == self._grid[row + i][col + i].lower():
                    consecutive_count += 1
                else:
                    break

            # define the winner
            if consecutive_count == 4:
                if self._players[0]._color.lower() == self._grid[row][col].lower():
                    self._winner = self._players[0]
                else:
                    self._winner = self._players[1]
                return True

        # check negative slope
        if row - 3 >= 0 and col - 3 >= 0:
            # search a connect four
            for i in xrange(4):
                if self._grid[row][col].lower() == self._grid[row - i][col - i].lower():
                    consecutive_count += 1
                else:
                    break
            # define the winner
            if consecutive_count == 4:
                if self._players[0]._color.lower() == self._grid[row][col].lower():
                    self._winner = self._players[0]
                else:
                    self._winner = self._players[1]
                return True

        return False

    def _print_state(self):
        """ Print state of the game (round, grid, winner)
        """
        # cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])
        # print the round
        print("             Round: " + str(self._round))
        print("")
        # print the grid
        for i in xrange(self._GRID_HEIGHT, 0, -1):
            print("\t"),
            for j in xrange(self._GRID_WIDTH):
                print("| " + str(self._grid[i - 1][j])),
            print("|")
        print("\t"),
        # print the bottom of the grid with columns index
        for k in xrange(self._GRID_WIDTH):
            print("  _"),
        print("")
        print("\t"),
        for k in xrange(self._GRID_WIDTH):
            print("  %d" % (k + 1)),
        print("")
        # print final message when the game is finished
        if self._finished:
            print("Game Over!")
            if self._winner != None:
                print(str(self._winner._type) + " is the winner!")
            else:
                print("Game was a draw")


class _Player(object):
    """ Abstract Player class
    """

    __metaclass__ = ABCMeta

    _type = None
    _color = None

    def __init__(self, color):
        self._color = color

    @abstractmethod
    def get_move(self, grid):
        pass


class _HumanPlayer(_Player):
    """ Human Player
    """

    def __init__(self, color):
        """
        Constructor
        :param color: str represent the value entered in the grid for example: `o` or `x`
        """
        super(_HumanPlayer, self).__init__(color)
        self._type = "Human"

    def get_move(self, grid):
        """
        Ask and return the column entered by the user
        :param grid: list
        """
        column = None
        while column == None:
            try:
                column = int(raw_input("Your turn : ")) - 1
            except ValueError:
                column = None
            if 0 <= column <= 6:
                return column
            else:
                column = None
                print("Please, enter a number between 0 and 6")


class _ComputerPlayer(_Player):
    """ Computer Player controled by an IA (Minmax algorythm)
    """

    _DIFFICULTY = 5
    _board = None
    _colors = ["x", "o"]

    def __init__(self, color):
        """
        Constructor
        :param color: character entered in the grid for example: `o` or `x`
        :return:
        """
        super(_ComputerPlayer, self).__init__(color)
        self._type = "IA"

    def get_move(self, grid):
        """
        Return the best "move" (column index) calculated by IA
        :param grid: the current grid of the game
        :return best_move:
        """
        best_move, value = self._get_best_move(self._DIFFICULTY, grid, self._color)
        return best_move

    def _get_best_move(self, depth, state, curr_player):
        """ Returns the best "move" (column index) and the associated alpha
        """
        # determine opponent's color
        self._board = [x[:] for x in state]

        if curr_player == self._colors[0]:
            opp_player = self._colors[1]
        else:
            opp_player = self._colors[0]

        # enumerate all legal moves
        legal_moves = {}  # will map legal move states to their alpha values
        for col in xrange(7):
            # if column i is a legal move...
            if self._is_legal_move(col, state):
                # make the move in column 'col' for curr_player
                temp = self._make_move(state, col, curr_player)
                legal_moves[col] = -self._search(depth - 1, temp, opp_player)

        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(moves)
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move, best_alpha

    def _search(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever
            called this search

            Returns the alpha value
        """
        # enumerate all legal moves from this state
        legal_moves = []
        for i in xrange(7):
            # if column i is a legal move...
            if self._is_legal_move(i, state):
                # make the move in column i for curr_player
                temp = self._make_move(state, i, curr_player)
                legal_moves.append(temp)

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self._game_is_over(state):
            # return the heuristic value of node
            return self._eval(state, curr_player)

        # determine opponent's color
        if curr_player == self._colors[0]:
            opp_player = self._colors[1]
        else:
            opp_player = self._colors[0]

        alpha = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self._search(depth - 1, child, opp_player))
        return alpha

    def _is_legal_move(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """
        for i in xrange(6):
            if state[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True

        # if we get here, the column is full
        return False

    def _game_is_over(self, state):
        if self._check_streak(state, self._colors[0], 4) >= 1:
            return True
        elif self._check_streak(state, self._colors[1], 4) >= 1:
            return True
        else:
            return False

    def _make_move(self, state, column, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'

            Returns a copy of new state array with the added move
        """

        temp = [x[:] for x in state]
        for i in xrange(6):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    def _eval(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 +
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if color == self._colors[0]:
            o_color = self._colors[1]
        else:
            o_color = self._colors[0]

        my_fours = self._check_streak(state, color, 4)
        my_threes = self._check_streak(state, color, 3)
        my_twos = self._check_streak(state, color, 2)
        opp_fours = self._check_streak(state, o_color, 4)
        # opp_threes = self._check_streak(state, o_color, 3)
        # opp_twos = self._check_streak(state, o_color, 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours * 100000 + my_threes * 100 + my_twos

    def _check_streak(self, state, color, streak):
        count = 0
        # for each piece in the board...
        for i in xrange(6):
            for j in xrange(7):
                # ...that is of the color we're looking for...
                if state[i][j].lower() == color.lower():
                    # check if a vertical streak starts at (i, j)
                    count += self._check_vertical_streak(i, j, state, streak)

                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self._check_horizontal_streak(i, j, state, streak)

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += self._check_diagonal_streak(i, j, state, streak)
        # return the sum of streaks of length 'streak'
        return count

    def _check_vertical_streak(self, row, col, state, streak):
        consecutive_count = 0
        for i in xrange(row, 6):
            if state[i][col].lower() == state[row][col].lower():
                consecutive_count += 1
            else:
                break

        if consecutive_count >= streak:
            return 1
        else:
            return 0

    def _check_horizontal_streak(self, row, col, state, streak):
        consecutive_count = 0
        for j in xrange(col, 7):
            if state[row][j].lower() == state[row][col].lower():
                consecutive_count += 1
            else:
                break

        if consecutive_count >= streak:
            return 1
        else:
            return 0

    def _check_diagonal_streak(self, row, col, state, streak):

        total = 0
        # check for diagonals with positive slope
        consecutive_count = 0
        j = col
        for i in xrange(row, 6):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutive_count += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutive_count >= streak:
            total += 1

        # check for diagonals with negative slope
        consecutive_count = 0
        j = col
        for i in xrange(row, -1, -1):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutive_count += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutive_count >= streak:
            total += 1

        return total
