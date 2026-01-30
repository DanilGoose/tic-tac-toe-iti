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


AVAILABLE_FIGURES = ["X", "O", "▲", "■", "◆", "●", "★", "✚", "✖", "◇"]

AVAILABLE_COLORS = [
    (255, 0, 0),
    (0, 0, 255),
    (0, 200, 0),
    (255, 165, 0),
    (160, 60, 200),
    (0, 170, 180),
    (255, 215, 0),
    (255, 105, 180),
    (140, 90, 40),
    (200, 200, 200),
]

COLOR_NAMES = {
    (255, 0, 0): "Красный",
    (0, 0, 255): "Синий",
    (0, 200, 0): "Зелёный",
    (255, 165, 0): "Оранжевый",
    (160, 60, 200): "Фиолетовый",
    (0, 170, 180): "Бирюзовый",
    (255, 215, 0): "Жёлтый",
    (255, 105, 180): "Розовый",
    (140, 90, 40): "Коричневый",
    (200, 200, 200): "Серый",
}

MAX_PLAYERS = min(len(AVAILABLE_FIGURES), len(AVAILABLE_COLORS))
