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

data = quips.get_all_values()

print(data)


class Battlequips():
    """
    Creates an instance of BattleQuips game
    """
    life = 10

    def __init__(self, grid_size, num_ships):
        self.grid_size = grid_size
        self.num_ships = num_ships

    def description(self):
        """
        Describes the instance of BattleQuips game
        """
        return f"Grid Size: {self.grid_size}, Ships: {self.num_ships}"

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
        print((7*5+9)*"-")

        # Other rows
        for i in range(self.grid_size):
            print(f"{chr(char+i)} ", end='')
            for j in range(self.grid_size):
                print("| ~ ", end='')
            print("| ")
            print((7*5+9)*"-")


def start_battlequips():
    """
    Starts BattleQuips game
    """
    # TODO: add feature to ask user for grid size and number of ships
    battlequips_game = Battlequips(10, 5)
    battlequips_game.print_board()

    while battlequips_game.life > 0:
        coordinates = input("What co-ordinates would you like to attack? (e.g. B3, J7) ")
        validator(coordinates)
        # Check if valid input, hit or miss
        # If hit; battlequips_game.life = 10
        # If miss; battlequips_game.life--


def validator(coordinates):
    """
    Validates co-ordinates
    """
    # check if first character is a letter between A-J
    x = ord(coordinates[0])
    print(x)

    # check if second character is a number between 1-10
    # slice from 1 to end
    return True

def run_game():
    """
    Start screen for Battlequips.
    """
    print("Hello! Welcome to BattleQuips!")

    is_game_running = True

    while is_game_running:
        start_game = input("Would you like to play a game? (Y/N) ")
        if start_game.lower() == "n":
            is_game_running = False
        elif start_game.lower() == "y":
            is_game_running = False
            start_battlequips()
        else:
            print("Please enter a valid answer...")


run_game()
