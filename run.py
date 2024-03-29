from os import system, name
import random
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
        ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("battle_quips")

quips = SHEET.worksheet("quips")
scoreboard = SHEET.worksheet("scoreboard")


class Battlequips():
    """
    Creates an instance of BattleQuips game
    """
    life = 15
    board = [[" "] * 10 for i in range(10)]

    def __init__(self, grid_size, num_ships, ship_coords):
        self.grid_size = grid_size
        self.num_ships = num_ships
        self.ship_coords = ship_coords

    def description(self):
        """
        Describes the instance of BattleQuips game
        """
        return f"Grid Size: {self.grid_size}, Ships: {self.num_ships}"

    def update_board(self, coordinates, value):
        """
        Updates the BattleQuips board
        """
        x_coord = convert_coordinates(coordinates[0])
        y_coord = int(coordinates[1:])
        self.board[x_coord - 1][y_coord - 1] = value

    def print_board(self):
        """
        Prints out BattleQuips board
        """
        # Lines 50-64 are adapted from Stack Overflow:
        # https://stackoverflow.com/a/60842852

        char = 65
        # First row
        print("  ", end='')
        for j in range(self.grid_size):
            print(f"| {j+1} ", end='')
        print("| ")

        # Other rows
        for i in range(self.grid_size):
            print(f"{chr(char+i)} ", end='')
            for j in range(self.grid_size):
                print(f"| {self.board[i][j]} ", end='')
            print("| ")


def start_battlequips():
    """
    Starts BattleQuips game
    """
    clear()
    battlequips_game = Battlequips(10, 5, get_ship_coords())
    battlequips_game.board = [[" "] * 10 for i in range(10)]
    print("\n\n")
    battlequips_game.print_board()
    quotes = get_quips()

    while battlequips_game.life > 0:
        if len(battlequips_game.ship_coords) == 0:
            scoreboard.update('B2', int(scoreboard.acell('B2').value) + 1)
            print("Well done! You've sunk all the ships!")
            break
        coordinates = input("What co-ordinates would you like to attack?" +
                            " (e.g. B3, J7) \n")
        if validator(coordinates):
            clear()
            if coordinates.upper() in battlequips_game.ship_coords:
                battlequips_game.update_board(coordinates, "X")
                battlequips_game.ship_coords.remove(coordinates.upper())
                battlequips_game.life = 15
                print("Hit! As someone wise once said...")
                print(f"{quotes[random.randint(0, 24)]}")
                print("Keep firing!")
            else:
                battlequips_game.life = battlequips_game.life - 1
                battlequips_game.update_board(coordinates, "O")
                print(f"Miss!\nTry again.\nYou have {battlequips_game.life}" +
                      " attempt(s) left.")
            battlequips_game.print_board()
        else:
            print("Oops! Invalid values - please choose between A1-J10.")
    if battlequips_game.life == 0:
        scoreboard.update('A2', int(scoreboard.acell('A2').value) + 1)
        print("Uh-oh! You're out of lives. Please start again.")
    print(f"Player score: {scoreboard.acell('B2').value}, " +
          f"Computer score: {scoreboard.acell('A2').value}")


def get_ship_coords():
    """
    Retrieves ship co-ordinates from Google Sheets
    """
    data = quips.col_values(3)
    listnum = list(range(0, 24))
    random.shuffle(listnum)
    all_coords = []
    for i in range(5):
        all_coords += data[listnum[i]].split(",")
    return list(dict.fromkeys(all_coords))


def get_quips():
    """
    Retrieves quotes from Google Sheets
    """
    return quips.col_values(2)


def validator(coordinates):
    """
    Validates co-ordinates
    """
    if len(coordinates) < 2 or not coordinates.isalnum():
        return False
    x_coord = convert_coordinates(coordinates[0])
    if not coordinates[1:].isnumeric():
        return False
    y_coord = int(coordinates[1:])
    if x_coord > 10 or x_coord < 1:
        return False
    if y_coord > 10 or y_coord < 1:
        return False
    return True


def convert_coordinates(coordinate):
    """
    Converts co-ordinates to corresponding numerical value
    """
    return ord(coordinate.upper()) - 64


def run_game():
    """
    Start screen for Battlequips.
    """
    print("  ____        _   _   _      \n" +
          " |  _ \      | | | | | |     \n" +
          " | |_) | __ _| |_| |_| | ___ \n" +
          " |  _ < / _` | __| __| |/ _ \ \n" +
          " | |_) | (_| | |_| |_| |  __/\n" +
          " |____/ \__,_|\__|\__|_|\___|\n" +
          "  / __ \      (_)            \n" +
          " | |  | |_   _ _ _ __  ___   \n" +
          " | |  | | | | | | '_ \/ __|  \n" +
          " | |__| | |_| | | |_) \__ \  \n" +
          "  \___\_\\__,_ |_|  ._/|___/  \n" +
          "                | |          \n" +
          "                |_|          ")
    print("Hello! Welcome to BattleQuips!")
    print("You have 15 attempts to sink 5 ships of varying sizes...")
    print("If you get a hit, your attempts will reset,")
    print("revealing a quip from a historical figure.")

    is_game_running = True

    while is_game_running:
        start_game = input("Would you like to play a game? (Y/N) \n")
        if start_game.lower() == "n":
            is_game_running = False
        elif start_game.lower() == "y":
            start_battlequips()
        else:
            print("Please enter a valid answer...")


def clear():
    """
    Function for clearing screen
    Sourced from: https://www.geeksforgeeks.org/clear-screen-python/.
    """
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


run_game()
