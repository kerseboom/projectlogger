import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
import sqlite3
import openpyxl
import os
import sys

class TimeTrackingAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracking App")

        # Set the initial size of the root window
        self.root.geometry("400x300")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.logic = TimeTrackingAppLogic(self)

        # Project tab
        self.create_project_tab()

        # Log hours tab
        self.create_log_hours_tab()

        # Overview tab
        self.create_overview_tab()

    def create_project_tab(self):
        project_tab = ttk.Frame(self.notebook)
        self.notebook.add(project_tab, text="Projects")

        # Project creation form
        project_label = ttk.Label(project_tab, text="New Project:")
        project_label.pack(side="top", pady=5, anchor=tk.W)

        ttk.Label(project_tab, text="Project Number:").pack(side="top", pady=5, anchor=tk.W)
        self.project_number_entry = ttk.Entry(project_tab, width=20)
        self.project_number_entry.pack(side="top", pady=5, anchor=tk.W)

        ttk.Label(project_tab, text="Project Name:").pack(side="top", pady=5, anchor=tk.W)
        self.project_name_entry = ttk.Entry(project_tab, width=20)
        self.project_name_entry.pack(side="top", pady=5, anchor=tk.W)

        ttk.Label(project_tab, text="Planned Hours:").pack(side="top", pady=5, anchor=tk.W)
        self.planned_hours_entry = ttk.Entry(project_tab, width=10)
        self.planned_hours_entry.pack(side="top", pady=5, anchor=tk.W)

        add_project_button = ttk.Button(project_tab, text="Add Project", command=self.logic.add_project)
        add_project_button.pack(side="top", pady=10)

    def create_log_hours_tab(self):
        log_hours_tab = ttk.Frame(self.notebook)
        self.notebook.add(log_hours_tab, text="Log Hours")

        # Log hours form
        log_hours_label = ttk.Label(log_hours_tab, text="Log Hours:")
        log_hours_label.pack(side="top", pady=5, anchor=tk.W)

        ttk.Label(log_hours_tab, text="Project Name:").pack(side="top", pady=5, anchor=tk.W)
        self.project_select = ttk.Combobox(log_hours_tab, values=self.logic.get_project_names())
        self.project_select.pack(side="top", pady=5, anchor=tk.W)

        ttk.Label(log_hours_tab, text="Date:").pack(side="top", pady=5, anchor=tk.W)
        self.date_entry = DateEntry(log_hours_tab, width=12, date_pattern="dd/mm/yyyy")
        self.date_entry.pack(side="top", pady=5, anchor=tk.W)

        ttk.Label(log_hours_tab, text="Hours:").pack(side="top", pady=5, anchor=tk.W)
        self.hours_entry = ttk.Entry(log_hours_tab, width=10)
        self.hours_entry.pack(side="top", pady=5, anchor=tk.W)

        log_hours_button = ttk.Button(log_hours_tab, text="Log Hours", command=self.logic.log_hours)
        log_hours_button.pack(side="top", pady=10)

    def create_overview_tab(self):
        overview_tab = ttk.Frame(self.notebook)
        self.notebook.add(overview_tab, text="Overview")

        # Overview form
        overview_label = ttk.Label(overview_tab, text="Weekly Overview:")
        overview_label.pack(side="top", pady=5, anchor=tk.W)

        self.week_select = ttk.Combobox(overview_tab, values=self.logic.get_weeks())
        self.week_select.pack(side="top", pady=5, anchor=tk.W)

        # Set the current week as the default selection
        current_week = datetime.date.today().isocalendar()[1]
        for index, week in enumerate(self.logic.get_weeks()):
            if str(current_week) in week.split(" ")[1]:
                self.week_select.current(index)
                break

        overview_button = ttk.Button(overview_tab, text="Get Overview", command=self.logic.get_weekly_overview)
        overview_button.pack(side="top", pady=10)

class TimeTrackingAppLogic:
    def __init__(self, gui):
        self.gui = gui
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        db_path = os.path.join(script_dir, 'data', 'time_tracking.db')
        print(f"script-path: {script_dir}\ndb-path: {db_path}")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, number INTEGER, name TEXT, planned_hours INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS hours (project_number INTEGER, date TEXT, hours INTEGER)''')
        self.conn.commit()

    def add_project(self):
        project_number = self.gui.project_number_entry.get()
        project_name = self.gui.project_name_entry.get()
        planned_hours = int(self.gui.planned_hours_entry.get())

        if project_number and project_name and planned_hours:
            self.cursor.execute("INSERT INTO projects (number, name, planned_hours) VALUES (?, ?, ?)", (project_number, project_name, planned_hours))
            self.conn.commit()

            # Clear project creation form
            self.gui.project_number_entry.delete(0, tk.END)
            self.gui.project_name_entry.delete(0, tk.END)
            self.gui.planned_hours_entry.delete(0, tk.END)

            # Update project selection dropdown
            self.gui.project_select['values'] = self.get_project_names()

    def log_hours(self):
        project_name = self.gui.project_select.get()
        hours = int(self.gui.hours_entry.get())
        current_date = self.gui.date_entry.get()

        if project_name and hours and current_date:
            project_number = self.get_project_number(project_name)
            self.cursor.execute("INSERT INTO hours (project_number, date, hours) VALUES (?, ?, ?)", (project_number, current_date, hours))
            self.conn.commit()

            # Clear log hours form
            self.gui.project_select.set("")  # Reset the combobox selection
            self.gui.hours_entry.delete(0, tk.END)

    def get_project_names(self):
        self.cursor.execute("SELECT name FROM projects")
        return [row[0] for row in self.cursor.fetchall()]

    def get_project_number(self, project_name):
        self.cursor.execute("SELECT number FROM projects WHERE name = ?", (project_name,))
        return self.cursor.fetchone()[0]

    def get_weeks(self):
        weeks = []
        today = datetime.date.today()
        current_week = today.isocalendar()[1]
        current_year = today.year

        for week in range(1, current_week + 1):
            start_date = datetime.datetime.strptime(f"{current_year}-W{week}-1", "%Y-W%W-%w").date()
            end_date = start_date + datetime.timedelta(days=4)
            week_str = f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"
            weeks.append(week_str)

        weeks.reverse()

        return weeks

    def get_weekly_overview(self):
        selected_week = self.gui.week_select.get()

        start_date_str = selected_week.split(" - ")[0].strip()
        start_date = datetime.datetime.strptime(start_date_str, "%d/%m/%Y").date()

        end_date_str = selected_week.split(" - ")[1].strip()
        end_date = datetime.datetime.strptime(end_date_str, "%d/%m/%Y").date()

        # Create a new workbook and add a worksheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Write headers to the sheet
        sheet.append(["Project Number", "Project Name", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

        for project_name in self.get_project_names():
            project_number = self.get_project_number(project_name)
            project_data = [project_number, project_name]

            # Iterate through each day of the week
            date = start_date
            for _ in range(5):
                # Query hours for the specific project and date
                self.cursor.execute(
                    "SELECT COALESCE(SUM(hours), 0) FROM hours WHERE project_number = ? AND date = ?",
                    (project_number, date.strftime("%d/%m/%Y"))
                )
                hours = self.cursor.fetchone()[0]
                project_data.append(hours)

                # Move to the next day
                date += datetime.timedelta(days=1)

            # Add project data to the sheet
            sheet.append(project_data)

        # Save to Excel file
        file_path = f"log_workinghours_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.xlsx"
        workbook.save(file_path)

        # Open the saved Excel file
        os.system(f"start excel.exe {file_path}")