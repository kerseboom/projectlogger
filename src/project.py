class Project:
    def __init__(self, number, name, planned_hours):
        self.number = number
        self.name = name
        self.planned_hours = planned_hours
        self.hours_log = {}

    def log_hours(self, date, hours):
        if date not in self.hours_log:
            self.hours_log[date] = 0
        self.hours_log[date] += hours

    def get_total_hours(self):
        return sum(self.hours_log.values())

    def get_weekly_hours(self, start_date, end_date):
        weekly_hours = 0
        for date, hours in self.hours_log.items():
            if start_date <= date <= end_date:
                weekly_hours += hours
        return weekly_hours