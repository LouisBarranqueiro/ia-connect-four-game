# ia-connect-four
Connect four game with some IA (MinMax algorithm)

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

The heuristic used to evaluate a game state is :
`(ia_fours * 100000 + ia_threes * 100 + ia_twos * 10 + depth) - (human_threes * 100 - human_twos * 10)`
