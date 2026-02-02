import argparse
import arcade
from game.board import MIN_BOARD_SIZE, MAX_BOARD_SIZE
from game.player import MAX_PLAYERS
from game.settings import get_default_settings
from game.player_db import init_db
from ui.menu_view import MenuView


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Крестики-нолики ИТИ"


class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title: str, settings: dict):
        super().__init__(width, height, title, resizable=True)
        self.game_settings = settings
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)


def main():
    parser = argparse.ArgumentParser(description="Крестики-Нолики (5 в ряд)")
    parser.add_argument("--width", type=int, default=20, help=f"Ширина поля ({MIN_BOARD_SIZE}-{MAX_BOARD_SIZE})")
    parser.add_argument("--height", type=int, default=20, help=f"Высота поля ({MIN_BOARD_SIZE}-{MAX_BOARD_SIZE})")
    parser.add_argument("--players", type=int, default=0, choices=range(0, MAX_PLAYERS + 1), help="Количество игроков")
    args = parser.parse_args()

    init_db()
    settings = get_default_settings()
    settings["width"] = max(MIN_BOARD_SIZE, min(MAX_BOARD_SIZE, args.width))
    settings["height"] = max(MIN_BOARD_SIZE, min(MAX_BOARD_SIZE, args.height))
    settings["player_count"] = args.players

    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, settings)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
