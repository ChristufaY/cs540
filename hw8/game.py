import random
import numpy as np
import copy
import time
import sys

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    depth_count = 3

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
    
    def succ(self, numPieces, piece, state):
        successors = []   
        if(numPieces < 8):
            for row in range(len(state)):
                for col in range(len(state[row])):
                        if(state[row][col] == ' '):
                            successors.append([(row, col)])
        else:
            for row in range(len(state)):
                for col in range(len(state[row])):
                    if(piece == state[row][col]):
                        if(row-1 >= 0 and col-1 >= 0 and state[row-1][col-1] == ' '):
                            successors.append([(row-1, col-1), (row, col)])
                        if(row-1 >= 0 and state[row-1][col] == ' '):
                            successors.append([(row-1, col), (row, col)])
                        if(row-1 >= 0 and col+1 <= 4 and state[row-1][col+1] == ' '):
                            successors.append([(row-1, col+1), (row, col)])
                        if(col-1 >= 0 and state[row][col-1] == ' '):
                            successors.append([(row, col-1), (row, col)])
                        if(col+1 <= 4 and state[row][col+1] == ' '):
                            successors.append([(row, col+1), (row, col)])
                        if(row+1 <= 4 and col-1 >= 0 and state[row+1][col-1] == ' '):
                            successors.append([(row+1, col-1), (row, col)])
                        if(row+1 <= 4 and state[row+1][col] == ' '):
                            successors.append([(row+1, col), (row, col)])
                        if(row+1 <= 4 and col+1 <= 4 and state[row+1][col+1] == ' '):
                            successors.append([(row+1, col+1), (row, col)])
        return successors

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
        numPieces = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                if(state[i][j] != ' '):
                    numPieces = numPieces + 1
        if(numPieces > 7):
            drop_phase = False
        pos_candidates = [[(1, 1)], [(1, 2)], [(1, 3)], [(2, 1)], [(2, 3)], 
        [(3, 1)], [(3, 2)], [(3, 3)]]
        if numPieces < 2:
            if state[2][2] == ' ':
                return [(2, 2)]
            for i in np.random.permutation(len(pos_candidates)):
                pos = pos_candidates[i]
                if state[pos[0][0]][pos[0][1]] == ' ':
                    return pos
        # if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            # pass
        m, pos = self.max_value(copy.deepcopy(state), 0)
        return pos
       
    def make_move_random(self, state):
        drop_phase = True
        piece_count = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                if(state[i][j] != ' '):
                    piece_count = piece_count + 1
        if(piece_count > 7):
             drop_phase = False
        if not drop_phase:
            res = self.succ(piece_count, self.opp, state)
            move = res[np.random.permutation(len(res))[0]]
            return move
        move = []
        (row, col) = (random.randint(0, 4), random.randint(0, 4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0, 4), random.randint(0, 4))
        move.insert(0, (row, col))
        return move

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

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1
                
        # TODO: check / diagonal wins
        for row in range(2):
            for col in range(2):
                if state[4-row][col] != ' ' and state[4-row][col] == state[3-row][col+1] == state[2-row][col+2] == state[1-row][col+3]:
                    return 1 if state[4-row][col]==self.my_piece else -1
                
        # TODO: check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col] == state[row][col+1] == state[row+1][col+1]:
                    return 1 if state[row][col]==self.my_piece else -1

        return 0 # no winner yet

    def location(self, state, piece):
        loc = []
        for i in range(len(state)):
            for j in range(len(state[0])):
                if(state[i][j] == piece):
                    loc.append((i, j))
        return loc

    def heuristic_game_value(self, state, piece):
        loc = self.location(state, piece)
        heuristic_val = np.linalg.norm(np.array(loc) - np.array(loc)[:,None], axis = -1)
        if(heuristic_val.sum() == 0):
            return 0
        heuristic_val = 1 - 2 / heuristic_val.sum()
        if(self.my_piece != piece):
            heuristic_val = -heuristic_val
        return heuristic_val
 
    def max_value(self, state, depth):
        alpha = -100
        curr_pos = None

        game_val = self.game_value(state)
        if(game_val == 1 or game_val == -1):
            return (game_val, curr_pos)
        if(depth >= self.depth_count):
            m = self.heuristic_game_value(state, self.my_piece)
            return (m, curr_pos)

        num_blanks = sum(i.count(' ') for i in state)
        num_pieces = 25 - num_blanks

        for s in self.succ(num_pieces, self.my_piece, state):
            if(len(s) > 1):
                state[s[1][0]][s[1][1]] = ' '
            state[s[0][0]][s[0][1]] = self.my_piece
            m, pos = self.min_value(state, depth + 1)
            if m > alpha:
                alpha = m
                curr_pos = s
            if(len(s) > 1):
                state[s[1][0]][s[1][1]] = self.my_piece
            state[s[0][0]][s[0][1]] = ' '
        return (alpha, curr_pos)
        
    def min_value(self, state, depth):
        beta = 100
        curr_pos = None

        game_val = self.game_value(state)
        if(game_val == 1 or game_val == -1):
            return (game_val, curr_pos)
        if(depth >= self.depth_count):
            m = self.heuristic_game_value(state, self.opp)
            return (m, curr_pos)

        num_blanks = sum(i.count(' ') for i in state)
        num_pieces = 25 - num_blanks

        for s in self.succ(num_pieces, self.opp, state):
            if(len(s) > 1):
                state[s[1][0]][s[1][1]] = ' '
            state[s[0][0]][s[0][1]] = self.opp
            m, pos = self.max_value(state, depth + 1)
            if m < beta:
                beta = m
                curr_pos = s
            if(len(s) > 1):
                state[s[1][0]][s[1][1]] = self.opp
            state[s[0][0]][s[0][1]] = ' '
        return (beta, curr_pos)
    
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
            start = time.time()
            move = ai.make_move(ai.board)
            end = time.time()
            print('Evaluation time: {}s'.format(round(end - start, 10)))
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            #move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            move = ai.make_move_random(ai.board)
            ai.opponent_move(move)
            #while not move_made:
            #    player_move = input("Move (e.g. B3): ")
            #    while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
            #        player_move = input("Move (e.g. B3): ")
            #    try:
            #        ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
            #        move_made = True
            #    except Exception as e:
            #        print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            start = time.time()
            move = ai.make_move(ai.board)
            end = time.time()
            print('Evaluation time: {}s'.format(round(end - start, 10)))
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            #move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            move = ai.make_move_random(ai.board)
            ai.opponent_move(move)
            # while not move_made:
            #     move_from = input("Move from (e.g. B3): ")
            #     while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
            #         move_from = input("Move from (e.g. B3): ")
            #     move_to = input("Move to (e.g. B3): ")
            #     while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
            #         move_to = input("Move to (e.g. B3): ")
            #     try:
            #         ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
            #                         (int(move_from[1]), ord(move_from[0])-ord("A"))])
            #         move_made = True
            #     except Exception as e:
            #         print(e)

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







