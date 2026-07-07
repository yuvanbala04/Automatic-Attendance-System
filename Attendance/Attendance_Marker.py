import pandas as pd
from datetime import datetime, timedelta

# Load attendance data
input_file = "attendance.csv"
output_file = "attendance_status.csv"

# Define weekly timetable with subjects
weekly_timetable = {
    "Monday": [("09:10", "10:00", "Math"), ("10:00", "10:50", "Science"), ("11:00", "11:50", "English"), ("11:50", "12:40", "History")],
    "Tuesday": [("09:10", "10:00", "Geography"), ("10:00", "10:50", "Physics"), ("11:00", "11:50", "Chemistry"), ("11:50", "12:40", "Biology")],
    "Wednesday": [("09:10", "10:00", "Computer"), ("10:00", "10:50", "Math"), ("11:00", "11:50", "Science"), ("11:50", "12:40", "English")],
    "Thursday": [("09:10", "10:00", "History"), ("10:00", "10:50", "Geography"), ("11:00", "11:50", "Physics"), ("11:50", "12:40", "Chemistry")],
    "Friday": [("09:10", "10:00", "Biology"), ("10:00", "10:50", "Computer"), ("11:00", "11:50", "Math"), ("11:50", "12:40", "Science")],
}

# Load CSV file and clean column names
df = pd.read_csv(input_file)
df.columns = df.columns.str.strip()  # Remove spaces in column names

# Rename columns if necessary (CSV might have different column names)
column_mapping = {
    "In-time": "Intime",
    "Out-time": "Outtime",
}
df.rename(columns=column_mapping, inplace=True)

# Check if required columns exist
required_columns = {"Name", "Date", "Intime", "Outtime"}
missing_columns = required_columns - set(df.columns)
if missing_columns:
    raise KeyError(f"Missing columns in CSV file: {missing_columns}")

# Convert Date to correct format
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df["Day"] = df["Date"].dt.day_name()

# Function to parse time properly
def parse_time(time_str):
    time_str = time_str.strip()
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return datetime.strptime(time_str, "%H:%M:%S").time()

# Merge multiple in-time and out-time entries for the same person on the same day
def merge_time_intervals(times):
    sorted_times = sorted(times, key=lambda x: x[0])
    merged = []
    for start, end in sorted_times:
        if merged and merged[-1][1] >= start:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged

# Parse Intime and Outtime
df["Intime"] = df["Intime"].apply(parse_time)
df["Outtime"] = df["Outtime"].apply(parse_time)

# Group by Name and Date, merge time intervals, and keep Day information
df_grouped = df.groupby(["Name", "Date"]).apply(lambda x: merge_time_intervals(list(zip(x["Intime"], x["Outtime"]))), include_groups=False).reset_index()
df_grouped = df_grouped.rename(columns={0: "MergedTimes"})

# Restore 'Day' column
df_grouped = df_grouped.merge(df[['Name', 'Date', 'Day']].drop_duplicates(), on=['Name', 'Date'], how='left')

# Function to calculate attendance per subject
def calculate_subject_attendance(merged_times, day):
    periods = weekly_timetable.get(day, [])
    subject_status = {subject: "-" for _, _, subject in periods}  # Default to "-" for all subjects
    for start, end, subject in periods:
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()
        period_duration = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).total_seconds()
        attended_duration = 0
        for intime, outtime in merged_times:
            attended_start = max(intime, start_time)
            attended_end = min(outtime, end_time)
            attended_duration += max((datetime.combine(datetime.today(), attended_end) - datetime.combine(datetime.today(), attended_start)).total_seconds(), 0)
        if attended_duration >= 0.7 * period_duration:
            subject_status[subject] = "Present"
        else:
            subject_status[subject] = "Absent"
    return subject_status

# Apply attendance check for each student
attendance_records = []
for _, row in df_grouped.iterrows():
    subject_attendance = calculate_subject_attendance(row["MergedTimes"], row["Day"])
    attendance_records.append({"Name": row["Name"], "Date": row["Date"].strftime("%d-%m-%Y"), **subject_attendance})

# Convert to DataFrame
df_final = pd.DataFrame(attendance_records)

# Save the output
df_final.to_csv(output_file, index=False)

print(f"Attendance status saved to {output_file}")