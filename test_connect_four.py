import unittest
from connect_four import *


class TestConnectFour(unittest.TestCase):
    """ Tests ConnectFour class
    """
    def setUp(self):
        self.connect_four = ConnectFour()

    def test_check_vertical_four(self):
        """ Check if vertical connect four is detected
        """
        grid = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['x', ' ', ' ', ' ', ' ', ' ', ' '],
            ['x', ' ', ' ', ' ', ' ', ' ', ' '],
            ['x', ' ', ' ', ' ', ' ', ' ', ' '],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ']
        ]
        self.connect_four._grid = grid
        self.assertEqual(self.connect_four._is_connect_four(), True)

    def test_check_horizontal_four(self):
        """ Check if horizontal connect four is detected
        """
        grid = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['x', 'x', 'x', 'x', ' ', ' ', ' ']
        ]
        self.connect_four._grid = grid
        self.assertEqual(self.connect_four._is_connect_four(), True)

    def test_check_diagonal_positive_four(self):
        """ Check if diagonal (positive slope) connect four is detected
        """
        grid = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'x', ' ', ' ', ' '],
            [' ', ' ', 'x', ' ', ' ', ' ', ' '],
            [' ', 'x', ' ', ' ', ' ', ' ', ' '],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ']
        ]
        self.connect_four._grid = grid
        self.assertEqual(self.connect_four._is_connect_four(), True)

    def test_check_diagonal_negative_four(self):
        """ Check if diagonal (negative slope) connect four is detected
        """
        grid = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'x', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'x', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'x', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'x']
        ]
        self.connect_four._grid = grid
        self.assertEqual(self.connect_four._is_connect_four(), True)

    def test_is_full(self):
        """ Check if the game detects that the grid is full
        """
        self.connect_four._round = CONNECT_FOUR_GRID_WIDTH * CONNECT_FOUR_GRID_HEIGHT + 1
        self.assertEqual(self.connect_four._is_full(), True)


class TestComputerPlayer(unittest.TestCase):
    """ Test ComputerPlayer class
    """

    def setUp(self):
        """ Start a new connect four
        """
        self.connect_four = ConnectFour()

    def test_check_vertical_four(self):
        """ Check if vertical connect four is detected by the computer player (IA)
        """
        grid = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['x', ' ', ' ', ' ', ' ', ' ', ' '],
            ['x', ' ', ' ', ' ', ' ', ' ', ' '],
            ['x', ' ', ' ', ' ', ' ', ' ', ' '],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ']
        ]
        self.assertEqual(self.connect_four._players[1]._find_streak(grid, "x", 4), 1)

    def test_check_horizontal_four(self):
        """ Check if horizontal connect four is detected by the computer player (IA)
        """
        grid = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['x', 'x', 'x', 'x', ' ', ' ', ' ']
        ]
        self.assertEqual(self.connect_four._players[1]._find_streak(grid, "x", 4), 1)

    def test_check_diagonal_positive_four(self):
        """ Check if diagonal (positive slope) connect four is detected by the computer player (IA)
        """
        grid = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'x', ' ', ' ', ' '],
            [' ', ' ', 'x', ' ', ' ', ' ', ' '],
            [' ', 'x', ' ', ' ', ' ', ' ', ' '],
            ['x', ' ', ' ', ' ', ' ', ' ', ' ']
        ]
        self.assertEqual(self.connect_four._players[1]._find_streak(grid, "x", 4), 1)

    def test_check_diagonal_negative_four(self):
        """ Check if diagonal (negative slope) connect four is detected by the computer player (IA)
        """
        grid = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'x', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'x', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'x', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'x']
        ]
        self.assertEqual(self.connect_four._players[1]._find_streak(grid, "x", 4), 1)

    def test_ia_intelligence_1(self):
        """ Check if IA wants to win (attack)
        """

        grid = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'o', 'x', ' ', ' ', ' '],
            [' ', 'o', 'x', 'x', ' ', ' ', ' '],
            [' ', 'o', 'x', 'x', ' ', ' ', ' '],
            [' ', 'o', 'x', 'o', 'x', ' ', 'o']
        ]
        self.assertEqual(self.connect_four._players[1].get_move(grid), 1)

    def test_ia_intelligence_2(self):
        """ Check if IA take the right choice (defense)
        """
        grid = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'o', ' ', ' ', ' ', ' '],
            [' ', 'x', 'x', 'x', ' ', ' ', ' '],
            [' ', 'o', 'x', 'x', ' ', ' ', 'o'],
            [' ', 'o', 'x', 'o', 'x', ' ', 'o']
        ]
        self.assertEqual(self.connect_four._players[1].get_move(grid), 1)


if __name__ == '__main__':
    unittest.main()
