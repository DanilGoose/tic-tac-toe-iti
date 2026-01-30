from typing import List, Tuple, Optional
from game.board import Board
from game.player import Player


class GameRules:
    WIN_LENGTH = 5
    MAX_MOVES_PER_TURN = 3
    
    def __init__(self, board: Board, players: List[Player], win_patterns: List[dict] = None):
        self.board = board
        self.players = players
        self.win_patterns = win_patterns
        self.current_player_index = 0
        self.pending_moves: List[Tuple[int, int]] = []
        self.winner: Optional[Player] = None
        self.winning_cells: List[Tuple[int, int]] = []
        self.is_draw = False
        self.game_over = False
        self.last_player_index: Optional[int] = None
        self.eliminated: set[int] = set()
    
    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]
    
    def get_remaining_moves(self) -> int:
        return self.MAX_MOVES_PER_TURN - len(self.pending_moves)
    
    def is_player_active(self, index: int) -> bool:
        return index not in self.eliminated

    def eliminate_last_player(self) -> bool:
        if self.last_player_index is None:
            return False
        self.eliminated.add(self.last_player_index)
        if len(self.eliminated) >= len(self.players):
            self.is_draw = True
            self.game_over = True
        return True

    def add_pending_move(self, x: int, y: int) -> Tuple[bool, str]:
        if self.game_over:
            return False, "Игра окончена"
        
        if not self.board.is_valid_position(x, y):
            return False, "Некорректные координаты"
        
        if not self.board.is_empty(x, y):
            return False, "Ячейка занята"
        
        if (x, y) in self.pending_moves:
            return False, "Эта клетка уже выбрана"
        
        if len(self.pending_moves) >= self.MAX_MOVES_PER_TURN:
            return False, "Достигнут лимит ходов"
        
        self.pending_moves.append((x, y))
        return True, "OK"
    
    def remove_last_pending_move(self) -> bool:
        if self.pending_moves:
            self.pending_moves.pop()
            return True
        return False
    
    def clear_pending_moves(self):
        self.pending_moves.clear()
    
    def confirm_turn(self) -> Tuple[bool, str]:
        if self.game_over:
            return False, "Игра окончена"
        
        current_player = self.get_current_player()
        
        unique_moves = list(dict.fromkeys(self.pending_moves))
        valid_moves = [(x, y) for x, y in unique_moves if self.board.is_empty(x, y)]

        for x, y in valid_moves:
            self.board.place_figure(x, y, current_player.player_id)

        self.pending_moves.clear()
        self.last_player_index = self.current_player_index
        return True, "OK"

    def advance_turn(self) -> Tuple[bool, str]:
        if self.game_over:
            return False, "Игра окончена"
        if len(self.eliminated) >= len(self.players):
            return False, "Игра окончена"
        attempts = 0
        while attempts < len(self.players):
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            if self.current_player_index not in self.eliminated:
                return True, "OK"
            attempts += 1
        return False, "Игра окончена"

    def check_winner(self) -> Tuple[bool, str]:
        if self.game_over:
            return False, "Игра окончена"
        if self.last_player_index is None:
            return False, "OK"
        player = self.players[self.last_player_index]
        for y in range(self.board.height):
            for x in range(self.board.width):
                if self.board.get_cell(x, y) == player.player_id:
                    win_cells = self.board.check_win_at(x, y, player.player_id, self.win_patterns)
                    if win_cells:
                        self.winner = player
                        self.winning_cells = win_cells
                        self.game_over = True
                        return True, "OK"
        return False, "OK"

    def skip_turn(self) -> Tuple[bool, str]:
        if self.game_over:
            return False, "Игра окончена"
        
        self.pending_moves.clear()
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return True, "Ход пропущен"
    
    def reset(self):
        self.board.reset()
        self.current_player_index = 0
        self.pending_moves.clear()
        self.winner = None
        self.winning_cells = []
        self.is_draw = False
        self.game_over = False
        self.last_player_index = None
        self.eliminated.clear()
    
    def parse_coordinate(self, coord_str: str) -> Optional[Tuple[int, int]]:
        coord_str = coord_str.strip().upper()
        if len(coord_str) < 2:
            return None
        
        try:
            col_part = ""
            row_part = ""
            for i, char in enumerate(coord_str):
                if char.isalpha():
                    col_part += char
                else:
                    row_part = coord_str[i:]
                    break
            
            if not col_part or not row_part:
                return None
            
            x = 0
            for char in col_part:
                x = x * 26 + (ord(char) - ord('A') + 1)
            x -= 1
            
            y = int(row_part) - 1
            
            if self.board.is_valid_position(x, y):
                return (x, y)
            return None
        except (ValueError, IndexError):
            return None
