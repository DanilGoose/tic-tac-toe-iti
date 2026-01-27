import argparse
import arcade
from game.player import AVAILABLE_FIGURES, AVAILABLE_COLORS
from ui.menu_view import MenuView


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Крестики-нолики ИТИ"


def get_default_patterns():
    return [
        {
            "name": "Линия 5",
            "enabled": True,
            "cells": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        },
        {
            "name": "Диагональ 5",
            "enabled": True,
            "cells": [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
        }
    ]


def get_default_settings():
    return {
        "width": 15,
        "height": 15,
        "player_count": 2,
        "hide_board_on_win": True,
        "win_patterns": get_default_patterns(),
        "players": [
            {"name": f"Игрок {i + 1}", "figure": AVAILABLE_FIGURES[i], "color": AVAILABLE_COLORS[i]}
            for i in range(4)
        ]
    }


class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title: str, settings: dict):
        super().__init__(width, height, title, resizable=True)
        self.game_settings = settings
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)


def main():
    parser = argparse.ArgumentParser(description="Крестики-Нолики (5 в ряд)")
    parser.add_argument("--width", type=int, default=15, help="Ширина поля (5-30)")
    parser.add_argument("--height", type=int, default=15, help="Высота поля (5-30)")
    parser.add_argument("--players", type=int, default=2, choices=[2, 3, 4], help="Количество игроков")
    args = parser.parse_args()
    
    settings = get_default_settings()
    settings["width"] = max(5, min(30, args.width))
    settings["height"] = max(5, min(30, args.height))
    settings["player_count"] = args.players
    
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, settings)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
