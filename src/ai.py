import random
from const import *
from move import Move
from piece import *


import time
import random
from const import *
from move import Move

class AI:
    def __init__(self, depth=3):
        self.depth = depth
        self.max_time = 5  # Maximum time in seconds for AI to make a decision
        self.max_moves = 1000  # Maximum number of moves to evaluate

    def get_best_move(self, board):
        print("Getting best move for AI...")
        start_time = time.time()
        best_move = None
        best_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        moves_evaluated = 0

        possible_moves = self.get_all_moves(board, 'black')
        print(f"Found {len(possible_moves)} possible moves")
        random.shuffle(possible_moves)  # Randomize move order for variety

        for move in possible_moves:
            print(f"Evaluating move: {move}")
            board.move(move.piece, move)
            eval, _ = self.minimax(board, self.depth - 1, alpha, beta, False)
            board.undo_move()

            print(f"Move evaluation: {eval}")

            if eval > best_eval:
                best_eval = eval
                best_move = move

            alpha = max(alpha, eval)
            moves_evaluated += 1

            if time.time() - start_time > self.max_time or moves_evaluated >= self.max_moves:
                print(f"AI search stopped: {'Time limit reached' if time.time() - start_time > self.max_time else 'Move limit reached'}")
                break

        if best_move:
            print(f"Best move found: {best_move}, Eval: {best_eval}, Moves evaluated: {moves_evaluated}, Time taken: {time.time() - start_time:.2f}s")
        else:
            print("No valid move found")
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_all_moves(board, 'black'):
                board.move(move.piece, move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.undo_move()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_all_moves(board, 'white'):
                board.move(move.piece, move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.undo_move()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_all_moves(self, board, color):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_team_piece(color):
                    piece = board.squares[row][col].piece
                    board.calc_moves(piece, row, col, bool=False)
                    moves.extend(piece.moves)
        return moves

    def evaluate_board(self, board):
        evaluation = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    evaluation += piece.value
        return evaluation

    # Piece-Square Tables for positional evaluation
    pawn_table = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ]

    knight_table = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]

    bishop_table = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]

    rook_table = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]
    ]

    queen_table = [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ]

    king_table = [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]
    ]
