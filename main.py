import argparse
from pathlib import Path
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
        self._music_sound = None
        self._music_player = None
        self._start_music()

    def _start_music(self):
        music_path = Path(__file__).resolve().parent / "assets" / "music.mp3"
        if not music_path.exists():
            return
        try:
            volume = self._normalize_volume(self.game_settings.get("music_volume", 0.12))
            self._music_sound = arcade.load_sound(music_path, streaming=True)
            self._music_player = self._music_sound.play(volume=volume, loop=True)
        except Exception:
            self._music_sound = None
            self._music_player = None

    def _normalize_volume(self, volume: float) -> float:
        try:
            volume = float(volume)
        except (TypeError, ValueError):
            volume = 0.12
        return max(0.0, min(1.0, volume))

    def set_music_volume(self, volume: float):
        volume = self._normalize_volume(volume)
        self.game_settings["music_volume"] = volume
        if self._music_player:
            try:
                self._music_player.volume = volume
            except Exception:
                pass

    def show_view_fade(self, view: arcade.View, duration: float = 0.25):
        from ui.fade_out_view import FadeOutView
        current = self.current_view
        if current is None:
            self.show_view(view)
            return
        self.show_view(FadeOutView(current, view, duration=duration))


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
