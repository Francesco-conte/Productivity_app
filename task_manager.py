#!/usr/bin/env python3
"""Daily Task Manager — main entry point."""

import sys
from datetime import datetime

from tasks.models import PRIORITIES, Task
from tasks.storage import load_tasks, save_tasks
from tasks.utils import colour, filter_tasks, format_task, parse_date, prompt, sort_tasks

TASKS_FILE = "tasks.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def divider(char="=", width=40):
    return char * width


def header(title):
    print()
    print(colour(divider(), "cyan"))
    print(colour(f"  {title}", "cyan", "bold"))
    print(colour(divider(), "cyan"))


def pause():
    input("\nPress Enter to continue...")


def find_task(tasks, task_id):
    """Return (index, task) for the given task_id, or (None, None)."""
    for i, t in enumerate(tasks):
        if t.task_id == task_id:
            return i, t
    return None, None


def select_task(tasks):
    """
    Show the task list and ask the user to enter a task ID.
    Returns the (index, task) tuple or (None, None).
    """
    if not tasks:
        print(colour("No tasks available.", "yellow"))
        return None, None
    for i, t in enumerate(tasks, start=1):
        print(format_task(t, index=i))
        print()
    task_id = input("Enter task ID (or press Enter to cancel): ").strip()
    if not task_id:
        return None, None
    idx, task = find_task(tasks, task_id)
    if task is None:
        print(colour("Task not found.", "red"))
    return idx, task


# ---------------------------------------------------------------------------
# Feature functions
# ---------------------------------------------------------------------------

def add_task(tasks):
    header("Add a New Task")
    title = prompt("Title")
    if not title:
        print(colour("Title cannot be empty.", "red"))
        return tasks

    description = prompt("Description", default="")
    priority = prompt("Priority", default="medium", choices=list(PRIORITIES))

    due_date = None
    while True:
        raw = prompt("Due date (YYYY-MM-DD)", default="")
        try:
            due_date = parse_date(raw)
            break
        except ValueError as e:
            print(colour(str(e), "red"))

    task = Task(title=title, description=description, priority=priority, due_date=due_date)
    tasks.append(task)
    save_tasks(tasks, TASKS_FILE)
    print(colour(f"\n✓ Task '{title}' added (ID: {task.task_id})", "green"))
    return tasks


def view_tasks(tasks, sort_by="due_date", title="All Tasks"):
    header(title)
    if not tasks:
        print(colour("No tasks found.", "yellow"))
        return

    sorted_tasks = sort_tasks(tasks, by=sort_by)
    for i, t in enumerate(sorted_tasks, start=1):
        print(format_task(t, index=i))
        print()
    print(f"Total: {len(sorted_tasks)} task(s)")


def view_today_tasks(tasks):
    header("Today's Tasks")
    today = datetime.now().strftime("%Y-%m-%d")
    today_tasks = [t for t in tasks if t.due_date == today]
    overdue_tasks = [t for t in tasks if t.is_overdue()]

    print(colour("--- Due Today ---", "bold"))
    if today_tasks:
        for i, t in enumerate(today_tasks, start=1):
            print(format_task(t, index=i))
            print()
    else:
        print(colour("  No tasks due today.", "yellow"))

    print(colour("\n--- Overdue ---", "red", "bold"))
    if overdue_tasks:
        for i, t in enumerate(overdue_tasks, start=1):
            print(format_task(t, index=i))
            print()
    else:
        print(colour("  No overdue tasks.", "green"))


def complete_task(tasks):
    header("Mark Task as Completed")
    idx, task = select_task(tasks)
    if task is None:
        return tasks

    if task.status == "completed":
        print(colour("Task is already completed.", "yellow"))
        return tasks

    tasks[idx].status = "completed"
    save_tasks(tasks, TASKS_FILE)
    print(colour(f"\n✓ Task '{task.title}' marked as completed.", "green"))
    return tasks


def edit_task(tasks):
    header("Edit a Task")
    idx, task = select_task(tasks)
    if task is None:
        return tasks

    print(colour("\nLeave a field blank to keep the current value.", "cyan"))

    new_title = prompt(f"Title", default=task.title)
    new_description = prompt("Description", default=task.description)
    new_priority = prompt("Priority", default=task.priority, choices=list(PRIORITIES))

    new_due_date = task.due_date
    while True:
        raw = prompt("Due date (YYYY-MM-DD, or clear with '-')", default=task.due_date or "")
        if raw == "-":
            new_due_date = None
            break
        try:
            new_due_date = parse_date(raw)
            break
        except ValueError as e:
            print(colour(str(e), "red"))

    tasks[idx].title = new_title
    tasks[idx].description = new_description
    tasks[idx].priority = new_priority
    tasks[idx].due_date = new_due_date
    save_tasks(tasks, TASKS_FILE)
    print(colour(f"\n✓ Task '{new_title}' updated.", "green"))
    return tasks


