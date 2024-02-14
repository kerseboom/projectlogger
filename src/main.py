import datetime
import pickle
from person import Person
from project import Project

def save_data(person, filename):
    with open(filename, 'wb') as file:
        pickle.dump(person, file)

def load_data(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None

# Example usage:

# Check if data file exists
data_filename = 'data/project_data.pkl'
loaded_person = load_data(data_filename)

# If data exists, use loaded data, otherwise create a new person
if loaded_person:
    person = loaded_person
else:
    # Create a new person
    person = Person("Your Name")

    # Create a project
    project1 = Project(1, "Project 1", 40)

    # Add project to the person
    person.add_project(project1)

# Log hours for a project with date
current_date = datetime.date.today()
person.log_hours(1, current_date, 5)

# Get weekly overview
start_date = current_date - datetime.timedelta(days=current_date.weekday())
end_date = start_date + datetime.timedelta(days=6)
weekly_overview = person.get_weekly_overview(start_date, end_date)

# Print weekly overview
print("Weekly Overview:")
for project_number, weekly_hours in weekly_overview.items():
    print(f"Project {project_number}: {weekly_hours} hours")

# Accessing detailed hours log for a project
project_log = person.projects[1].hours_log
print(f"\nDetailed Hours Log for Project 1:")
for date, hours in project_log.items():
    print(f"{date}: {hours} hours")

# Save the data for future use
save_data(person, data_filename)
