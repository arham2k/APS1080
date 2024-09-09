'''
Arham Sheikh| Sept. 9, 2024

Consider the game of tic tac toe (TTT). Two individuals (i.e., an X-player, and an O-player) 
play on a 9-position board, alternately placing "X" or "O" markers on the board. A player wins 
when they have achieved three markers of their type, in a row (vertical, horizontal, diagonal).

Code a TTT player in the following manner:

Create a python class maintains the TTT board. It should have a reset method (to clear the TTT 
board), methods for setting the position of the board for each player, and a method to indicate 
whether the game has been won (returning who has won), or whether the game is at a draw.

Test this python class, by playing a two-human game of TTT.

Now you are to create a computer player. The goal of the computer player is to win if possible, 
or at worst, not lose. First think about the strategy that you need to codify, and then codify it.

Test your python class, by playing a human-vs-computer game of TTT.
'''

import numpy as np


Rows = 3
Cols = 3
Size = Rows * Cols

class Board:
    def __init__(self):
        # the board is represented by an n * n array,
        # 1 represents an X for the player who moves first,
        # -1 represents an O of the other player
        # 0 represents an empty position
        self.data = np.zeros((Rows, Cols))
        self.winner = None
        self.hash_val = None
        self.end = False

    def is_end(self):        
        results = []

        # check row
        for i in range(Rows):
            results.append(np.sum(self.data[i, :]))
        # check columns
        for i in range(Cols):
            results.append(np.sum(self.data[:, i]))

        # check diagonals
        count = 0
        reverse_count = 0
        for i in range(Rows):
            count += self.data[i, i]
            reverse_count += self.data[i, Rows - 1 - i]
        results.append(count)
        results.append(reverse_count)
                
        for result in results:
            if result == 3:
                self.winner = 1
                self.end = True
                return self.end
            elif result == -3:
                self.winner = -1
                self.end = True
                return self.end
            
        # whether it's a tie
        sum_values = np.sum(np.abs(self.data))
        if sum_values == Size:
            self.winner = 0
            self.end = True
            return self.end

        # game is still going on
        self.end = False
        return self.end

    # put X or O symbol in position (i, j)
    def next_board(self, i, j, symbol):
        new_state = Board()
        new_state.data = np.copy(self.data)
        new_state.data[i, j] = symbol
        return new_state

    def available_moves(self):
        moves = []
        for i in range(Rows):
            for j in range(Cols):
                if self.data[i, j] == 0:
                    moves.append((i, j))
        
        return moves
    
    def update_state(self, i, j, symbol):
        if self.data[i, j] == 0:
            self.data[i, j] = symbol
            return True
        else:
            print("Invalid move!")
            return False
        
    def reset(self):
        self.data = np.zeros((Rows, Cols))
        self.winner = None
        self.end = None
        
    # print the board
    def print_state(self):
        for i in range(Rows):
            print('-------------')
            out = '| '
            for j in range(Cols):
                if self.data[i, j] == 1:
                    token = 'X'
                elif self.data[i, j] == -1:
                    token = 'O'
                else:
                    token = '!'
                out += token + ' | '
            print(out)
        print('-------------')

class Player:
    def __init__(self, name: str, symbol: int):
        self.name = name
        self.symbol = symbol

    def make_move(self, board):
        available = board.available_moves()
        print(f"Available moves: {available}")

        while True:
            move = input(f"{self.name} ({'X' if self.symbol == 1 else 'O'}), enter your move (row,col): ")
            try:
                i, j = map(int, move.split(','))
                if (i, j) in available:
                    board.update_state(i, j, self.symbol)
                    break
                else:
                    print("Move not valid, try again!")
            except ValueError:
                print("Invalid input format. Please enter row,col as integers.")

class AIPlayer:
    def __init__(self, name: str, symbol: int):
        self.name = name
        self.symbol = symbol

    def make_move(self, board):
        # Check if AI can win
        for move in board.available_moves():
            new_board = board.next_board(move[0], move[1], self.symbol)
            if new_board.is_end() and new_board.winner == self.symbol:
                board.update_state(move[0], move[1], self.symbol)
                return
        
        # Check if opponent can win, block it
        opponent_symbol = -self.symbol
        for move in board.available_moves():
            new_board = board.next_board(move[0], move[1], opponent_symbol)
            if new_board.is_end() and new_board.winner == opponent_symbol:
                board.update_state(move[0], move[1], self.symbol)
                return
        
        # Take a corner if available
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for corner in corners:
            if corner in board.available_moves():
                board.update_state(corner[0], corner[1], self.symbol)
                return
        
        # Take the center if available
        if (1, 1) in board.available_moves():
            board.update_state(1, 1, self.symbol)
            return

        # Take any remaining available move
        available_moves = board.available_moves()
        if available_moves:
            move = available_moves[0]
            board.update_state(move[0], move[1], self.symbol)

def play_game():
    board = Board()
    player1 = Player("Player 1", 1)  # Human player
    player2 = AIPlayer("Computer", -1)  # AI player

    current_player = player1

    while not board.is_end():
        board.print_state()
        current_player.make_move(board)

        if board.is_end():
            break

        current_player = player2 if current_player == player1 else player1

    board.print_state()
    if board.winner == 1:
        print("Player 1 (X) wins!")
    elif board.winner == -1:
        print("Computer (O) wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    play_game()