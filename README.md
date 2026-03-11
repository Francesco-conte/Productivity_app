# 📋 Daily Task Manager

A simple, interactive command-line application for managing your daily tasks — built entirely with Python's standard library.

## Features

- ➕ **Add tasks** with a title, optional description, priority (low / medium / high), and optional due date
- 📋 **View all tasks** sorted by due date or priority
- 📅 **View today's tasks** — see what's due today and any overdue items
- ✅ **Mark tasks as completed**
- ✏️ **Edit tasks** — update any field at any time
- 🗑️ **Delete tasks**
- 🔍 **Filter tasks** by status (pending / completed) and/or priority
- 📊 **Daily summary** — overview of pending, completed, and overdue tasks

## Requirements

- Python 3.7+
- No external dependencies (uses only the standard library: `json`, `datetime`, `os`, `uuid`, `sys`)

## Getting Started

Clone or download this repository, then run:

```bash
python task_manager.py
```

That's it — no installation or virtual environment needed.

## File Structure

```
Productivity_app/
├── README.md           # This file
├── task_manager.py     # Main entry point — run this!
├── requirements.txt    # No external dependencies
└── tasks/
    ├── __init__.py
    ├── models.py       # Task data model
    ├── storage.py      # JSON file persistence (tasks.json)
    └── utils.py        # Formatting, date parsing, sorting/filtering helpers
```

Tasks are stored locally in a `tasks.json` file (created automatically on first run).

## Menu Options

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
