from game.player import AVAILABLE_FIGURES, AVAILABLE_COLORS, MAX_PLAYERS


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
        "width": 20,
        "height": 20,
        "player_count": 0,
        "hide_board_on_win": False,
        "music_volume": 0.2,
        "win_patterns": get_default_patterns(),
        "players": [
            {"name": "", "figure": AVAILABLE_FIGURES[i], "color": AVAILABLE_COLORS[i]}
            for i in range(MAX_PLAYERS)
        ]
    }
