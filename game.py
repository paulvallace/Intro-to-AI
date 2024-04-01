import random

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = True   
        move = []
        piece_count = sum(row.count(self.my_piece) for row in state)
        drop_phase = piece_count < 4

        if not drop_phase:
            # Select a piece of the AI to move
            my_pieces = [(i, j) for i in range(5) for j in range(5) if state[i][j] == self.my_piece]
            source = random.choice(my_pieces)

            # Find a valid new position for the selected piece
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
            valid_moves = [(source[0] + dx, source[1] + dy) for dx, dy in directions]
            valid_moves = [(x, y) for x, y in valid_moves if 0 <= x < 5 and 0 <= y < 5 and state[x][y] == ' ']
            if valid_moves:
                destination = random.choice(valid_moves)
                move = [destination, source]
        else:
            # Drop phase
            (row, col) = (random.randint(0,4), random.randint(0,4))
            while not state[row][col] == ' ':
                (row, col) = (random.randint(0,4), random.randint(0,4))
            move = [(row, col)]

        return move

    def succ(self, state):
        successors = []
        piece_count = sum(row.count(self.my_piece) for row in state)
        drop_phase = piece_count < 4

        if drop_phase:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        new_state = [row[:] for row in state]
                        new_state[i][j] = self.my_piece
                        successors.append(new_state)
        else:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == self.my_piece:
                        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < 5 and 0 <= nj < 5 and state[ni][nj] == ' ':
                                new_state = [row[:] for row in state]
                                new_state[i][j] = ' '
                                new_state[ni][nj] = self.my_piece
                                successors.append(new_state)
        return successors

    def heuristic_game_value(self, state):
        # Placeholder heuristic: counts the number of AI pieces and opponent pieces
        my_count = sum(row.count(self.my_piece) for row in state)
        opp_count = sum(row.count(self.opp) for row in state)
        return (my_count - opp_count) / 8  # Normalize to range [-1, 1]

    def max_value(self, state, depth, depth_limit):
        if depth == depth_limit or self.game_value(state) != 0:
            return self.heuristic_game_value(state)
        v = float('-inf')
        for s in self.succ(state):
            v = max(v, self.min_value(s, depth + 1, depth_limit))
        return v

    def min_value(self, state, depth, depth_limit):
        if depth == depth_limit or self.game_value(state) != 0:
            return self.heuristic_game_value(state)
        v = float('inf')
        for s in self.succ(state):
            v = min(v, self.max_value(s, depth + 1, depth_limit))
        return v

    def make_move(self, state):
        best_score = float('-inf')
        best_move = None
        depth_limit = 3  # Adjust based on performance

        for s in self.succ(state):
            score = self.min_value(s, 1, depth_limit)
            if score > best_score:
                best_score = score
                best_move = s  # Store the entire state as the best move

        # Convert the best_move (state) to the move format required
        move = self.state_to_move(state, best_move)
        return move

    def state_to_move(self, old_state, new_state):

        drop_phase = sum(row.count(self.my_piece) for row in old_state) < 4
        if drop_phase:
            # In drop phase, find the newly added piece
            for i in range(5):
                for j in range(5):
                    if old_state[i][j] == ' ' and new_state[i][j] == self.my_piece:
                        return [(i, j)]
        else:
            # In move phase, find the piece that has moved
            for i in range(5):
                for j in range(5):
                    if old_state[i][j] == self.my_piece and new_state[i][j] == ' ':
                        source = (i, j)
                    elif old_state[i][j] == ' ' and new_state[i][j] == self.my_piece:
                        destination = (i, j)
            return [destination, source]

        return None  # Return None if no valid move is found


    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return 1 if state[i][j] == self.my_piece else -1
                
        # check / diagonal wins
        for i in range(2):
            for j in range(3, 5):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                    return 1 if state[i][j]==self.my_piece else -1
        # check box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j] == state[i][j+1] == state[i+1][j+1]:
                    return 1 if state[i][j]==self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
