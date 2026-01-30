from typing import Optional, List, Tuple, Set

MIN_BOARD_SIZE = 5
MAX_BOARD_SIZE = 50

_transformation_cache = {}
_offset_cache = {}


def get_pattern_transformations_cached(cells_tuple: Tuple[Tuple[int, int], ...]) -> List[Tuple[Tuple[int, int], ...]]:
    if cells_tuple in _transformation_cache:
        return _transformation_cache[cells_tuple]
    
    cells = list(cells_tuple)
    seen = set()
    transformations = []
    current = cells
    
    for _ in range(4):
        key = _normalize_to_tuple(current)
        if key not in seen:
            seen.add(key)
            transformations.append(key)
        
        current = [(-y, x) for x, y in current]
    
    current = [(-x, y) for x, y in cells]
    for _ in range(4):
        key = _normalize_to_tuple(current)
        if key not in seen:
            seen.add(key)
            transformations.append(key)
        
        current = [(-y, x) for x, y in current]
    
    _transformation_cache[cells_tuple] = transformations
    
    for t in transformations:
        if t not in _offset_cache:
            _offset_cache[t] = set(t)
    
    return transformations


def _normalize_to_tuple(cells: List[Tuple[int, int]]) -> Tuple[Tuple[int, int], ...]:
    if not cells:
        return tuple()
    min_x = min(x for x, y in cells)
    min_y = min(y for x, y in cells)
    return tuple(sorted((x - min_x, y - min_y) for x, y in cells))


def get_pattern_transformations(cells: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    cells_tuple = tuple(sorted(cells))
    cached = get_pattern_transformations_cached(cells_tuple)
    return [list(t) for t in cached]


def normalize_pattern(cells: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not cells:
        return cells
    min_x = min(x for x, y in cells)
    min_y = min(y for x, y in cells)
    return sorted((x - min_x, y - min_y) for x, y in cells)


class Board:
    def __init__(self, width: int, height: int):
        self.width = max(MIN_BOARD_SIZE, min(width, MAX_BOARD_SIZE))
        self.height = max(MIN_BOARD_SIZE, min(height, MAX_BOARD_SIZE))
        self.grid: List[List[Optional[int]]] = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]
    
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_empty(self, x: int, y: int) -> bool:
        if not self.is_valid_position(x, y):
            return False
        return self.grid[y][x] is None
    
    def get_cell(self, x: int, y: int) -> Optional[int]:
        if not self.is_valid_position(x, y):
            return None
        return self.grid[y][x]
    
    def place_figure(self, x: int, y: int, player_id: int) -> bool:
        if not self.is_valid_position(x, y):
            return False
        if not self.is_empty(x, y):
            return False
        self.grid[y][x] = player_id
        return True
    
    def is_full(self) -> bool:
        for row in self.grid:
            for cell in row:
                if cell is None:
                    return False
        return True
    
    def reset(self):
        self.grid = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]
    
    def count_in_direction(self, x: int, y: int, dx: int, dy: int, player_id: int) -> int:
        count = 0
        cx, cy = x + dx, y + dy
        while self.is_valid_position(cx, cy) and self.grid[cy][cx] == player_id:
            count += 1
            cx += dx
            cy += dy
        return count
    
    def check_win_at(self, x: int, y: int, player_id: int, patterns: List[dict] = None) -> Optional[List[Tuple[int, int]]]:
        if patterns is None:
            patterns = [
                {"enabled": True, "cells": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]},
                {"enabled": True, "cells": [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]}
            ]
        
        grid = self.grid
        width = self.width
        height = self.height
        
        for pattern in patterns:
            if not pattern.get("enabled", True):
                continue
            
            pattern_cells = pattern.get("cells", [])
            if not pattern_cells:
                continue
            
            cells_tuple = tuple(sorted(pattern_cells))
            transformations = get_pattern_transformations_cached(cells_tuple)
            pattern_size = len(pattern_cells)
            
            for transformed in transformations:
                for offset_x, offset_y in transformed:
                    base_x = x - offset_x
                    base_y = y - offset_y
                    
                    if base_x < 0 or base_y < 0:
                        continue
                    
                    match = True
                    winning_cells = []
                    
                    for px, py in transformed:
                        check_x = base_x + px
                        check_y = base_y + py
                        
                        if check_x >= width or check_y >= height:
                            match = False
                            break
                        
                        if grid[check_y][check_x] != player_id:
                            match = False
                            break
                        
                        winning_cells.append((check_x, check_y))
                    
                    if match and len(winning_cells) == pattern_size:
                        return winning_cells
        
        return None
