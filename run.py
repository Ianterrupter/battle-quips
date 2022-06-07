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
    def __init__(self, grid_size, num_ships):
        self.grid_size = grid_size
        self.num_ships = num_ships
    
    def description(self):
        """
        Describes the instance of BattleQuips game
        """
        return f"Grid Size: {self.grid_size}, Number of Ships: {self.num_ships}"







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
            print("Start game")
        else:
            print("Please enter a valid answer...")


run_game()
