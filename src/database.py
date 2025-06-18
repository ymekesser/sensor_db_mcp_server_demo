from pathlib import Path
import re
import sqlite3


class SqliteDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def query(self, sql: str, safe: bool = True) -> list[dict]:
        """Execute a safe, read-only SQL query and return results as list of dicts."""
        print("Attempting to execute query.")

        if safe and not self._is_safe_query(sql):
            raise ValueError("Only safe SELECT queries are allowed.")

        with sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(sql)
            return [dict(row) for row in cursor.fetchall()]

    def get_table_schema(self, table_name: str) -> list[dict]:
        with sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(f"PRAGMA table_info({table_name})")
            return [dict(row) for row in cursor.fetchall()]

    def _is_safe_query(self, sql: str) -> bool:
        """
        Basic check to ensure the query is read-only.
        It must start with SELECT and not contain keywords like INSERT, UPDATE, DELETE, etc.
        """
        sql_clean = sql.strip().lower()
        forbidden = [
            "insert",
            "update",
            "delete",
            "drop",
            "alter",
            "create",
            "replace",
            "pragma",
            "attach",
            "detach",
        ]
        if not sql_clean.startswith("select"):
            return False
        if any(re.search(rf"\b{kw}\b", sql_clean) for kw in forbidden):
            return False
        return True
