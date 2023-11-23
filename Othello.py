# Author: Paige Knickerbocker
# GitHub username: knickerbockermt
# Date: 6/4/2023
# Description: Text-based Othello game for two players with Player and Othello classes.
# Player class represents player object with player name and piece color. Othello class
# represents Othello game that creates players, initializes the game board, takes and
# validates position from player. If position is valid, places piece on the board
# and captures opponent's pieces in valid directions. Keeps count of players' pieces and
# returns a winner when no player can make a valid move.


class Player:
    """represents a player object. Initializes player name and piece color. Used by
    Othello class to create player"""

    def __init__(self, name, color):
        """takes player name and piece color as parameters and initializes them to
        self._name and self._color respectively"""
        self._name = name
        self._color = color

    def get_name(self):
        """returns player's name"""
        return self._name

    def get_color(self):
        """returns color of player's pieces"""
        return self._color


class Othello:
    """Represents an Othello game object. Initializes game board, creates player objects,
    returns available positions for player to choose, takes given position from player and
    validates the move; if valid, will place piece at position and return the updated board;
    checks if game has ended and returns winner; calls on player class to create players"""

    def __init__(self):
        """initializes game board, player list, number of pieces on board for each player, list
        of available positions, list of valid directions, and winner;
        takes no parameters"""
        self._board = [
            ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", ".", ".", ".", "O", "X", ".", ".", ".", "*"],
            ["*", ".", ".", ".", "X", "O", ".", ".", ".", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*"]
        ]
        self._player_list = []
        self._black_pieces = 2
        self._white_pieces = 2
        self._white_available_positions = []
        self._black_available_positions = []
        self._valid_directions = []
        self._end = False
        self._winning_color = None
        self._player_color = None
        self._opponent_color = None

    def print_board(self):
        """prints self._board to console"""
        for row in self._board:
            print("  ".join(row))

    def create_player(self, player_name, color):
        """calls Player class to create player object, adds player object to self._players; takes
        player name and piece color as parameters"""
        player = Player(player_name, color)
        self._player_list.append(player)

    def play_game(self, player_color, piece_position):
        """takes player color and position chosen by player as parameters;
        calls validate functions to see if move is valid; if valid, calls make move to update board,
        calls check_winner to check if there is a winner, if so, calls return_winner and prints
        final score and winner to console"""
        if player_color == "black":
            self._player_color = "X"
            self._opponent_color = "O"

        if player_color == "white":
            self._player_color = "O"
            self._opponent_color = "X"

        # check if position is valid
        self.validate_move(piece_position)

        if not self._valid_directions:  # no valid directions
            self.return_available_positions(player_color)
            print("Invalid Move")
            if player_color == "black":
                print("Here are the valid moves: ", self._black_available_positions)
                return "Invalid move"
            if player_color == "white":
                print("Here are the valid moves: ", self._white_available_positions)
                return "Invalid move"

        else:
            # make move
            self.make_move(player_color, piece_position)

            # check for end of game
            if player_color == "white":
                opponent_color = "black"
                self.check_end(player_color, opponent_color)

            if player_color == "black":
                opponent_color = "white"
                self.check_end(player_color, opponent_color)

            if self._end:
                white_score = str(self._white_pieces)
                black_score = str(self._black_pieces)
                scores = "Game is ended white piece: " + white_score + " black piece: " + black_score
                print(scores)
                print(self.return_winner())

    def validate_move(self, piece_position):
        """helper function for play_game to validate player's position
        choice; calls each direction's validate function; for each valid
        direction, adds to list of valid directions that will be used by make_move"""
        self._valid_directions = []

        if self.validate_right(piece_position) is True:
            self._valid_directions.append("right")

        if self.validate_left(piece_position) is True:
            self._valid_directions.append("left")

        if self.validate_up(piece_position) is True:
            self._valid_directions.append("up")

        if self.validate_down(piece_position) is True:
            self._valid_directions.append("down")

        if self.validate_right_up(piece_position) is True:
            self._valid_directions.append("right up")

        if self.validate_right_down(piece_position) is True:
            self._valid_directions.append("right down")

        if self.validate_left_up(piece_position) is True:
            self._valid_directions.append("left up")

        if self.validate_left_down(piece_position) is True:
            self._valid_directions.append("left down")

        return

    def validate_right(self, piece_position, row=None, col=None):
        """takes player color and board position chosen by player as parameters,
        called by validate_move and return_available_positions to check if pieces form a valid
        line to the right of the chosen piece; returns true if direction is valid, false if invalid"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        # check if position is empty
        if col == piece_position[1]:
            if self._board[row][col] == "*":
                return False

            if self._board[row][col] == self._player_color:
                return False

            if self._board[row][col] == self._opponent_color:
                return False

        # check if line of pieces ends with "."
        if self._board[row][col + 1] == ".":
            return False

        # check if line of pieces ends with "*"
        if self._board[row][col + 1] == "*":
            return False

        # check if next piece is player's color
        if self._board[row][col + 1] == self._player_color:
            if col == piece_position[1]: # no opponent pieces between player's pieces
                return False
            else:
                return True

        # if next piece is opponent's color
        if self._board[row][col + 1] == self._opponent_color:
            return self.validate_right(piece_position, row, col + 1)

    def validate_left(self, piece_position, row=None, col=None):
        """takes player color and board position chosen by player as parameters,
        called by validate_move and return_available_positions to check if pieces form a valid horizontal
        line to the left of the chosen piece; returns true if direction is valid, false if invalid"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if col == piece_position[1]:
            if self._board[row][col] == "*":
                return False

            if self._board[row][col] == self._player_color:
                return False

            if self._board[row][col] == self._opponent_color:
                return False

        if self._board[row][col - 1] == ".":
            return False

        if self._board[row][col - 1] == "*":
            return False

        if self._board[row][col - 1] == self._player_color:
            if col == piece_position[1]:
                return False
            else:
                return True

        if self._board[row][col - 1] == self._opponent_color:
            return self.validate_left(piece_position, row, col - 1)

    def validate_up(self, piece_position, row=None, col=None):
        """takes player color and board position chosen by player as parameters,
        called by validate_move and return_available_positions to check if pieces form a valid vertical
        line above the chosen piece; returns true if direction is valid, false if invalid"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if row == piece_position[0]:
            if self._board[row][col] == "*":
                return False

            if self._board[row][col] == self._player_color:
                return False

            if self._board[row][col] == self._opponent_color:
                return False

        if self._board[row - 1][col] == ".":
            return False

        if self._board[row - 1][col] == "*":
            return False

        if self._board[row - 1][col] == self._player_color:
            if row == piece_position[0]:
                return False
            else:
                return True

        if self._board[row - 1][col] == self._opponent_color:
            return self.validate_up(piece_position, row - 1, col)

    def validate_down(self, piece_position, row=None, col=None):
        """takes player color and board position chosen by player as parameters,
        called by validate_move and return_available_positions to check if pieces form a valid
        vertical line below the chosen piece; returns true if direction is valid, false if invalid"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if row == piece_position[0]:
            if self._board[row][col] == "*":
                return False

            if self._board[row][col] == self._player_color:
                return False

            if self._board[row][col] == self._opponent_color:
                return False

        if self._board[row + 1][col] == ".":
            return False

        if self._board[row + 1][col] == "*":
            return False

        if self._board[row + 1][col] == self._player_color:
            if row == piece_position[0]:
                return False
            else:
                return True

        if self._board[row + 1][col] == self._opponent_color:
            return self.validate_down(piece_position, row + 1, col)

    def validate_right_up(self, piece_position, row=None, col=None):
        """takes player color and board position chosen by player as parameters,
        called by validate_move and return_available_positions to check if pieces form a valid right up
        diagonal line the chosen piece; returns true if direction is valid, false if invalid"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if row == piece_position[0]:
            if self._board[row][col] == "*":
                return False

            if self._board[row][col] == self._player_color:
                return False

            if self._board[row][col] == self._opponent_color:
                return False

        if self._board[row - 1][col + 1] == ".":
            return False

        if self._board[row - 1][col + 1] == "*":
            return False

        if self._board[row - 1][col + 1] == self._player_color:
            if col == piece_position[1]:
                return False
            else:
                return True

        if self._board[row - 1][col + 1] == self._opponent_color:
            return self.validate_right_up(piece_position, row - 1, col + 1)

    def validate_right_down(self, piece_position, row=None, col=None):
        """takes player color and board position chosen by player as parameters,
        called by validate_move and return_available_positions to check if pieces form a valid right down
        diagonal line the chosen piece; returns true if direction is valid, false if invalid"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if row == piece_position[0]:
            if self._board[row][col] == "*":
                return False

            if self._board[row][col] == self._player_color:
                return False

            if self._board[row][col] == self._opponent_color:
                return False

        if self._board[row + 1][col + 1] == ".":
            return False

        if self._board[row + 1][col + 1] == "*":
            return False

        if self._board[row + 1][col + 1] == self._player_color:
            if col == piece_position[1]:
                return False
            else:
                return True

        if self._board[row + 1][col + 1] == self._opponent_color:
            return self.validate_right_down(piece_position, row + 1, col + 1)

    def validate_left_up(self, piece_position, row=None, col=None):
        """takes player color and board position chosen by player as parameters,
        called by validate_move and return_available_positions to check if pieces form a valid left up
        diagonal line the chosen piece; returns true if direction is valid, false if invalid"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if row == piece_position[0]:
            if self._board[row][col] == "*":
                return False

            if self._board[row][col] == self._player_color:
                return False

            if self._board[row][col] == self._opponent_color:
                return False

        if self._board[row - 1][col - 1] == ".":
            return False

        if self._board[row - 1][col - 1] == "*":
            return False

        if self._board[row - 1][col - 1] == self._player_color:
            if col == piece_position[1]:
                return False
            else:
                return True

        if self._board[row - 1][col - 1] == self._opponent_color:
            return self.validate_left_up(piece_position, row - 1, col - 1)

    def validate_left_down(self, piece_position, row=None, col=None):
        """takes player color and board position chosen by player as parameters,
        called by validate_move and return_available_positions to check if pieces form a valid left down
        diagonal line the chosen piece; returns true if direction is valid, false if invalid"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if row == piece_position[0]:
            if self._board[row][col] == "*":
                return False

            if self._board[row][col] == self._player_color:
                return False

            if self._board[row][col] == self._opponent_color:
                return False

        if self._board[row + 1][col - 1] == ".":
            return False

        if self._board[row + 1][col - 1] == "*":
            return False

        if self._board[row + 1][col - 1] == self._player_color:
            if col == piece_position[1]:
                return False
            else:
                return True

        if self._board[row + 1][col - 1] == self._opponent_color:
            return self.validate_left_down(piece_position, row + 1, col - 1)

    def make_move(self, color, piece_position):
        """helper function for play_game; takes player color and board position chosen by player
        as parameters, called by play_game when player makes valid move, places player's piece and
        calls capture_pieces to flips any captured tokens, returns board updated with player's move"""
        # initialize colors and position
        row = piece_position[0]
        col = piece_position[1]

        if color == "black":
            self._player_color = "X"
            self._opponent_color = "O"

        if color == "white":
            self._player_color = "O"
            self._opponent_color = "X"

        # get valid directions
        self.validate_move(piece_position)

        # put player's tile down and update piece count
        self._board[row][col] = self._player_color

        if color == "black":
            self._black_pieces += 1

        if color == "white":
            self._white_pieces += 1

        # flip pieces in each valid direction
        for direction in self._valid_directions:
            if direction == "right":
                self.capture_right(color, piece_position)

            if direction == "left":
                self.capture_left(color, piece_position)

            if direction == "up":
                self.capture_up(color, piece_position)

            if direction == "down":
                self.capture_down(color, piece_position)

            if direction == "right up":
                self.capture_right_up(color, piece_position)

            if direction == "right down":
                self.capture_right_down(color, piece_position)

            if direction == "left up":
                self.capture_left_up(color, piece_position)

            if direction == "left down":
                self.capture_left_down(color, piece_position)

        return self._board

    def capture_right(self, color, piece_position, row=None, col=None):
        """helper function for make_move; takes player color and piece position as parameters;
        flips any pieces captured to right of a player's move and updates board;
        does not return anything"""
        # initialize row and col
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        # end when reach player color in next position
        if self._board[row][col + 1] == self._player_color:
            return

        # continue to next position if opponent's color
        if self._board[row][col + 1] == self._opponent_color:
            self._board[row][col + 1] = self._player_color  # change next to player's color

            # update piece counts
            if color == "black":
                self._black_pieces += 1
                self._white_pieces -= 1

            if color == "white":
                self._white_pieces += 1
                self._black_pieces -= 1

            return self.capture_right(color, piece_position, row, col + 1)

    def capture_left(self, color, piece_position, row=None, col=None):
        """helper function for make_move; takes player color and piece position as parameters;
        flips any pieces captured to left of a player's move and updates board;
        does not return anything"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if self._board[row][col - 1] == self._player_color:
            return

        if self._board[row][col - 1] == self._opponent_color:
            self._board[row][col - 1] = self._player_color

            if color == "black":
                self._black_pieces += 1
                self._white_pieces -= 1

            if color == "white":
                self._white_pieces += 1
                self._black_pieces -= 1

            return self.capture_left(color, piece_position, row, col - 1)

    def capture_up(self, color, piece_position, row=None, col=None):
        """helper function for make_move; takes player color and piece position as parameters;
        flips any pieces captured above a player's move and updates board; does not return anything"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if self._board[row - 1][col] == self._player_color:
            return

        if self._board[row - 1][col] == self._opponent_color:
            self._board[row - 1][col] = self._player_color

            if color == "black":
                self._black_pieces += 1
                self._white_pieces -= 1

            if color == "white":
                self._white_pieces += 1
                self._black_pieces -= 1

            return self.capture_up(color, piece_position, row - 1, col)

    def capture_down(self, color, piece_position, row=None, col=None):
        """helper function for make_move; takes player color and piece position as parameters;
        flips any pieces captured below a player's move and updates board; does not return anything"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if self._board[row + 1][col] == self._player_color:
            return

        if self._board[row + 1][col] == self._opponent_color:
            self._board[row + 1][col] = self._player_color

            if color == "black":
                self._black_pieces += 1
                self._white_pieces -= 1

            if color == "white":
                self._white_pieces += 1
                self._black_pieces -= 1

            return self.capture_down(color, piece_position, row + 1, col)

    def capture_right_up(self, color, piece_position, row=None, col=None):
        """helper function for make_move; takes player color and piece position as parameters;
        flips any pieces captured to right up diagonal of player's move and updates board;
        does not return anything"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if self._board[row - 1][col + 1] == self._player_color:
            return

        if self._board[row - 1][col + 1] == self._opponent_color:
            self._board[row - 1][col + 1] = self._player_color

            if color == "black":
                self._black_pieces += 1
                self._white_pieces -= 1

            if color == "white":
                self._white_pieces += 1
                self._black_pieces -= 1

            return self.capture_right_up(color, piece_position, row - 1, col + 1)

    def capture_right_down(self, color, piece_position, row=None, col=None):
        """helper function for make_move; takes player color and piece position as parameters;
        flips any pieces captured to right down diagonal of player's move and updates board;
        does not return anything"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if self._board[row + 1][col + 1] == self._player_color:
            return

        if self._board[row + 1][col + 1] == self._opponent_color:
            self._board[row + 1][col + 1] = self._player_color

            if color == "black":
                self._black_pieces += 1
                self._white_pieces -= 1

            if color == "white":
                self._white_pieces += 1
                self._black_pieces -= 1

            return self.capture_right_down(color, piece_position, row + 1, col + 1)

    def capture_left_up(self, color, piece_position, row=None, col=None):
        """helper function for make_move; takes player color and piece position as parameters;
        flips any pieces captured to left up diagonal of player's move and updates board;
        does not return anything"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if self._board[row - 1][col - 1] == self._player_color:
            return

        if self._board[row - 1][col - 1] == self._opponent_color:
            self._board[row - 1][col - 1] = self._player_color

            if color == "black":
                self._black_pieces += 1
                self._white_pieces -= 1

            if color == "white":
                self._white_pieces += 1
                self._black_pieces -= 1

            return self.capture_left_up(color, piece_position, row - 1, col - 1)

    def capture_left_down(self, color, piece_position, row=None, col=None):
        """helper function for make_move; takes player color and piece position as parameters;
        flips any pieces captured to left down diagonal of player's move and updates board;
        does not return anything"""
        if row is None and col is None:
            row = piece_position[0]
            col = piece_position[1]

        if self._board[row + 1][col - 1] == self._player_color:
            return

        if self._board[row + 1][col - 1] == self._opponent_color:
            self._board[row + 1][col - 1] = self._player_color

            if color == "black":
                self._black_pieces += 1
                self._white_pieces -= 1

            if color == "white":
                self._white_pieces += 1
                self._black_pieces -= 1

            return self.capture_left_down(color, piece_position, row + 1, col - 1)

    def return_available_positions(self, color):
        """takes player color as a parameter, checks board for valid moves and returns
        list of available positions for player to chose for their
        turn; called on by play_game after player attempts invalid move"""
        if color == "black":
            self._black_available_positions = []
            self._player_color = "X"
            self._opponent_color = "O"
            row = 0  # start at first row

            for line in self._board:
                col = 0  # start at first column of each row
                # validate each direction at each position
                for pos in line:
                    position = (row, col)

                    if self.validate_right(position) is True:
                        if position not in self._black_available_positions:
                            self._black_available_positions.append(position)

                    if self.validate_left(position) is True:
                        if position not in self._black_available_positions:
                            self._black_available_positions.append(position)

                    if self.validate_up(position) is True:
                        if position not in self._black_available_positions:
                            self._black_available_positions.append(position)

                    if self.validate_down(position) is True:
                        if position not in self._black_available_positions:
                            self._black_available_positions.append(position)

                    if self.validate_right_up(position) is True:
                        if position not in self._black_available_positions:
                            self._black_available_positions.append(position)

                    if self.validate_right_down(position) is True:
                        if position not in self._black_available_positions:
                            self._black_available_positions.append(position)

                    if self.validate_left_up(position) is True:
                        if position not in self._black_available_positions:
                            self._black_available_positions.append(position)

                    if self.validate_left_down(position) is True:
                        if position not in self._black_available_positions:
                            self._black_available_positions.append(position)

                    col += 1

                row += 1

            return self._black_available_positions

        if color == "white":
            self._white_available_positions = []
            self._player_color = "O"
            self._opponent_color = "X"
            row = 0

            for line in self._board:
                col = 0  # start at first column of each row
                # validate each direction at each position
                for pos in line:
                    position = (row, col)

                    if self.validate_right(position) is True:
                        if position not in self._white_available_positions:
                            self._white_available_positions.append(position)

                    if self.validate_left(position) is True:
                        if position not in self._white_available_positions:
                            self._white_available_positions.append(position)

                    if self.validate_up(position) is True:
                        if position not in self._white_available_positions:
                            self._white_available_positions.append(position)

                    if self.validate_down(position) is True:
                        if position not in self._white_available_positions:
                            self._white_available_positions.append(position)

                    if self.validate_right_up(position) is True:
                        if position not in self._white_available_positions:
                            self._white_available_positions.append(position)

                    if self.validate_right_down(position) is True:
                        if position not in self._white_available_positions:
                            self._white_available_positions.append(position)

                    if self.validate_left_up(position) is True:
                        if position not in self._white_available_positions:
                            self._white_available_positions.append(position)

                    if self.validate_left_down(position) is True:
                        if position not in self._white_available_positions:
                            self._white_available_positions.append(position)

                    col += 1

                row += 1

            return self._white_available_positions

    def check_end(self, color, opponent_color):
        """ helper function for play_game; determines if board has any open spots;
        if no open spots on board, returns winner; if open spots, returns none;
        called by play_game after each turn"""

        self.return_available_positions(opponent_color)  # first check if opponent has moves

        if opponent_color == "white":
            if not self._white_available_positions:  # no valid moves for opponent
                self.return_available_positions(color)  # check if player has valid moves
                if not self._black_available_positions:  # if no valid moves
                    self._end = True  # reached end of game
                else:
                    return
            else:
                return

        if opponent_color == "black":
            if not self._black_available_positions:  # no valid moves for opponent
                self.return_available_positions(color)  # check if player has valid moves
                if not self._white_available_positions:  # if no valid moves
                    self._end = True  # reached end of game
                else:
                    return
            else:
                return

        if self._end is True:
            if self._black_pieces > self._white_pieces:
                self._winning_color = "black"

            if self._white_pieces > self._black_pieces:
                self._winning_color = "white"

            if self._white_pieces == self._black_pieces:
                self._winning_color = "tie"

    def return_winner(self):
        """helper function for play_game; called by play_game at end of game; returns
        string with winner color and name; if tied, returns string stating there was a tie"""
        if self._winning_color == "tie":
            return "It's a tie"

        for player in self._player_list:
            color = player.get_color()

            if color == self._winning_color:
                name = player.get_name()
                winner = "Winner is " + color + " player: " + name
                return winner


def main():
    game = Othello()
    game.create_player("Helen", "white")
    game.create_player("Leo", "black")
    game.play_game("white", (8,4))
    game.print_board()
    print(game.return_available_positions("white"))


if __name__ == '__main__':
    main()
