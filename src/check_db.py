import sqlite3

def check_database_contents():
    conn = sqlite3.connect('data/time_tracking.db')
    cursor = conn.cursor()

    # Query to retrieve all records from the 'projects' table
    cursor.execute("SELECT * FROM projects")
    projects_data = cursor.fetchall()

    # Query to retrieve all records from the 'hours' table
    cursor.execute("SELECT * FROM hours")
    hours_data = cursor.fetchall()

    conn.close()

    print("Projects Table:")
    print("ID\tName\tPlanned Hours")
    for row in projects_data:
        print(f"{row[0]}\t{row[1]}\t{row[2]}")

    print("\nHours Table:")
    print("Project ID\tDate\t\tHours")
    for row in hours_data:
        print(f"{row[0]}\t\t{row[1]}\t{row[2]}")

if __name__ == "__main__":
    check_database_contents()
