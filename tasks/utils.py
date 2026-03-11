"""Helper functions for formatting and date parsing."""

from datetime import datetime

from tasks.models import DATE_FMT, PRIORITIES

# Priority sort order (higher value = higher urgency)
PRIORITY_ORDER = {"high": 3, "medium": 2, "low": 1}

# Colour codes for terminal output
COLOURS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}


def colour(text, *codes):
    """Wrap text with ANSI colour codes."""
    prefix = "".join(COLOURS.get(c, "") for c in codes)
    return f"{prefix}{text}{COLOURS['reset']}"


def parse_date(date_str):
    """
    Parse a date string in YYYY-MM-DD format.
    Returns the string if valid, or None if empty.
    Raises ValueError if the format is wrong.
    """
    if not date_str or date_str.strip() == "":
        return None
    date_str = date_str.strip()
    try:
        datetime.strptime(date_str, DATE_FMT)
        return date_str
    except ValueError:
        raise ValueError(f"Invalid date '{date_str}'. Expected format: YYYY-MM-DD.")


def format_task(task, index=None):
    """Return a formatted multi-line string representing a task."""
    prefix = f"{index}. " if index is not None else "   "
    status_icon = colour("✓", "green") if task.status == "completed" else colour("○", "yellow")

    priority_colours = {"high": ("red", "bold"), "medium": ("yellow",), "low": ("cyan",)}
    p_colours = priority_colours.get(task.priority, ("white",))
    priority_str = colour(task.priority.upper(), *p_colours)

    due_str = task.due_date or "No due date"
    if task.is_overdue():
        due_str = colour(f"{task.due_date} (OVERDUE)", "red", "bold")
    elif task.is_due_today():
        due_str = colour(f"{task.due_date} (TODAY)", "green", "bold")

    lines = [
        f"{prefix}{colour(task.title, 'bold')} [{status_icon}]",
        f"     ID       : {task.task_id}",
        f"     Priority : {priority_str}",
        f"     Due      : {due_str}",
        f"     Status   : {task.status}",
        f"     Created  : {task.created_at}",
    ]
    if task.description:
        lines.append(f"     Desc     : {task.description}")
    return "\n".join(lines)


def sort_tasks(tasks, by="due_date"):
    """
    Sort tasks.
    by='due_date'  — tasks without a due date go last
    by='priority'  — highest priority first
    """
    if by == "priority":
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 0), reverse=True)
    # default: due_date
    def due_key(t):
        if not t.due_date:
            return "9999-99-99"
        return t.due_date

    return sorted(tasks, key=due_key)


def filter_tasks(tasks, status=None, priority=None):
    """Filter tasks by optional status and/or priority."""
    result = tasks
    if status:
        result = [t for t in result if t.status == status]
    if priority:
        result = [t for t in result if t.priority == priority]
    return result


def prompt(message, default=None, choices=None):
    """
    Prompt the user for input.
    If default is provided, it is shown in brackets and used when the user
    presses Enter without typing anything.
    If choices is a list, the input is validated against it.
    """
    hint = ""
    if choices:
        hint = f" [{'/'.join(choices)}]"
    if default is not None:
        hint += f" (default: {default})"
    while True:
        value = input(f"{message}{hint}: ").strip()
        if value == "" and default is not None:
            return default
        if choices and value not in choices:
            print(colour(f"Please enter one of: {', '.join(choices)}", "yellow"))
            continue
        return value
