# 📚 StudyWizz — Productivity App

A sleek, dark-mode **GUI productivity app** built with Python and CustomTkinter.
Manage tasks with deadlines and priorities, view them on an interactive calendar, and stay on top of your schedule.

> The original CLI task manager (`task_manager.py`) is still available for terminal use.

## Features

- 📋 **Tasks with deadlines** — ordered by due date, with overdue warnings (⚠)
- ⭐ **Tasks without deadlines** — priority-based tasks with star ratings
- 📅 **Interactive calendar** — month view with task count badges; click any day
- 📊 **Done / Stats views** — review completed tasks and productivity statistics
- 🔄 **Google Calendar sync button** — ready for OAuth integration
- 💾 **SQLite database** — persistent storage via `studywizz.db`
- 🌙 **Dark mode** — minimalistic design with a dark colour scheme

## Requirements

- Python 3.8+
- `customtkinter` (installed via `pip install -r requirements.txt`)

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the GUI app
python studywizz.py

# Or run the original CLI task manager
python task_manager.py
```

## File Structure

```
Productivity_app/
├── README.md           # This file
├── studywizz.py        # GUI app — run this!
├── task_manager.py     # Original CLI task manager
├── requirements.txt    # Python dependencies
└── tasks/
    ├── __init__.py
    ├── models.py       # Task data model
    ├── database.py     # SQLite database persistence (studywizz.db)
    ├── storage.py      # JSON file persistence (tasks.json, for CLI)
    └── utils.py        # Formatting, date parsing, sorting/filtering helpers
```

Tasks are stored in a local `studywizz.db` SQLite database (created automatically on first run).

## CLI Menu Options (task_manager.py)

```
=================================
  Daily Task Manager
=================================
  1. Add a new task
  2. View all tasks
  3. View today's tasks
  4. Mark task as completed
  5. Edit a task
  6. Delete a task
  7. Filter tasks
  8. Daily summary
  9. Exit
=================================
```

## Usage Examples

### Adding a task
```
Title: Finish project report
Description: Include Q1 metrics
Priority [low/medium/high] (default: medium): high
Due date (YYYY-MM-DD): 2026-03-15
✓ Task 'Finish project report' added (ID: ...)
```

### Viewing all tasks
```
1. Finish project report [○]
     ID       : <uuid>
     Priority : HIGH
     Due      : 2026-03-15 (TODAY)
     Status   : pending
     Created  : 2026-03-11 09:00:00
     Desc     : Include Q1 metrics
```

### Daily summary
```
  Date           : 2026-03-11
  Total tasks    : 5
  Pending        : 3
  Completed      : 2
  Due today      : 1
  Overdue        : 0
```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
