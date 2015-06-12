import os
import random
import time
from abc import ABCMeta, abstractmethod

CONNECT_FOUR_GRID_WIDTH = 7
CONNECT_FOUR_GRID_HEIGHT = 6
CONNECT_FOUR_COLORS = ["x", "o"]


class ConnectFour(object):
    """ Connect Four game
    """
    _GRID_WIDTH = CONNECT_FOUR_GRID_WIDTH
    _GRID_HEIGHT = CONNECT_FOUR_GRID_HEIGHT
    _grid = None
    _round = None
    _finished = False
    _winner = None
    _current_player = None
    _players = [None, None]
    _COLORS = CONNECT_FOUR_COLORS

    def __init__(self):
        self._round = 1
        self._finished = False
        self._winner = None

        # cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])
        # init players with their "colors"
        self._players[0] = _HumanPlayer(self._COLORS[0])
        self._players[1] = _ComputerPlayer(self._COLORS[1])
        # display players's status
        for i in xrange(2):
            print('%s play with %s ' % (self._players[i]._type, self._COLORS[i]))

        # choose the first player randomly
        self._current_player = self._players[random.randint(0, 1)]
        # init grid with white spaces
        self._grid = []
        for i in xrange(self._GRID_HEIGHT):
            self._grid.append([])
            for j in xrange(self._GRID_WIDTH):
                self._grid[i].append(' ')

    def start(self):
        """ Start a game
        """
        while not self._finished:
            self._next_move()

    def start_new(self):
        """ Start a new game
        """
        # cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])
        # reset game status
        self._round = 1
        self._finished = False
        self._winner = None
        # choose the first player randomly
        self._current_player = self._players[random.randint(0, 1)]
        # clear grid with white spaces
        self._grid = []
        for i in xrange(self._GRID_HEIGHT):
            self._grid.append([])
            for j in xrange(self._GRID_WIDTH):
                self._grid[i].append(' ')

        # start a new game
        self.start()

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
        for i in xrange(self._GRID_HEIGHT - 1, -1, -1):
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
        # for each box of the grid
        for i in xrange(self._GRID_HEIGHT - 1, -1, -1):
            for j in xrange(self._GRID_WIDTH):
                if self._grid[i][j] != ' ':
                    # check for vertical connect four
                    if self._find_vertical_four(i, j):
                        return True

                    # check for horizontal connect four
                    if self._find_horizontal_four(i, j):
                        return True

                    # check for diagonal connect four
                    if self._find_diagonal_four(i, j):
                        return True

        return False

    def _find_vertical_four(self, row, col):
        """
        Check for vertical connect four starting at index [row][col] of the grid
        :param row: row of the grid
        :param col: column of the grid
        :return: Boolean
        """
        consecutive_count = 0

        if row + 3 < self._GRID_HEIGHT:
            for i in xrange(4):
                if self._grid[row][col] == self._grid[row + i][col]:
                    consecutive_count += 1
                else:
                    break

            # define the winner
            if consecutive_count == 4:
                if self._players[0]._color == self._grid[row][col]:
                    self._winner = self._players[0]
                else:
                    self._winner = self._players[1]
                return True

        return False

    def _find_horizontal_four(self, row, col):
        """
        Check for horizontal connect four starting at index [row][col] of the grid
        :param row: row of the grid
        :param col: column of the grid
        :return: Boolean
        """
        consecutive_count = 0

        if col + 3 < self._GRID_WIDTH:
            for i in xrange(4):
                if self._grid[row][col] == self._grid[row][col + i]:
                    consecutive_count += 1
                else:
                    break

            # define the winner
            if consecutive_count == 4:
                if self._players[0]._color == self._grid[row][col]:
                    self._winner = self._players[0]
                else:
                    self._winner = self._players[1]
                return True

        return False

    def _find_diagonal_four(self, row, col):
        """
        Check for diagonal connect four starting at index [row][col] of the grid
        :param row: row of the grid
        :param col: column of the grid
        :return: Boolean
        """
        consecutive_count = 0
        # check positive slope
        if row + 3 < self._GRID_HEIGHT and col + 3 < self._GRID_WIDTH:
            for i in xrange(4):
                if self._grid[row][col] == self._grid[row + i][col + i]:
                    consecutive_count += 1
                else:
                    break

            # define the winner
            if consecutive_count == 4:
                if self._players[0]._color == self._grid[row][col]:
                    self._winner = self._players[0]
                else:
                    self._winner = self._players[1]
                return True

        consecutive_count = 0
        # check negative slope
        if row - 3 >= 0 and col + 3 < self._GRID_WIDTH:
            for i in xrange(4):
                if self._grid[row][col] == self._grid[row - i][col + i]:
                    consecutive_count += 1
                else:
                    break

            # define the winner
            if consecutive_count == 4:
                if self._players[0]._color == self._grid[row][col]:
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
        for i in xrange(self._GRID_HEIGHT):
            print("\t"),
            for j in xrange(self._GRID_WIDTH):
                print("| " + str(self._grid[i][j])),
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
                print("Game is a draw")


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
        :param color: character entered in the grid for example: `o` or `x`
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
                print("Please, enter a number between 1 and 7")


