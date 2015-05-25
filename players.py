from abc import ABCMeta, abstractmethod
from minmax import Minmax

class Player(object):
    """ Abstract Player class
    """
    __metaclass__ = ABCMeta

    type = None
    color = None

    def __init__(self, color):
        self.color = color

    @abstractmethod
    def move(self, state):
        pass

class HumanPlayer(Player):
    """ Human Player
    """
    def __init__(self, color):
        super(HumanPlayer, self).__init__(color)
        self.type = "Human"

    def move(self, state):
        #print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        column = None
        while column == None:
            try:
                column = int(raw_input("A vous de jouer : ")) - 1
            except ValueError:
                column = None
            if 0 <= column <= 6:
                return column
            else:
                column = None
                print("Veuillez entrer un chiffre entre 0 et 6")


class ComputerPlayer(Player):
    """ Computer Player controled by an IA (Minmax algorythm)
    """

    difficulty = None

    def __init__(self, color, difficulty = 5):
        super(ComputerPlayer, self).__init__(color)
        self.type = "AI"
        self.difficulty = difficulty

    def move(self, state):
        #print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        m = Minmax(state)
        best_move, value = m.bestMove(self.difficulty, state, self.color)
        return best_move
