import mysql.connector
from mysql.connector import Error

import loginInfo as LI
from databaseInfo import DBHM

class ClubDatabaseCLI:
    def __init__(self):
        self.connection = None
        self.connect_to_database()
    
    def setup_database(self):
        connection = mysql.connector.connect(
            host=LI.host,
            user=LI.user,
            password=LI.password
        )
        cursor = connection.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {LI.database}")
        cursor.execute(f"USE {LI.database}")

        with open("ClubDB.sql", "r") as file:
            sql_script = file.read()
        
        commands = sql_script.split(";")

        for command in commands:
            command = command.strip()
            if command:
                try:
                    print("Running:", command[:50])
                    cursor.execute(command)
                except Exception as e:
                    print("Error:", e)

        connection.commit()
        cursor.close()
        connection.close()

        print(f"Your {LI.database} database is ready!")

    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(
                host=LI.host,
                user=LI.user,
                password=LI.password,
                database=LI.database
            )
            print("Connected to database successfully.\n")
        except Error as err:
            print(f"Database connection error: {err}")
            raise SystemExit(1)

    def run_query(self, sql, params=None, fetch=False):
        if not self.connection or not self.connection.is_connected():
            self.connect_to_database()

        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params or ())
            if fetch:
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return columns, rows

            self.connection.commit()
            return cursor.rowcount
        except Error as err:
            self.connection.rollback()
            print(f"SQL Error: {err}")
            return None
        finally:
            cursor.close()

    def print_rows(self, title, columns, rows):
        print("\n" + "=" * 80)
        print(title)
        print("=" * 80)

        if not rows:
            print("No rows found.\n")
            return

        widths = [len(str(col)) for col in columns]
        for row in rows:
            for i, value in enumerate(row):
                widths[i] = max(widths[i], len(str(value)))

        header = " | ".join(str(columns[i]).ljust(widths[i]) for i in range(len(columns)))
        divider = "-+-".join("-" * width for width in widths)
        print(header)
        print(divider)

        for row in rows:
            print(" | ".join(str(row[i]).ljust(widths[i]) for i in range(len(row))))
        print()

    def choose_table(self):
        tables = list(DBHM.keys())
        print("\nTables:")
        for i, table in enumerate(tables, start=1):
            print(f"{i}. {table}")

        choice = input("Choose a table number: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(tables)):
            print("Invalid table choice.")
            return None
        return tables[int(choice) - 1]

    def view_table(self):
        table = self.choose_table()
        if not table:
            return

        columns = input("Columns to view (* for all): ").strip() or "*"
        where = input("Optional WHERE condition, without the word WHERE: ").strip()

        sql = f"SELECT {columns} FROM {table}"
        if where:
            sql += f" WHERE {where}"

        result = self.run_query(sql, fetch=True)
        if result:
            cols, rows = result
            self.print_rows(table, cols, rows)

    def view_all_tables(self):
        for table in DBHM.keys():
            result = self.run_query(f"SELECT * FROM {table}", fetch=True)
            if result:
                cols, rows = result
                self.print_rows(table, cols, rows)

    def add_row(self):
        table = self.choose_table()
        if not table:
            return

        print(f"\nAdding row to {table}")
        print("Leave auto-increment IDs blank if you want MySQL to create them.")

        columns = []
        values = []
        for column in DBHM[table]:
            value = input(f"{column}: ").strip()
            if value != "":
                columns.append(column)
                values.append(value)

        if not columns:
            print("No values entered. Insert canceled.")
            return

        placeholders = ", ".join(["%s"] * len(values))
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        count = self.run_query(sql, values)
        if count is not None:
            print(f"Inserted {count} row into {table}.\n")

    def delete_row(self):
        table = self.choose_table()
        if not table:
            return

        where = input("WHERE condition, without the word WHERE: ").strip()
        if not where:
            print("Delete canceled. A WHERE condition is required.")
            return

        confirm = input(f"Delete from {table} where {where}? Type YES to confirm: ").strip()
        if confirm != "YES":
            print("Delete canceled.")
            return

        count = self.run_query(f"DELETE FROM {table} WHERE {where}")
        if count is not None:
            print(f"Deleted {count} row(s) from {table}.\n")

    def modify_row(self):
        table = self.choose_table()
        if not table:
            return

        print("Example SET value: Annual_Budget = 3500.00")
        set_text = input("SET value, without the word SET: ").strip()
        where = input("WHERE condition, without the word WHERE: ").strip()

        if not set_text or not where:
            print("Update canceled. Both SET and WHERE are required.")
            return

        count = self.run_query(f"UPDATE {table} SET {set_text} WHERE {where}")
        if count is not None:
            print(f"Updated {count} row(s) in {table}.\n")

    def report_students_in_club(self):
        club = input("Club name: ").strip()
        year = input("Year: ").strip()
        sql = """
            SELECT s.Student_ID, s.Student_Name
            FROM Student s
            JOIN Participation p ON s.Student_ID = p.Student_ID
            WHERE p.Club_Name = %s AND p.Curr_Year = %s
            ORDER BY s.Student_Name
        """
        self.show_report("Students in Club", sql, (club, year))

    def report_clubs_advisors(self):
        year = input("Year: ").strip()
        sql = """
            SELECT c.Club_Name, c.Curr_Year, f.Faculty_Name
            FROM Clubs c
            JOIN Faculty f ON c.Faculty_ID = f.Faculty_ID
            WHERE c.Curr_Year = %s
            ORDER BY c.Club_Name
        """
        self.show_report("Clubs and Advisors", sql, (year,))

    def report_meetings_for_club(self):
        club = input("Club name: ").strip()
        year = input("Year: ").strip()
        sql = """
            SELECT Meeting_Date, Meeting_Time, Meeting_Location, Meeting_Description
            FROM Meetings
            WHERE Club_Name = %s AND Curr_Year = %s
            ORDER BY Meeting_Date, Meeting_Time
        """
        self.show_report("Meetings for Club", sql, (club, year))

    def report_remaining_budget(self):
        club = input("Club name: ").strip()
        year = input("Year: ").strip()
        sql = """
            SELECT Club_Name, Curr_Year, Annual_Budget, Annual_Expenses,
                   Annual_Budget - Annual_Expenses AS Remaining_Budget
            FROM Clubs
            WHERE Club_Name = %s AND Curr_Year = %s
        """
        self.show_report("Remaining Budget", sql, (club, year))

    def report_total_budget(self):
        year = input("Year: ").strip()
        sql = """
            SELECT Curr_Year, SUM(Annual_Budget) AS Total_Budget
            FROM Clubs
            WHERE Curr_Year = %s
            GROUP BY Curr_Year
        """
        self.show_report("Total Budget", sql, (year,))

    def report_faculty_clubs(self):
        faculty_id = input("Faculty ID: ").strip()
        year = input("Year: ").strip()
        sql = """
            SELECT f.Faculty_Name, c.Club_Name, c.Curr_Year
            FROM Faculty f
            JOIN Clubs c ON f.Faculty_ID = c.Faculty_ID
            WHERE f.Faculty_ID = %s AND c.Curr_Year = %s
            ORDER BY c.Club_Name
        """
        self.show_report("Clubs Advised by Faculty", sql, (faculty_id, year))

    def report_student_clubs(self):
        student_id = input("Student ID: ").strip()
        year = input("Year: ").strip()
        sql = """
            SELECT s.Student_Name, p.Club_Name, p.Curr_Year
            FROM Student s
            JOIN Participation p ON s.Student_ID = p.Student_ID
            WHERE s.Student_ID = %s AND p.Curr_Year = %s
            ORDER BY p.Club_Name
        """
        self.show_report("Student Clubs", sql, (student_id, year))

    def report_student_events_on_date(self):
        student_id = input("Student ID: ").strip()
        date = input("Date YYYY-MM-DD: ").strip()
        sql = """
            SELECT p.Club_Name, m.Meeting_Date, m.Meeting_Time,
                   m.Meeting_Location, m.Meeting_Description
            FROM Participation p
            JOIN Meetings m
              ON p.Club_Name = m.Club_Name AND p.Curr_Year = m.Curr_Year
            WHERE p.Student_ID = %s AND m.Meeting_Date = %s
            ORDER BY m.Meeting_Time
        """
        self.show_report("Student Events on Date", sql, (student_id, date))

    def show_report(self, title, sql, params):
        result = self.run_query(sql, params, fetch=True)
        if result:
            cols, rows = result
            self.print_rows(title, cols, rows)

    def reports_menu(self):
        while True:
            print("\nReports")
            print("1. View all students in a club for a year")
            print("2. View all clubs and faculty advisors for a year")
            print("3. View all meetings/events for a club for a year")
            print("4. Report total expenses and remaining budget for a club/year")
            print("5. Report total budget of all clubs for a year")
            print("6. List all clubs advised by a faculty member")
            print("7. List all clubs a student belongs to")
            print("8. View all club meetings/events a student should attend on a date")
            print("9. Back")

            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.report_students_in_club()
            elif choice == "2":
                self.report_clubs_advisors()
            elif choice == "3":
                self.report_meetings_for_club()
            elif choice == "4":
                self.report_remaining_budget()
            elif choice == "5":
                self.report_total_budget()
            elif choice == "6":
                self.report_faculty_clubs()
            elif choice == "7":
                self.report_student_clubs()
            elif choice == "8":
                self.report_student_events_on_date()
            elif choice == "9":
                return
            else:
                print("Invalid option.")

    def main_menu(self):
        self.setup_database()

        while True:
            print("\nClub Database")
            print("1. View one table")
            print("2. View all tables")
            print("3. Add row")
            print("4. Delete row")
            print("5. Modify row")
            print("6. Reports")
            print("7. Exit")

            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.view_table()
            elif choice == "2":
                self.view_all_tables()
            elif choice == "3":
                self.add_row()
            elif choice == "4":
                self.delete_row()
            elif choice == "5":
                self.modify_row()
            elif choice == "6":
                self.reports_menu()
            elif choice == "7":
                print("Goodbye.")
                if self.connection and self.connection.is_connected():
                    self.connection.close()
                break
            else:
                print("Invalid option.")


if __name__ == "__main__":
    app = ClubDatabaseCLI()
    app.main_menu()