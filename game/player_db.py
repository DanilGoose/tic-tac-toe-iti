import os
import sqlite3
from typing import List, Tuple, Optional, Dict

from game.player import MAX_PLAYERS


DB_PATH = os.path.join(os.path.dirname(__file__), "players.db")


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def _normalize_name(name: str) -> str:
    return " ".join(name.strip().split())


def _default_names() -> List[str]:
    return [f"Игрок {i + 1}" for i in range(MAX_PLAYERS)]


def init_db() -> None:
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                games_played INTEGER NOT NULL DEFAULT 0,
                wins INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        cur.execute("PRAGMA table_info(players)")
        columns = {row[1] for row in cur.fetchall()}
        if "games_played" not in columns:
            cur.execute("ALTER TABLE players ADD COLUMN games_played INTEGER NOT NULL DEFAULT 0")
        if "wins" not in columns:
            cur.execute("ALTER TABLE players ADD COLUMN wins INTEGER NOT NULL DEFAULT 0")
        for name in _default_names():
            cur.execute("DELETE FROM players WHERE name = ?", (name,))
        conn.commit()


def get_player_names() -> List[str]:
    init_db()
    with _connect() as conn:
        rows = conn.execute("SELECT name FROM players ORDER BY name COLLATE NOCASE").fetchall()
    return [row[0] for row in rows]


def player_exists(name: str) -> bool:
    normalized = _normalize_name(name)
    if not normalized:
        return False
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM players WHERE lower(name) = lower(?) LIMIT 1",
            (normalized,),
        ).fetchone()
    return row is not None


def add_player(name: str) -> Tuple[bool, str]:
    normalized = _normalize_name(name)
    if not normalized:
        return False, "Введите имя игрока."
    if player_exists(normalized):
        return False, "Игрок с таким именем уже существует."
    init_db()
    try:
        with _connect() as conn:
            conn.execute("INSERT INTO players(name) VALUES (?)", (normalized,))
            conn.commit()
    except sqlite3.IntegrityError:
        return False, "Игрок с таким именем уже существует."
    return True, ""


def get_player_stats() -> List[Dict[str, int]]:
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT name, games_played, wins
            FROM players
            ORDER BY wins DESC, games_played DESC, name COLLATE NOCASE
            """
        ).fetchall()
    return [{"name": row[0], "games_played": row[1], "wins": row[2]} for row in rows]


def record_game_result(player_names: List[str], winner_name: Optional[str]) -> None:
    normalized_players = [_normalize_name(name) for name in player_names if _normalize_name(name)]
    if not normalized_players:
        return
    init_db()
    with _connect() as conn:
        for name in normalized_players:
            conn.execute(
                "UPDATE players SET games_played = games_played + 1 WHERE lower(name) = lower(?)",
                (name,),
            )
        if winner_name:
            winner_normalized = _normalize_name(winner_name)
            if winner_normalized:
                conn.execute(
                    "UPDATE players SET wins = wins + 1 WHERE lower(name) = lower(?)",
                    (winner_normalized,),
                )
        conn.commit()