def delete_task(tasks):
    header("Delete a Task")
    idx, task = select_task(tasks)
    if task is None:
        return tasks

    confirm = prompt(f"Delete '{task.title}'? This cannot be undone", choices=["y", "n"])
    if confirm == "y":
        tasks.pop(idx)
        save_tasks(tasks, TASKS_FILE)
        print(colour(f"\n✓ Task deleted.", "green"))
    else:
        print("Cancelled.")
    return tasks


def filter_menu(tasks):
    header("Filter Tasks")
    print("1. Filter by status")
    print("2. Filter by priority")
    print("3. Filter by status AND priority")
    choice = prompt("Choice", choices=["1", "2", "3"])

    status = None
    priority = None

    if choice in ("1", "3"):
        status = prompt("Status", choices=["pending", "completed"])
    if choice in ("2", "3"):
        priority = prompt("Priority", choices=list(PRIORITIES))

    result = filter_tasks(tasks, status=status, priority=priority)

    sort_by = prompt("Sort by", default="due_date", choices=["due_date", "priority"])
    view_tasks(result, sort_by=sort_by, title="Filtered Tasks")


def daily_summary(tasks):
    header("Daily Summary")
    today = datetime.now().strftime("%Y-%m-%d")
    today_tasks = [t for t in tasks if t.due_date == today]
    overdue_tasks = [t for t in tasks if t.is_overdue()]
    pending_tasks = [t for t in tasks if t.status == "pending"]
    completed_tasks = [t for t in tasks if t.status == "completed"]

    print(f"  Date           : {colour(today, 'bold')}")
    print(f"  Total tasks    : {len(tasks)}")
    print(f"  Pending        : {colour(str(len(pending_tasks)), 'yellow')}")
    print(f"  Completed      : {colour(str(len(completed_tasks)), 'green')}")
    print(f"  Due today      : {colour(str(len(today_tasks)), 'cyan')}")
    print(f"  Overdue        : {colour(str(len(overdue_tasks)), 'red')}")

    if overdue_tasks:
        print(colour("\n  ⚠  Overdue tasks:", "red", "bold"))
        for t in overdue_tasks:
            print(f"     - {t.title} (due {t.due_date})")
    if today_tasks:
        print(colour("\n  📅 Due today:", "cyan", "bold"))
        for t in today_tasks:
            icon = "✓" if t.status == "completed" else "○"
            print(f"     {icon} {t.title}")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

MENU = """
{divider}
  {title}
{divider}
  1. Add a new task
  2. View all tasks
  3. View today's tasks
  4. Mark task as completed
  5. Edit a task
  6. Delete a task
  7. Filter tasks
  8. Daily summary
  9. Exit
{divider}
""".strip()


def show_menu():
    width = 33
    print()
    print(colour("=" * width, "cyan"))
    print(colour("  Daily Task Manager", "cyan", "bold"))
    print(colour("=" * width, "cyan"))
    print("  1. Add a new task")
    print("  2. View all tasks")
    print("  3. View today's tasks")
    print("  4. Mark task as completed")
    print("  5. Edit a task")
    print("  6. Delete a task")
    print("  7. Filter tasks")
    print("  8. Daily summary")
    print("  9. Exit")
    print(colour("=" * width, "cyan"))


def main():
    tasks = load_tasks(TASKS_FILE)

    while True:
        show_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            tasks = add_task(tasks)
            pause()
        elif choice == "2":
            sort_by = prompt(
                "Sort by", default="due_date", choices=["due_date", "priority"]
            )
            view_tasks(tasks, sort_by=sort_by)
            pause()
        elif choice == "3":
            view_today_tasks(tasks)
            pause()
        elif choice == "4":
            tasks = complete_task(tasks)
            pause()
        elif choice == "5":
            tasks = edit_task(tasks)
            pause()
        elif choice == "6":
            tasks = delete_task(tasks)
            pause()
        elif choice == "7":
            filter_menu(tasks)
            pause()
        elif choice == "8":
            daily_summary(tasks)
            pause()
        elif choice == "9":
            print(colour("\nGoodbye! Stay productive. 👋\n", "cyan", "bold"))
            sys.exit(0)
        else:
            print(colour("Invalid choice. Please enter a number between 1 and 9.", "red"))


if __name__ == "__main__":
    main()
