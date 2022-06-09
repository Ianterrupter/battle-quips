import gspread
from google.oauth2.service_account import Credentials


class Battlequips():
    """
    Creates an instance of BattleQuips game
    """
    life = 10
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
        print((7*5+9)*"-")

        # Other rows
        for i in range(self.grid_size):
            print(f"{chr(char+i)} ", end='')
            for j in range(self.grid_size):
                print(f"| {self.board[i][j]} ", end='')
            print("| ")
            print((7*5+9)*"-")


def start_battlequips():
    """
    Starts BattleQuips game
    """
    # TODO: add feature to ask user for grid size and number of ships

    battlequips_game = Battlequips(10, 5, get_ship_coords())
    battlequips_game.print_board()

    while battlequips_game.life > 0:
        if len(battlequips_game.ship_coords) == 0:
            print("Well done! You've sunk all the ships!")
            break
        coordinates = input("What co-ordinates would you like to attack? (e.g. B3, J7) ")
        if validator(coordinates):
            if coordinates.upper() in battlequips_game.ship_coords:
                battlequips_game.update_board(coordinates, "X")
                print(battlequips_game.ship_coords)
                battlequips_game.ship_coords.remove(coordinates.upper())
                battlequips_game.life = 10
                print("Hit! Keep firing!")
            else:
                battlequips_game.life = battlequips_game.life - 1
                battlequips_game.update_board(coordinates, "O")
                print(f"Miss! Try again. You have {battlequips_game.life} attempt(s) left.")
            battlequips_game.print_board()
        else:
            print("Oops! Invalid values - please choose between A1-J10.")
    if battlequips_game.life == 0: 
        print("Uh-oh! You're out of lives. Please start again.")


def get_ship_coords():
    """
    Retrieves ship co-ordinates from Google Sheets
    """
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

    data = quips.col_values(3)

    all_coords = []
    for coords in data:
        all_coords += coords.split(",")
    return all_coords
    

def validator(coordinates):
    """
    Validates co-ordinates
    """
    # check if first character is a letter between A-J
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
    print("Hello! Welcome to BattleQuips!")
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
