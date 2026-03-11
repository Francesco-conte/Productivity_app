#!/usr/bin/env python3
"""StudyWizz — GUI Productivity App."""

import calendar
from datetime import datetime

import customtkinter as ctk

from tasks.database import (
    delete_task_db,
    init_db,
    load_tasks_db,
    save_task_db,
    update_task_status_db,
)
from tasks.models import Task

# ---------------------------------------------------------------------------
# Theme / colours
# ---------------------------------------------------------------------------
BG_DARK = "#0f1123"
BG_PANEL = "#1a1d35"
BG_CARD = "#232848"
BG_INPUT = "#2a2f55"
ACCENT = "#6c63ff"
ACCENT_HOVER = "#5a52e0"
TEXT_PRIMARY = "#e2e2f0"
TEXT_SECONDARY = "#8888aa"
TEXT_MUTED = "#555577"
BORDER_COLOR = "#2e3360"
CAL_TODAY = "#6c63ff"
CAL_SELECTED = "#4444aa"
CAL_HAS_TASKS = "#3a3d65"
WARNING_COLOR = "#ff9f43"
DANGER_COLOR = "#ee5a5a"
SUCCESS_COLOR = "#2ecc71"

FONT_FAMILY = "Segoe UI"

DB_PATH = "studywizz.db"


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------
class StudyWizzApp(ctk.CTk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        # -- Database --
        init_db(DB_PATH)
        self.tasks = load_tasks_db(DB_PATH)

        # -- Window --
        self.title("StudyWizz")
        self.geometry("1200x820")
        self.minsize(1000, 700)
        self.configure(fg_color=BG_DARK)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # -- Calendar state --
        today = datetime.now()
        self.cal_year = today.year
        self.cal_month = today.month
        self.selected_date = today.strftime("%Y-%m-%d")

        self._build_ui()
        self.refresh_all()

    # -----------------------------------------------------------------------
    # UI construction
    # -----------------------------------------------------------------------
    def _build_ui(self):
        self._build_topbar()
        self._build_main_area()

    # -- Top bar -----------------------------------------------------------
    def _build_topbar(self):
        bar = ctk.CTkFrame(self, fg_color=BG_PANEL, corner_radius=0, height=50)
        bar.pack(fill="x", padx=0, pady=0)
        bar.pack_propagate(False)

        # Brand
        brand = ctk.CTkLabel(
            bar,
            text="STUDYWIZZ",
            font=ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        brand.pack(side="left", padx=20)

        # Centre buttons
        centre = ctk.CTkFrame(bar, fg_color="transparent")
        centre.pack(side="left", expand=True)

        self.btn_done = ctk.CTkButton(
            centre,
            text="Done",
            width=70,
            height=30,
            corner_radius=6,
            fg_color="transparent",
            hover_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            command=self._show_done_tasks,
        )
        self.btn_done.pack(side="left", padx=4)

        self.btn_stats = ctk.CTkButton(
            centre,
            text="Stats",
            width=70,
            height=30,
            corner_radius=6,
            fg_color="transparent",
            hover_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            command=self._show_stats,
        )
        self.btn_stats.pack(side="left", padx=4)

        # Right – Sync
        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.pack(side="right", padx=20)

        self.sync_label = ctk.CTkLabel(
            right,
            text="Ready",
            text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
        )
        self.sync_label.pack(side="left", padx=(0, 8))

        self.btn_sync = ctk.CTkButton(
            right,
            text="Sync",
            width=60,
            height=30,
            corner_radius=15,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="#ffffff",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            command=self._sync_google_calendar,
        )
        self.btn_sync.pack(side="left")

    # -- Main area ---------------------------------------------------------
    def _build_main_area(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=16, pady=(10, 16))
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self._build_left_panel(container)
        self._build_right_panel(container)

    # -- Left panel --------------------------------------------------------
    def _build_left_panel(self, parent):
        left = ctk.CTkFrame(parent, fg_color=BG_PANEL, corner_radius=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        inner = ctk.CTkFrame(left, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        # ---- Tasks with deadline -----------------------------------------
        ctk.CTkLabel(
            inner,
            text="Tasks with deadline",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
            text_color=TEXT_PRIMARY,
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        # Add row
        add_row = ctk.CTkFrame(inner, fg_color="transparent")
        add_row.pack(fill="x", pady=(0, 8))

        self.dl_entry = ctk.CTkEntry(
            add_row,
            placeholder_text="Add a deadline task...",
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_MUTED,
            corner_radius=8,
            height=36,
        )
        self.dl_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.dl_date_entry = ctk.CTkEntry(
            add_row,
            width=110,
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            text_color=TEXT_PRIMARY,
            corner_radius=8,
            height=36,
        )
        self.dl_date_entry.pack(side="left", padx=(0, 6))
        self.dl_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ctk.CTkButton(
            add_row,
            text="+",
            width=36,
            height=36,
            corner_radius=8,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="#ffffff",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self._add_deadline_task,
        ).pack(side="left")

        # Scrollable list
        self.dl_scroll = ctk.CTkScrollableFrame(
            inner, fg_color="transparent", corner_radius=0
        )
        self.dl_scroll.pack(fill="both", expand=True, pady=(0, 14))

        # ---- Tasks without deadline --------------------------------------
        ctk.CTkLabel(
            inner,
            text="Tasks without deadline",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
            text_color=TEXT_PRIMARY,
            anchor="w",
        ).pack(fill="x", pady=(6, 10))

        # Add row
        add_row2 = ctk.CTkFrame(inner, fg_color="transparent")
        add_row2.pack(fill="x", pady=(0, 8))

        self.ndl_entry = ctk.CTkEntry(
            add_row2,
            placeholder_text="Add a priority task...",
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_MUTED,
            corner_radius=8,
            height=36,
        )
        self.ndl_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.ndl_priority = ctk.CTkComboBox(
            add_row2,
            values=["★★★★★", "★★★★☆", "★★★☆☆", "★★☆☆☆", "★☆☆☆☆"],
            width=110,
            height=36,
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            button_color=BG_CARD,
            button_hover_color=ACCENT,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=ACCENT,
            text_color=TEXT_PRIMARY,
            corner_radius=8,
        )
        self.ndl_priority.pack(side="left", padx=(0, 6))
        self.ndl_priority.set("★★★☆☆")

        ctk.CTkButton(
            add_row2,
            text="+",
            width=36,
            height=36,
            corner_radius=8,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="#ffffff",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self._add_no_deadline_task,
        ).pack(side="left")

        # Scrollable grid for no-deadline tasks
        self.ndl_scroll = ctk.CTkScrollableFrame(
            inner, fg_color="transparent", corner_radius=0
        )
        self.ndl_scroll.pack(fill="both", expand=True)

    # -- Right panel -------------------------------------------------------
    def _build_right_panel(self, parent):
        right = ctk.CTkFrame(parent, fg_color=BG_PANEL, corner_radius=14)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        inner = ctk.CTkFrame(right, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        # Calendar header
        cal_header = ctk.CTkFrame(inner, fg_color="transparent")
        cal_header.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            cal_header,
            text="Calendar",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        nav = ctk.CTkFrame(cal_header, fg_color="transparent")
        nav.pack(side="right")

        ctk.CTkButton(
            nav,
            text="<",
            width=30,
            height=28,
            corner_radius=6,
            fg_color=BG_CARD,
            hover_color=ACCENT,
            text_color=TEXT_PRIMARY,
            command=self._cal_prev,
        ).pack(side="left", padx=2)

        self.cal_month_label = ctk.CTkLabel(
            nav,
            text="",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=TEXT_PRIMARY,
            width=120,
        )
        self.cal_month_label.pack(side="left", padx=4)

        ctk.CTkButton(
            nav,
            text=">",
            width=30,
            height=28,
            corner_radius=6,
            fg_color=BG_CARD,
            hover_color=ACCENT,
            text_color=TEXT_PRIMARY,
            command=self._cal_next,
        ).pack(side="left", padx=2)

        # Day-of-week headers
        days_row = ctk.CTkFrame(inner, fg_color="transparent")
        days_row.pack(fill="x", pady=(4, 2))
        for i in range(7):
            days_row.grid_columnconfigure(i, weight=1)
        for i, name in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
            ctk.CTkLabel(
                days_row,
                text=name,
                font=ctk.CTkFont(family=FONT_FAMILY, size=11),
                text_color=TEXT_SECONDARY,
            ).grid(row=0, column=i, sticky="ew")

        # Calendar grid
        self.cal_grid = ctk.CTkFrame(inner, fg_color="transparent")
        self.cal_grid.pack(fill="both", expand=True, pady=(0, 10))
        for i in range(7):
            self.cal_grid.grid_columnconfigure(i, weight=1)

        # Events section
        self.events_label = ctk.CTkLabel(
            inner,
            text="Events for ...",
            font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
            text_color=TEXT_PRIMARY,
            anchor="w",
        )
        self.events_label.pack(fill="x", pady=(6, 6))

        self.events_scroll = ctk.CTkScrollableFrame(
            inner, fg_color="transparent", corner_radius=0, height=140
        )
        self.events_scroll.pack(fill="both", expand=False)

    # -----------------------------------------------------------------------
    # Data helpers
    # -----------------------------------------------------------------------
    def _reload_tasks(self):
        self.tasks = load_tasks_db(DB_PATH)

    def _tasks_with_deadline(self):
        pending = [t for t in self.tasks if t.due_date and t.status == "pending"]
        return sorted(pending, key=lambda t: t.due_date)

    def _tasks_without_deadline(self):
        return [t for t in self.tasks if not t.due_date and t.status == "pending"]

    def _tasks_for_date(self, date_str):
        return [t for t in self.tasks if t.due_date == date_str and t.status == "pending"]

    def _tasks_count_by_date(self):
        counts = {}
        for t in self.tasks:
            if t.due_date and t.status == "pending":
                counts[t.due_date] = counts.get(t.due_date, 0) + 1
        return counts

    def _priority_to_stars(self, priority):
        mapping = {"high": "★★★★★", "medium": "★★★☆☆", "low": "★☆☆☆☆"}
        return mapping.get(priority, "★★★☆☆")

    def _stars_to_priority(self, stars):
        star_count = stars.count("★")
        if star_count >= 5:
            return "high"
        elif star_count >= 3:
            return "medium"
        return "low"

    # -----------------------------------------------------------------------
    # Refresh UI
    # -----------------------------------------------------------------------
    def refresh_all(self):
        self._reload_tasks()
        self._refresh_deadline_list()
        self._refresh_no_deadline_list()
        self._refresh_calendar()
        self._refresh_events()

    def _refresh_deadline_list(self):
        for w in self.dl_scroll.winfo_children():
            w.destroy()

        tasks = self._tasks_with_deadline()
        for t in tasks:
            self._make_deadline_card(self.dl_scroll, t)

    def _refresh_no_deadline_list(self):
        for w in self.ndl_scroll.winfo_children():
            w.destroy()

        tasks = self._tasks_without_deadline()
        col_count = 2
        for i, t in enumerate(tasks):
            row = i // col_count
            col = i % col_count
            self.ndl_scroll.grid_columnconfigure(col, weight=1)
            self._make_no_deadline_card(self.ndl_scroll, t, row, col)

    def _make_deadline_card(self, parent, task):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10, height=44)
        card.pack(fill="x", pady=3)

        cb = ctk.CTkCheckBox(
            card,
            text="",
            width=24,
            height=24,
            corner_radius=4,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            border_color=BORDER_COLOR,
            command=lambda tid=task.task_id: self._complete_task(tid),
        )
        cb.pack(side="left", padx=(10, 6), pady=8)

        ctk.CTkLabel(
            card,
            text=task.title,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=TEXT_PRIMARY,
            anchor="w",
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))

        ctk.CTkLabel(
            card,
            text=task.due_date or "",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=TEXT_SECONDARY,
            fg_color=BG_INPUT,
            corner_radius=6,
            width=90,
            height=28,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            card,
            text="×",
            width=28,
            height=28,
            corner_radius=6,
            fg_color="transparent",
            hover_color=DANGER_COLOR,
            text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(size=14),
            command=lambda tid=task.task_id: self._delete_task(tid),
        ).pack(side="left", padx=(0, 4))

        # Warning icon for overdue or upcoming
        if task.is_overdue():
            ctk.CTkLabel(
                card,
                text="⚠",
                font=ctk.CTkFont(size=16),
                text_color=WARNING_COLOR,
            ).pack(side="left", padx=(0, 10))

    def _make_no_deadline_card(self, parent, task, row, col):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10)
        card.grid(row=row, column=col, sticky="ew", padx=3, pady=3)

        cb = ctk.CTkCheckBox(
            card,
            text="",
            width=24,
            height=24,
            corner_radius=4,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            border_color=BORDER_COLOR,
            command=lambda tid=task.task_id: self._complete_task(tid),
        )
        cb.pack(side="left", padx=(10, 4), pady=8)

        ctk.CTkLabel(
            card,
            text=task.title,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=TEXT_PRIMARY,
            anchor="w",
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))

        stars = self._priority_to_stars(task.priority)
        ctk.CTkLabel(
            card,
            text=stars,
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=WARNING_COLOR,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            card,
            text="×",
            width=24,
            height=24,
            corner_radius=6,
            fg_color="transparent",
            hover_color=DANGER_COLOR,
            text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(size=13),
            command=lambda tid=task.task_id: self._delete_task(tid),
        ).pack(side="left", padx=(0, 8))

    # -----------------------------------------------------------------------
    # Calendar
    # -----------------------------------------------------------------------
    def _refresh_calendar(self):
        for w in self.cal_grid.winfo_children():
            w.destroy()

        month_name = calendar.month_name[self.cal_month]
        self.cal_month_label.configure(text=f"{month_name} {self.cal_year}")

        today_str = datetime.now().strftime("%Y-%m-%d")
        counts = self._tasks_count_by_date()

        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(self.cal_year, self.cal_month)

        for r, week in enumerate(weeks):
            self.cal_grid.grid_rowconfigure(r, weight=1)
            for c, day in enumerate(week):
                if day == 0:
                    cell = ctk.CTkFrame(self.cal_grid, fg_color="transparent")
                    cell.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
                    continue

                date_str = f"{self.cal_year}-{self.cal_month:02d}-{day:02d}"
                n = counts.get(date_str, 0)

                bg = "transparent"
                border_w = 0
                border_c = BORDER_COLOR

                if date_str == self.selected_date:
                    border_w = 2
                    border_c = ACCENT
                if date_str == today_str:
                    bg = CAL_TODAY
                elif n > 0:
                    bg = CAL_HAS_TASKS

                cell = ctk.CTkFrame(
                    self.cal_grid,
                    fg_color=bg,
                    corner_radius=8,
                    border_width=border_w,
                    border_color=border_c,
                )
                cell.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

                lbl_day = ctk.CTkLabel(
                    cell,
                    text=str(day),
                    font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                    text_color=TEXT_PRIMARY,
                    anchor="nw",
                )
                lbl_day.pack(padx=4, pady=(4, 0), anchor="nw")

                if n > 0:
                    badge = ctk.CTkLabel(
                        cell,
                        text=str(n),
                        font=ctk.CTkFont(family=FONT_FAMILY, size=10),
                        text_color="#ffffff",
                        fg_color=ACCENT,
                        corner_radius=8,
                        width=20,
                        height=20,
                    )
                    badge.pack(pady=(0, 4), anchor="center")

                # Click binding
                for widget in (cell, lbl_day):
                    widget.bind(
                        "<Button-1>",
                        lambda e, d=date_str: self._select_date(d),
                    )

    def _cal_prev(self):
        if self.cal_month == 1:
            self.cal_month = 12
            self.cal_year -= 1
        else:
            self.cal_month -= 1
        self._refresh_calendar()

    def _cal_next(self):
        if self.cal_month == 12:
            self.cal_month = 1
            self.cal_year += 1
        else:
            self.cal_month += 1
        self._refresh_calendar()

    def _select_date(self, date_str):
        self.selected_date = date_str
        self._refresh_calendar()
        self._refresh_events()

    # -----------------------------------------------------------------------
    # Events for selected date
    # -----------------------------------------------------------------------
    def _refresh_events(self):
        for w in self.events_scroll.winfo_children():
            w.destroy()

        self.events_label.configure(text=f"Events for {self.selected_date}")
        tasks = self._tasks_for_date(self.selected_date)

        if not tasks:
            ctk.CTkLabel(
                self.events_scroll,
                text="No tasks for this day.",
                text_color=TEXT_MUTED,
                font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            ).pack(pady=10)
            return

        for t in tasks:
            row = ctk.CTkFrame(self.events_scroll, fg_color=BG_CARD, corner_radius=8)
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(
                row,
                text=f"• {t.title}",
                font=ctk.CTkFont(family=FONT_FAMILY, size=12),
                text_color=TEXT_PRIMARY,
                anchor="w",
            ).pack(side="left", padx=10, pady=6, fill="x", expand=True)

            prio = ctk.CTkLabel(
                row,
                text=t.priority.upper(),
                font=ctk.CTkFont(family=FONT_FAMILY, size=10),
                text_color=TEXT_SECONDARY,
            )
            prio.pack(side="right", padx=10)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------
    def _add_deadline_task(self):
        title = self.dl_entry.get().strip()
        date = self.dl_date_entry.get().strip()
        if not title:
            return

        # Validate date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return

        task = Task(title=title, due_date=date, priority="medium")
        save_task_db(task, DB_PATH)
        self.dl_entry.delete(0, "end")
        self.refresh_all()

    def _add_no_deadline_task(self):
        title = self.ndl_entry.get().strip()
        if not title:
            return

        stars = self.ndl_priority.get()
        priority = self._stars_to_priority(stars)
        task = Task(title=title, priority=priority)
        save_task_db(task, DB_PATH)
        self.ndl_entry.delete(0, "end")
        self.refresh_all()

    def _complete_task(self, task_id):
        update_task_status_db(task_id, "completed", DB_PATH)
        self.refresh_all()

    def _delete_task(self, task_id):
        delete_task_db(task_id, DB_PATH)
        self.refresh_all()

    def _sync_google_calendar(self):
        self.sync_label.configure(text="Syncing...", text_color=WARNING_COLOR)
        self.update_idletasks()
        # Placeholder – actual Google Calendar integration requires OAuth
        self.after(1500, lambda: self.sync_label.configure(
            text="Ready", text_color=SUCCESS_COLOR
        ))

    def _show_done_tasks(self):
        win = ctk.CTkToplevel(self)
        win.title("Completed Tasks")
        win.geometry("500x400")
        win.configure(fg_color=BG_DARK)

        ctk.CTkLabel(
            win,
            text="Completed Tasks",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(pady=(16, 10))

        scroll = ctk.CTkScrollableFrame(win, fg_color=BG_PANEL, corner_radius=10)
        scroll.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        done = [t for t in self.tasks if t.status == "completed"]
        if not done:
            ctk.CTkLabel(
                scroll,
                text="No completed tasks yet.",
                text_color=TEXT_MUTED,
            ).pack(pady=20)
        else:
            for t in done:
                row = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=8)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(
                    row,
                    text=f"✓  {t.title}",
                    font=ctk.CTkFont(family=FONT_FAMILY, size=12),
                    text_color=SUCCESS_COLOR,
                    anchor="w",
                ).pack(side="left", padx=12, pady=8)
                if t.due_date:
                    ctk.CTkLabel(
                        row,
                        text=t.due_date,
                        font=ctk.CTkFont(family=FONT_FAMILY, size=11),
                        text_color=TEXT_SECONDARY,
                    ).pack(side="right", padx=12)

    def _show_stats(self):
        win = ctk.CTkToplevel(self)
        win.title("Statistics")
        win.geometry("400x300")
        win.configure(fg_color=BG_DARK)

        total = len(self.tasks)
        pending = sum(1 for t in self.tasks if t.status == "pending")
        done = sum(1 for t in self.tasks if t.status == "completed")
        overdue = sum(1 for t in self.tasks if t.is_overdue())
        today_str = datetime.now().strftime("%Y-%m-%d")
        due_today = sum(1 for t in self.tasks if t.due_date == today_str and t.status == "pending")

        ctk.CTkLabel(
            win,
            text="Statistics",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(pady=(16, 14))

        frame = ctk.CTkFrame(win, fg_color=BG_PANEL, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        stats = [
            ("Total tasks", str(total), TEXT_PRIMARY),
            ("Pending", str(pending), WARNING_COLOR),
            ("Completed", str(done), SUCCESS_COLOR),
            ("Due today", str(due_today), ACCENT),
            ("Overdue", str(overdue), DANGER_COLOR),
        ]
        for label, value, colour in stats:
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=4)
            ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                text_color=TEXT_SECONDARY,
                anchor="w",
            ).pack(side="left")
            ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
                text_color=colour,
            ).pack(side="right")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    app = StudyWizzApp()
    app.mainloop()


if __name__ == "__main__":
    main()
