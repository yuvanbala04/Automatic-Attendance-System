import cv2
import face_recognition
import numpy as np
import os
import csv
import sqlite3
import smtplib
from datetime import datetime

# Database setup
DB_FILE = "attendance.db"
EMAIL_CSV_FILE = "Student_Email_ID.csv"  # CSV file containing names and emails
def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

setup_database()
def load_email_addresses():
    emails = {}
    with open(EMAIL_CSV_FILE, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:
                name, email = row
                emails[name] = email
    return emails

email_dict = load_email_addresses()
EMAIL_SENDER = "ranjithp24072004@gmail.com"
EMAIL_PASSWORD = "fmdr wzyi tgms cgmk"  # Use App Password, not real password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
def send_email(name):
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Enable security
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    recipient = email_dict.get(name)
    if not recipient:
            print(f"No email found for {name}")
            return
    subject = "Attendance Logged"
    body = f"Dear {name},\n\nYour attendance has been recorded on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."

    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(EMAIL_SENDER, recipient, message)
    server.quit()

    print("Email sent successfully!")

# Directory containing images of known faces
KNOWN_FACES_DIR = "studentdetails"
known_face_encodings = []
known_face_names = []

# Load and encode multiple images for each person
for person_name in os.listdir(KNOWN_FACES_DIR):
    person_dir = os.path.join(KNOWN_FACES_DIR, person_name)
    if os.path.isdir(person_dir):
        for filename in os.listdir(person_dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(person_dir, filename)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)

                if encodings:
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(person_name)

# Store recognized faces to avoid duplicate entries
recognized_faces = set()

# Open webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else None

        if best_match_index is not None and matches[best_match_index]:
            name = known_face_names[best_match_index]

            if name not in recognized_faces:
                recognized_faces.add(name)
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S")

                # Insert attendance into the database
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
                conn.commit()
                conn.close()

                print(f"Attendance recorded: {name} at {time} on {date}")
                send_email(name)

        # Draw rectangle and label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Face Recognition & Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()