class _ComputerPlayer(_Player):
    """ Computer Player controlled by an IA (MinMax algorithm)
    """
    _DIFFICULTY = 5

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
        Returns the best "move" (column index) calculated by IA
        :param grid: the current grid of the game
        :return: the best move found by IA (MinMax algorithm)
        """
        return self._get_best_move(grid)

    def _get_best_move(self, grid):
        """
        Search and return the best "move" (column index)
        :param grid: the grid of the connect four
        :return best_move: the best "move" (column index)
        """
        # start time
        start_time = int(round(time.time() * 1000))
        # determine opponent's color
        if self._color == CONNECT_FOUR_COLORS[0]:
            human_color = CONNECT_FOUR_COLORS[1]
        else:
            human_color = CONNECT_FOUR_COLORS[0]

        # enumerate all legal moves
        # will map legal move states to their alpha values
        legal_moves = {}
        # check if the move is legal for each column
        for col in xrange(CONNECT_FOUR_GRID_WIDTH):
            if self._is_legal_move(col, grid):
                # simulate the move in column `col` for the current player
                tmp_grid = self._simulate_move(grid, col, self._color)
                legal_moves[col] = -self._find(self._DIFFICULTY - 1, tmp_grid, human_color)

        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        # search the best "move" with the highest `alpha` value
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        end_time = int(round(time.time() * 1000))
        print "response time: %d" % (end_time - start_time)

        return best_move

    def _find(self, depth, grid, curr_player_color):
        """
        Searches in the tree at depth = `depth` till it's not equal to 0. This function is recursive
        :param depth: the current depth of the tree
        :param grid: a grid of the connect four
        :param curr_player_color: the color of the current player
        :return alpha: value calculated with an heuristic. It represent the value of a "move" (column index)
        """
        # enumerate all legal moves from this state
        legal_moves = []
        for i in xrange(CONNECT_FOUR_GRID_HEIGHT):
            if self._is_legal_move(i, grid):
                # simulate the move in column i for curr_player
                tmp_grid = self._simulate_move(grid, i, curr_player_color)
                legal_moves.append(tmp_grid)

        if depth == 0 or len(legal_moves) == 0 or self._game_is_over(grid):
            # return the heuristic value of node
            return self._eval_game(depth, grid, curr_player_color)

        # determine opponent's color
        if curr_player_color == CONNECT_FOUR_COLORS[0]:
            opp_player_color = CONNECT_FOUR_COLORS[1]
        else:
            opp_player_color = CONNECT_FOUR_COLORS[0]

        alpha = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self._find(depth - 1, child, opp_player_color))
        return alpha

    def _is_legal_move(self, column, grid):
        """ Boolean function to check if a move (column) is a legal move
        """
        for i in xrange(CONNECT_FOUR_GRID_HEIGHT - 1, -1, -1):
            if grid[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True

        # if we get here, the column is full
        return False

    def _game_is_over(self, grid):
        if self._find_streak(grid, CONNECT_FOUR_COLORS[0], 4) > 0:
            return True
        elif self._find_streak(grid, CONNECT_FOUR_COLORS[1], 4) > 0:
            return True
        else:
            return False

    def _simulate_move(self, grid, column, color):
        """
        Simulate a "move" in the grid `grid` by the current player with its color `color.
        :param grid: a grid of connect four
        :param column: column index
        :param color: color of a player
        :return tmp_grid: the new grid with the "move" just added
        """
        tmp_grid = [x[:] for x in grid]
        for i in xrange(CONNECT_FOUR_GRID_HEIGHT - 1, -1, -1):
            if tmp_grid[i][column] == ' ':
                tmp_grid[i][column] = color
                return tmp_grid

    def _eval_game(self, depth, grid, player_color):
        """
        Evaluate the game with its grid
        :param depth: the depth of the tree
        :param grid: a grid of connect four
        :param player_color: the current player's color
        :return: alpha : value calculated with an heuristic. It represent the value of a "move" (column index)
        """
        if player_color == CONNECT_FOUR_COLORS[0]:
            opp_color = CONNECT_FOUR_COLORS[1]
        else:
            opp_color = CONNECT_FOUR_COLORS[0]
        # get scores of human and IA player with theirs streaks
        ia_fours = self._find_streak(grid, player_color, 4)
        ia_threes = self._find_streak(grid, player_color, 3)
        ia_twos = self._find_streak(grid, player_color, 2)
        human_fours = self._find_streak(grid, opp_color, 4)
        human_threes = self._find_streak(grid, opp_color, 3)
        human_twos = self._find_streak(grid, opp_color, 2)
        # calculate and return the alpha
        if human_fours > 0:
            return -100000 - depth
        else:
            return (ia_fours * 100000 + ia_threes * 100 + ia_twos * 10) - (human_threes * 100 + human_twos * 10) + depth

    def _find_streak(self, grid, color, streak):
        """
        Search streaks of a color in the grid
        :param grid: a grid of connect four
        :param color: color of a player
        :param streak: number of consecutive "color"
        :return count: number of streaks founded
        """
        count = 0
        # for each box in the grid...
        for i in xrange(CONNECT_FOUR_GRID_HEIGHT):
            for j in xrange(CONNECT_FOUR_GRID_WIDTH):
                # ...that is of the color we're looking for...
                if grid[i][j] == color:
                    # check if a vertical streak starts at index [i][j] of the grid game
                    count += self._find_vertical_streak(i, j, grid, streak)

                    # check if a horizontal streak starts at index [i][j] of the grid game
                    count += self._find_horizontal_streak(i, j, grid, streak)

                    # check if a diagonal streak starts at index [i][j] of the grid game
                    count += self._find_diagonal_streak(i, j, grid, streak)
        # return the sum of streaks of length 'streak'

        return count

    def _find_vertical_streak(self, row, col, grid, streak):
        """
        Search vertical streak starting at index [row][col] in the grid
        :param row: row the grid
        :param col: column of the grid
        :param grid: a grid of connect four
        :param streak: number of "color" consecutive
        :return: 0: no streak found, 1: streak founded
        """
        consecutive_count = 0
        if row + streak - 1 < CONNECT_FOUR_GRID_HEIGHT:
            for i in xrange(streak):
                if grid[row][col] == grid[row + i][col]:
                    consecutive_count += 1
                else:
                    break

        if consecutive_count == streak:
            return 1
        else:
            return 0

    def _find_horizontal_streak(self, row, col, grid, streak):
        """
        Search horizontal streak starting at index [row][col] in the grid
        :param row: row the grid
        :param col: column of the grid
        :param grid: a grid of connect four
        :param streak: number of "color" consecutive
        :return: 0: no streak found, 1: streak founded
        """
        consecutive_count = 0
        if col + streak - 1 < CONNECT_FOUR_GRID_WIDTH:
            for i in xrange(streak):
                if grid[row][col] == grid[row][col + i]:
                    consecutive_count += 1
                else:
                    break

        if consecutive_count == streak:
            return 1
        else:
            return 0

    def _find_diagonal_streak(self, row, col, grid, streak):
        """
        Search diagonal streak starting at index [row][col] in the grid
        It check positive and negative slope
        :param row: row the grid
        :param col: column of the grid
        :param grid: a grid of connect four
        :param streak: number of "color" consecutive
        :return total: number of streaks founded
        """
        total = 0
        # check for diagonals with positive slope
        consecutive_count = 0
        if row + streak - 1 < CONNECT_FOUR_GRID_HEIGHT and col + streak - 1 < CONNECT_FOUR_GRID_WIDTH:
            for i in xrange(streak):
                if grid[row][col] == grid[row + i][col + i]:
                    consecutive_count += 1
                else:
                    break

        if consecutive_count == streak:
            total += 1

        # check for diagonals with negative slope
        consecutive_count = 0
        if row - streak + 1 >= 0 and col + streak - 1 < CONNECT_FOUR_GRID_WIDTH:
            for i in xrange(streak):
                if grid[row][col] == grid[row - i][col + i]:
                    consecutive_count += 1
                else:
                    break

        if consecutive_count == streak:
            total += 1

        return total
