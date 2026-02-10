import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# SQLite database path
DATABASE = BASE_DIR / "database" / "attendance.db"

# Path to the schema file used to initialize the database
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

# Flask secret key (for sessions and security)
# In production, override this with an environment variable.
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here")
