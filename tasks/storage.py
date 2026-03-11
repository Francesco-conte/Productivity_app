"""JSON file persistence for tasks."""

import json
import os

from tasks.models import Task

DEFAULT_FILE = "tasks.json"


def load_tasks(filepath=DEFAULT_FILE):
    """Load tasks from a JSON file. Returns a list of Task objects."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task.from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError):
        print(f"Warning: Could not read '{filepath}'. Starting with an empty task list.")
        return []


def save_tasks(tasks, filepath=DEFAULT_FILE):
    """Save a list of Task objects to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=2, ensure_ascii=False)
