import os
import random

class Ship:
    def __init__(self, size):
        self.size = size
        self.hits = 0

    def is_sunk(self):
        return self.hits == self.size

class Player:
    def __init__(self, name):
        self.name = name
        self.board = [[' ' for _ in range(7)] for _ in range(7)]
        self.ships = [Ship(3), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)]

    def place_ships_randomly(self):
        for ship in self.ships:
            while True:
                try:
                    row, col, orientation = self.get_random_coordinates(ship.size)
                    self.place_ship(ship, row, col, orientation)
                    break
                except ValueError:
                    pass

    def get_random_coordinates(self, ship_size):
        row = random.randint(0, 6)
        col = random.randint(0, 6)
        orientation = random.choice(['horizontal', 'vertical'])
        return row, col, orientation

    def place_ship(self, ship, row, col, orientation):
        if orientation == 'horizontal':
            for i in range(ship.size):
                if self.board[row][col + i] != ' ':
                    raise ValueError("Ships cannot overlap.")
            for i in range(ship.size):
                self.board[row][col + i] = str(ship.size)
        elif orientation == 'vertical':
            for i in range(ship.size):
                if self.board[row + i][col] != ' ':
                    raise ValueError("Ships cannot overlap.")
            for i in range(ship.size):
                self.board[row + i][col] = str(ship.size)

    def display_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("   1 2 3 4 5 6 7")
        for i, row in enumerate(self.board):
            print(chr(ord('A') + i), end='  ')
            print(' '.join(cell if cell in ['X', 'O', 'M'] else ' ' for cell in row))
        print()

    def take_shot(self):
        while True:
            try:
                coordinates = input("Take a shot (e.g., A1): ").upper()
                row, col = ord(coordinates[0]) - ord('A'), int(coordinates[1]) - 1
                if not (0 <= row < 7) or not (0 <= col < 7) or self.board[row][col] in ['X', 'O', 'M']:
                    raise ValueError("Invalid shot. Try again.")
                return row, col
            except (ValueError, IndexError, TypeError):
                print("Invalid input. Try again.")

def report_hit(result, ship_size):
    if result == 'hit':
        return f"Hit! Ship of size {ship_size}"
    elif result == 'sunk':
        return f"Sunk! Ship of size {ship_size}"
    else:
        return "Miss!"

def main():
    players = []
    
    while True:
        print("Welcome to Battleship!")
        player_name = input("Enter your name: ")
        player = Player(player_name)

        player.place_ships_randomly()
        input("Press Enter to start the game. The ship placement will be hidden.")

        shots = 0

        while any(not ship.is_sunk() for ship in player.ships):
            player.display_board()
            row, col = player.take_shot()
            shots += 1

            if player.board[row][col] == ' ':
                print("Miss!")
                player.board[row][col] = 'M'
                result = 'miss'
            else:
                ship_size = int(player.board[row][col])
                player.ships[ship_size - 1].hits += 1
                player.board[row][col] = 'X'
                if player.ships[ship_size - 1].is_sunk():
                    result = 'sunk'
                else:
                    result = 'hit'
            
                print(report_hit(result, ship_size))

        player.display_board()
        print(f"Congratulations, {player.name}! You sunk all the ships in {shots} shots.")
        players.append((player.name, shots))

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            break

    print("\nGame Over. Here are the results:")
    players.sort(key=lambda x: x[1])  # Sort players based on the number of shots
    for i, (name, shots) in enumerate(players, start=1):
        print(f"{i}. {name}: {shots} shots")

if __name__ == "__main__":
    main()
