from connect_four import ConnectFour


def main():
    """ Play a game!
    """
    connect_four = ConnectFour()
    menu_choice = 1
    while menu_choice == 1:
        # start the game
        connect_four.start_new()
        # menu
        print("Menu")
        print("1 - Play again")
        print("2 - Quit")
        menu_choice = int(raw_input("choice : "))


if __name__ == "__main__":
    main()
