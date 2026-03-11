"""Task data model."""

import uuid
from datetime import datetime

PRIORITIES = ("low", "medium", "high")
STATUSES = ("pending", "completed")

DATE_FMT = "%Y-%m-%d"


class Task:
    """Represents a single task."""

    def __init__(
        self,
        title,
        description="",
        priority="medium",
        due_date=None,
        status="pending",
        task_id=None,
        created_at=None,
    ):
        if priority not in PRIORITIES:
            raise ValueError(f"Priority must be one of {PRIORITIES}")
        if status not in STATUSES:
            raise ValueError(f"Status must be one of {STATUSES}")

        self.task_id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date  # stored as "YYYY-MM-DD" string or None
        self.status = status
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self):
        """Convert task to a JSON-serialisable dictionary."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task from a dictionary (e.g. loaded from JSON)."""
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date"),
            status=data.get("status", "pending"),
            task_id=data.get("task_id"),
            created_at=data.get("created_at"),
        )

    def is_overdue(self):
        """Return True if the task has a due date in the past and is still pending."""
        if not self.due_date or self.status == "completed":
            return False
        today = datetime.now().date()
        try:
            due = datetime.strptime(self.due_date, DATE_FMT).date()
            return due < today
        except ValueError:
            return False

    def is_due_today(self):
        """Return True if the task is due today."""
        if not self.due_date:
            return False
        today = datetime.now().date()
        try:
            due = datetime.strptime(self.due_date, DATE_FMT).date()
            return due == today
        except ValueError:
            return False
