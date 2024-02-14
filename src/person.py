class Person:
    def __init__(self, name):
        self.name = name
        self.projects = {}

    def add_project(self, project):
        self.projects[project.number] = project

    def log_hours(self, project_number, date, hours):
        if project_number in self.projects:
            self.projects[project_number].log_hours(date, hours)

    def get_weekly_overview(self, start_date, end_date):
        weekly_overview = {}
        for project_number, project in self.projects.items():
            weekly_hours = project.get_weekly_hours(start_date, end_date)
            weekly_overview[project_number] = weekly_hours
        return weekly_overview
