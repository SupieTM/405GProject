DBHM = {
    "Faculty": ["Faculty_ID", "Faculty_Name"],
    "Student": ["Student_ID", "Student_Name"],
    "Clubs": ["Club_Name", "Curr_Year", "Faculty_ID", "Annual_Expenses", "Annual_Budget"],
    "Meetings": ["Meeting_ID", "Club_Name", "Curr_Year", "Meeting_Date", "Meeting_Time", "Meeting_Location", "Meeting_Description"],
    "Participation": ["Student_ID", "Club_Name", "Curr_Year"]
}

TABLE_NAMES = set(DBHM.keys())