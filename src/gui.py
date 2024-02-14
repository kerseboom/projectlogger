import tkinter as tk
from tkinter import ttk
import datetime
import pickle
from person import Person
from project import Project

class TimeTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracking App")

        # Create a new person or load existing data
        self.person = self.load_data()

        # Project tab
        self.create_project_tab()

        # Log hours tab
        self.create_log_hours_tab()

    def load_data(self):
        try:
            with open('project_data.pkl', 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return Person("Your Name")

    def save_data(self):
        with open('project_data.pkl', 'wb') as file:
            pickle.dump(self.person, file)

    def create_project_tab(self):
        project_tab = ttk.Frame(self.root)
        project_tab.grid(row=0, column=0, padx=10, pady=10)

        # Project creation form
        project_label = ttk.Label(project_tab, text="New Project:")
        project_label.grid(row=0, column=0, pady=5, sticky=tk.W)

        self.project_number_entry = ttk.Entry(project_tab, width=10)
        self.project_name_entry = ttk.Entry(project_tab, width=20)
        self.project_planned_hours_entry = ttk.Entry(project_tab, width=10)

        ttk.Label(project_tab, text="Project Number:").grid(row=1, column=0, pady=5, sticky=tk.W)
        self.project_number_entry.grid(row=1, column=1, pady=5, sticky=tk.W)
        ttk.Label(project_tab, text="Project Name:").grid(row=2, column=0, pady=5, sticky=tk.W)
        self.project_name_entry.grid(row=2, column=1, pady=5, sticky=tk.W)
        ttk.Label(project_tab, text="Planned Hours:").grid(row=3, column=0, pady=5, sticky=tk.W)
        self.project_planned_hours_entry.grid(row=3, column=1, pady=5, sticky=tk.W)

        add_project_button = ttk.Button(project_tab, text="Add Project", command=self.add_project)
        add_project_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_log_hours_tab(self):
        log_hours_tab = ttk.Frame(self.root)
        log_hours_tab.grid(row=0, column=1, padx=10, pady=10)

        # Log hours form
        log_hours_label = ttk.Label(log_hours_tab, text="Log Hours:")
        log_hours_label.grid(row=0, column=0, pady=5, sticky=tk.W)

        self.project_select = ttk.Combobox(log_hours_tab, values=list(self.person.projects.keys()))
        self.hours_entry = ttk.Entry(log_hours_tab, width=10)

        ttk.Label(log_hours_tab, text="Project Number:").grid(row=1, column=0, pady=5, sticky=tk.W)
        self.project_select.grid(row=1, column=1, pady=5, sticky=tk.W)
        ttk.Label(log_hours_tab, text="Date:").grid(row=2, column=0, pady=5, sticky=tk.W)
        ttk.Entry(log_hours_tab, state="readonly").grid(row=2, column=1, pady=5, sticky=tk.W)  # Placeholder for date
        ttk.Label(log_hours_tab, text="Hours:").grid(row=3, column=0, pady=5, sticky=tk.W)
        self.hours_entry.grid(row=3, column=1, pady=5, sticky=tk.W)

        log_hours_button = ttk.Button(log_hours_tab, text="Log Hours", command=self.log_hours)
        log_hours_button.grid(row=4, column=0, columnspan=2, pady=10)

    def add_project(self):
        project_number = int(self.project_number_entry.get())
        project_name = self.project_name_entry.get()
        planned_hours = int(self.project_planned_hours_entry.get())

        new_project = Project(project_number, project_name, planned_hours)
        self.person.add_project(new_project)
        self.save_data()

        # Update project dropdown in log hours tab
        self.project_select["values"] = list(self.person.projects.keys())

        # Clear project creation form
        self.project_number_entry.delete(0, tk.END)
        self.project_name_entry.delete(0, tk.END)
        self.project_planned_hours_entry.delete(0, tk.END)

    def log_hours(self):
        project_number = int(self.project_select.get())
        hours = int(self.hours_entry.get())
        current_date = datetime.date.today()

        self.person.log_hours(project_number, current_date, hours)
        self.save_data()

        # Clear log hours form
        self.project_select.set("")  # Reset the combobox selection
        self.hours_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackingApp(root)
    root.mainloop()
