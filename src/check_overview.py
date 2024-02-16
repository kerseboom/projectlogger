import sqlite3
from datetime import datetime

def check_weekly_overview():
    conn = sqlite3.connect('data/time_tracking.db')
    cursor = conn.cursor()

    # Replace this with the actual week you want to check
    selected_week = "Week 7, 02/12/2024 - 02/16/2024"

    # Extract start and end dates from the selected_week
    date_parts = selected_week.split(" - ")
    start_date_str = date_parts[0].split(", ")[1].strip()
    end_date_str = date_parts[1].strip()

    # Parse the start and end dates using datetime
    start_date = datetime.strptime(start_date_str, "%m/%d/%Y").date()
    end_date = datetime.strptime(end_date_str, "%m/%d/%Y").date()

    query = "SELECT projects.id, projects.name, " \
        "COALESCE(SUM(hours.hours), 0) as Monday, " \
        "COALESCE(SUM(hours1.hours), 0) as Tuesday, " \
        "COALESCE(SUM(hours2.hours), 0) as Wednesday, " \
        "COALESCE(SUM(hours3.hours), 0) as Thursday, " \
        "COALESCE(SUM(hours4.hours), 0) as Friday " \
        "FROM projects " \
        "LEFT JOIN (SELECT project_id, hours FROM hours WHERE date = ?) hours ON projects.id = hours.project_id " \
        "LEFT JOIN (SELECT project_id, hours FROM hours WHERE date = ?) hours1 ON projects.id = hours1.project_id " \
        "LEFT JOIN (SELECT project_id, hours FROM hours WHERE date = ?) hours2 ON projects.id = hours2.project_id " \
        "LEFT JOIN (SELECT project_id, hours FROM hours WHERE date = ?) hours3 ON projects.id = hours3.project_id " \
        "LEFT JOIN (SELECT project_id, hours FROM hours WHERE date = ?) hours4 ON projects.id = hours4.project_id " \
        "GROUP BY projects.id, projects.name"

    print("SQL Query:", query)
    cursor.execute(query, (start_date.strftime('%d/%m/%Y'),)*5)
    print(f"startdate: {start_date}\nenddate:{end_date}")


    weekly_overview = cursor.fetchall()

    conn.close()

    print("Project ID\tProject Name\tMonday\tTuesday\tWednesday\tThursday\tFriday")
    for row in weekly_overview:
        print(f"{row[0]}\t\t{row[1]}\t\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t\t{row[6]}")

if __name__ == "__main__":
    check_weekly_overview()
