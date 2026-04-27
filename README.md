**CS405G Club Database Application**

---

### Files:

* **ClubDB.sql**: contains SQL statements to create tables, constraints, and sample data.
* **main.py**: terminal-only Python application (automatically sets up database).
* **databaseInfo.py**: table/column information used by the Python app.
* **loginInfo.py**: your MySQL login settings.

---

### Required software:

1. MySQL Server
2. Python 3
3. mysql-connector-python

Install connector:

```
pip install mysql-connector-python
```

---

### Database setup (UPDATED):

1. SSH into your VM.
2. Upload/copy all project files onto the VM.
3. Edit `loginInfo.py` with your MySQL credentials:

```
host = "YOUR_HOST"
user = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
database = "ClubDB"
```

**No manual SQL setup required.**
The program will automatically:

* Create the database (if it does not exist)
* Select the database
* Execute all SQL commands from `ClubDB.sql`

---

### Run the application:

```
python3 main.py
```

---

### How it works:

* On startup, the program automatically initializes the database.
* If tables already exist, they will not be recreated (assuming `IF NOT EXISTS` is used).
* Sample data from `ClubDB.sql` will be inserted.

---

### How to use:

* Choose options from the numbered menus.
* View one table or all tables.
* Add rows by entering values for each column.
* Delete and modify require a WHERE condition to avoid affecting all rows.
* Reports include:

  * Club members by year
  * Advisors by year
  * Club meetings
  * Budgets and expenses
  * Student memberships
  * Student events on a specific date

---

### Example WHERE conditions:

```
Club_Name = 'Band'
Curr_Year = 2026
Student_ID = 1
```

---

### Example UPDATE SET value:

```
Annual_Budget = 3500.00
```

---

### Notes:

* Make sure `ClubDB.sql` is in the same directory as `main.py`.
* The program assumes the SQL file is safe to run multiple times.
* If errors occur during setup, they will be skipped and printed to the terminal.

---