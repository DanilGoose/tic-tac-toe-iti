from dataclasses import dataclass
from typing import Tuple


@dataclass
class Player:
    player_id: int
    name: str
    figure: str
    color: Tuple[int, int, int]
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Игрок {self.player_id + 1}"


AVAILABLE_FIGURES = ["X", "O", "▲", "■"]

AVAILABLE_COLORS = [
    (255, 0, 0),
    (0, 0, 255),
    (0, 200, 0),
    (255, 165, 0),
]

COLOR_NAMES = {
    (255, 0, 0): "Красный",
    (0, 0, 255): "Синий",
    (0, 200, 0): "Зелёный",
    (255, 165, 0): "Оранжевый",
}
