"""SQLite database persistence for tasks."""

import sqlite3
import uuid
from datetime import datetime

from tasks.models import DATE_FMT, Task

DEFAULT_DB = "studywizz.db"


def get_connection(db_path=DEFAULT_DB):
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=DEFAULT_DB):
    """Create the tasks table if it does not exist."""
    conn = get_connection(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            task_id    TEXT PRIMARY KEY,
            title      TEXT NOT NULL,
            description TEXT DEFAULT '',
            priority   TEXT DEFAULT 'medium',
            due_date   TEXT,
            status     TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def load_tasks_db(db_path=DEFAULT_DB):
    """Load all tasks from the database. Returns a list of Task objects."""
    conn = get_connection(db_path)
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [
        Task(
            title=row["title"],
            description=row["description"],
            priority=row["priority"],
            due_date=row["due_date"],
            status=row["status"],
            task_id=row["task_id"],
            created_at=row["created_at"],
        )
        for row in rows
    ]


def save_task_db(task, db_path=DEFAULT_DB):
    """Insert or replace a single task in the database."""
    conn = get_connection(db_path)
    conn.execute(
        """
        INSERT OR REPLACE INTO tasks
            (task_id, title, description, priority, due_date, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            task.task_id,
            task.title,
            task.description,
            task.priority,
            task.due_date,
            task.status,
            task.created_at,
        ),
    )
    conn.commit()
    conn.close()


def delete_task_db(task_id, db_path=DEFAULT_DB):
    """Delete a task by its ID."""
    conn = get_connection(db_path)
    conn.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
    conn.commit()
    conn.close()


def update_task_status_db(task_id, status, db_path=DEFAULT_DB):
    """Update the status of a task."""
    conn = get_connection(db_path)
    conn.execute(
        "UPDATE tasks SET status = ? WHERE task_id = ?",
        (status, task_id),
    )
    conn.commit()
    conn.close()
