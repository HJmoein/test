"""
Asynchronous SQLite access using aiosqlite (non-blocking).
"""

import logging
from pathlib import Path
from datetime import datetime, timezone

import aiosqlite

from app import config

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """Initialize database and create users table if not exists."""
    db_path = Path(config.DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_city TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        await db.commit()
    logger.info(f"Database initialized at {db_path}")


async def upsert_user(user_id: int, username: str | None, first_name: str | None, last_city: str | None = None) -> None:
    """Insert or update user. Updates updated_at, preserves created_at on update."""
    now = datetime.now(timezone.utc).isoformat()
    db_path = config.DB_PATH

    async with aiosqlite.connect(db_path) as db:
        # Check if exists
        async with db.execute("SELECT user_id, created_at FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()

        if row is None:
            # Insert
            await db.execute(
                """
                INSERT INTO users (user_id, username, first_name, last_city, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, username, first_name, last_city, now, now),
            )
        else:
            # Update
            created_at = row[1]
            # Keep last_city if not provided
            if last_city is None:
                async with db.execute("SELECT last_city FROM users WHERE user_id = ?", (user_id,)) as c2:
                    existing = await c2.fetchone()
                    last_city = existing[0] if existing else None

            await db.execute(
                """
                UPDATE users
                SET username = ?, first_name = ?, last_city = ?, updated_at = ?
                WHERE user_id = ?
                """,
                (username, first_name, last_city, now, user_id),
            )

            # Ensure created_at not overwritten (already preserved)
            _ = created_at

        await db.commit()


async def update_last_city(user_id: int, city: str) -> None:
    """Update last_city for user, creates user row if not exists (minimal)."""
    now = datetime.now(timezone.utc).isoformat()
    db_path = config.DB_PATH

    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()

        if row is None:
            await db.execute(
                """
                INSERT INTO users (user_id, username, first_name, last_city, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, None, None, city, now, now),
            )
        else:
            await db.execute(
                "UPDATE users SET last_city = ?, updated_at = ? WHERE user_id = ?",
                (city, now, user_id),
            )
        await db.commit()


async def get_user(user_id: int) -> dict | None:
    """Get user by id."""
    db_path = config.DB_PATH
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return dict(row)
            return None
