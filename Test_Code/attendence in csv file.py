import cv2
import face_recognition
import os
import numpy as np
import pandas as pd
from datetime import datetime

# Load stored faces
face_encodings = []
face_names = []
path = "studentdetails"  # Folder containing images of known people

for filename in os.listdir(path):
    img_path = os.path.join(path, filename)
    image = face_recognition.load_image_file(img_path)
    encoding = face_recognition.face_encodings(image)
    
    if encoding:
        face_encodings.append(encoding[0])
        face_names.append(os.path.splitext(filename)[0])  # Use filename as name

# Attendance tracking dictionary
attendance_log = {}

# Function to mark attendance
def mark_attendance(name):
    """Logs attendance in CSV if not already marked for the session."""
    if name not in attendance_log:
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        # Append data to CSV
        df = pd.DataFrame([[name, date_time]], columns=["Name", "Date_Time"])
        if not os.path.exists("attendance.csv"):
            df.to_csv("attendance.csv", index=False)
        else:
            df.to_csv("attendance.csv", mode="a", header=False, index=False)

        # Mark as attended for this session
        attendance_log[name] = date_time
        print(f"✅ Attendance marked for {name} at {date_time}")

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)
    unknown_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(unknown_encodings, face_locations):
        matches = face_recognition.compare_faces(face_encodings, face_encoding)
        name = "Unknown"

        # Find the best match
        face_distances = face_recognition.face_distance(face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances) if matches else None

        if best_match_index is not None and matches[best_match_index]:
            name = face_names[best_match_index]
            mark_attendance(name)  # Store attendance

        # Draw rectangle around face
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show the video feed
    cv2.imshow("Face Recognition & Attendance", frame)

    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release camera and close window
video_capture.release()
cv2.destroyAllWindows()
