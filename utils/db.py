import sqlite3
from pathlib import Path

from config import DATABASE, SCHEMA_PATH


def get_db_connection():
    """Return a SQLite connection with Row factory enabled."""
    # Ensure DATABASE is a string path for sqlite3
    db_path = Path(DATABASE)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize the database if it does not exist using schema.sql."""
    db_path = Path(DATABASE)

    if not db_path.exists():
        conn = get_db_connection()
        schema_path = Path(SCHEMA_PATH)
        with schema_path.open("r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.close()
