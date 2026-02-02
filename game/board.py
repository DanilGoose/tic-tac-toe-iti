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
            
            raw_cells = pattern.get("cells", [])
            pattern_cells = []
            for cell in raw_cells:
                if cell is None or len(cell) != 2:
                    continue
                try:
                    cx = int(cell[0])
                    cy = int(cell[1])
                except (TypeError, ValueError):
                    continue
                pattern_cells.append((cx, cy))
            if not pattern_cells:
                continue

            normalized = normalize_pattern(pattern_cells)
            line_info = self._get_line_info(normalized)
            if line_info:
                dx, dy, length = line_info
                if self.grid[y][x] == player_id:
                    total = 1 + self.count_in_direction(x, y, dx, dy, player_id) + self.count_in_direction(x, y, -dx, -dy, player_id)
                    if total >= length:
                        start_x = x - dx * self.count_in_direction(x, y, -dx, -dy, player_id)
                        start_y = y - dy * self.count_in_direction(x, y, -dx, -dy, player_id)
                        winning_cells = []
                        cx, cy = start_x, start_y
                        for _ in range(total):
                            winning_cells.append((cx, cy))
                            cx += dx
                            cy += dy
                        return winning_cells[:length]
            
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

    def _get_line_info(self, cells: List[Tuple[int, int]]) -> Optional[Tuple[int, int, int]]:
        if len(cells) < 2:
            return None
        xs = [x for x, _ in cells]
        ys = [y for _, y in cells]
        length = len(cells)
        if all(y == ys[0] for y in ys):
            xs_sorted = sorted(set(xs))
            if len(xs_sorted) == length and xs_sorted == list(range(xs_sorted[0], xs_sorted[0] + length)):
                return (1, 0, length)
        if all(x == xs[0] for x in xs):
            ys_sorted = sorted(set(ys))
            if len(ys_sorted) == length and ys_sorted == list(range(ys_sorted[0], ys_sorted[0] + length)):
                return (0, 1, length)
        if all((x - y) == (xs[0] - ys[0]) for x, y in cells):
            points = sorted(cells, key=lambda p: p[0])
            if all(points[i + 1][0] - points[i][0] == 1 and points[i + 1][1] - points[i][1] == 1 for i in range(length - 1)):
                return (1, 1, length)
        if all((x + y) == (xs[0] + ys[0]) for x, y in cells):
            points = sorted(cells, key=lambda p: p[0])
            if all(points[i + 1][0] - points[i][0] == 1 and points[i + 1][1] - points[i][1] == -1 for i in range(length - 1)):
                return (1, -1, length)
        return None
