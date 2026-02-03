import os
import sqlite3
from typing import List, Tuple, Optional, Dict

from game.player import MAX_PLAYERS


APP_NAME = "tic-tac-toe-iti"
_DB_PATH_CACHE: Optional[str] = None


def _candidate_base_dirs() -> List[str]:
    override_dir = os.environ.get("TICTACTOE_DATA_DIR")
    candidates = []
    if override_dir:
        candidates.append(override_dir)
    candidates.extend(
        [
            os.environ.get("LOCALAPPDATA"),
            os.environ.get("APPDATA"),
            os.environ.get("USERPROFILE"),
            os.environ.get("TEMP"),
            os.getcwd(),
        ]
    )
    return [c for c in candidates if c]


def get_db_path() -> str:
    if _DB_PATH_CACHE:
        return _DB_PATH_CACHE
    for base_dir in _candidate_base_dirs():
        db_dir = os.path.join(base_dir, APP_NAME)
        try:
            os.makedirs(db_dir, exist_ok=True)
            return os.path.join(db_dir, "players.db")
        except OSError:
            continue
    return os.path.join(os.getcwd(), "players.db")


def _connect() -> sqlite3.Connection:
    global _DB_PATH_CACHE
    if _DB_PATH_CACHE:
        return sqlite3.connect(_DB_PATH_CACHE)

    last_error = None
    for base_dir in _candidate_base_dirs():
        db_dir = os.path.join(base_dir, APP_NAME)
        try:
            os.makedirs(db_dir, exist_ok=True)
        except OSError as e:
            last_error = e
            continue
        db_path = os.path.join(db_dir, "players.db")
        try:
            conn = sqlite3.connect(db_path)
            # Probe write access early (helps when running from a bundled .exe).
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("CREATE TABLE IF NOT EXISTS __codex_probe (id INTEGER)")
            conn.commit()
            _DB_PATH_CACHE = db_path
            return conn
        except sqlite3.OperationalError as e:
            last_error = e
            try:
                conn.close()
            except Exception:
                pass
            continue
    raise sqlite3.OperationalError(f"unable to open database file: {last_error}")


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


def delete_player(name: str) -> Tuple[bool, str]:
    normalized = _normalize_name(name)
    if not normalized:
        return False, "Укажите имя игрока."
    init_db()
    with _connect() as conn:
        cur = conn.execute(
            "DELETE FROM players WHERE lower(name) = lower(?)",
            (normalized,),
        )
        conn.commit()
    if cur.rowcount == 0:
        return False, "Игрок не найден."
    return True, ""


def rename_player(old_name: str, new_name: str) -> Tuple[bool, str]:
    old_normalized = _normalize_name(old_name)
    new_normalized = _normalize_name(new_name)
    if not old_normalized:
        return False, "Укажите имя игрока."
    if not new_normalized:
        return False, "Введите новое имя."
    init_db()
    with _connect() as conn:
        current = conn.execute(
            "SELECT name FROM players WHERE lower(name) = lower(?) LIMIT 1",
            (old_normalized,),
        ).fetchone()
        if not current:
            return False, "Игрок не найден."
        existing = conn.execute(
            "SELECT 1 FROM players WHERE lower(name) = lower(?) LIMIT 1",
            (new_normalized,),
        ).fetchone()
        if existing and current[0].lower() != new_normalized.lower():
            return False, "Игрок с таким именем уже существует."
        try:
            conn.execute(
                "UPDATE players SET name = ? WHERE lower(name) = lower(?)",
                (new_normalized, old_normalized),
            )
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
