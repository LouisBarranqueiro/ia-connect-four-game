# ia-connect-four-game
Connect four game against IA player (MinMax algorithm) written in python for a small project in university

* **Author:** Louis Barranqueiro
* **Python:** v2.7.6

## Getting started

Get source code: `git clone https://github.com/LouisBarranqueiro/ia-connect-four.git`  
Run program: `python main.py`
  
## Documentation

### Tests

Tests written aimed to test computer player's intelligence and function used to detect four-in-row.
To run them : `python test_connect_four.py`

#### Heuristic

The heuristic used to evaluate a game state is : count of ia's four-in-row * 1000 + count of ia's three-in-row * 100 + count of ia's two-in-row * 10 - count of human's four-in-row * 1000 + count of human's three-in-row * 100 + count of human's two-in-row * 10 + current depth of tree.  
**python formula:** `(ia_fours * 100000 + ia_threes * 100 + ia_twos * 10) - (human_threes * 100 - human_twos * 10) + depth`

## License

ia-connect-four-game is released under the terms of the [MIT License](https://github.com/LouisBarranqueiro/ia-connect-four-game/blob/master/LICENSE)
