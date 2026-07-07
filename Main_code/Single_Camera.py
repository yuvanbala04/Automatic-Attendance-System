import cv2
import face_recognition
import numpy as np
import os
import csv
import smtplib
import time
from datetime import datetime

# CSV file for attendance records
ATTENDANCE_CSV_FILE = "attendance.csv"

def setup_csv():
    if not os.path.exists(ATTENDANCE_CSV_FILE):
        with open(ATTENDANCE_CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Name", "In-time", "Out-time"])

setup_csv()

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
                for encoding in encodings:  # Store multiple encodings
                    known_face_encodings.append(encoding)
                    known_face_names.append(person_name)

# Store recognized faces and their times
recognized_faces = {}

# Open a single camera
video_capture = cv2.VideoCapture(0)

def process_frame():
    ret, frame = video_capture.read()
    if not ret:
        return None

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # Resize for faster processing
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else None
        name = "Unknown"

        if best_match_index is not None and face_distances[best_match_index] < 0.5:  # Stricter threshold
            name = known_face_names[best_match_index]
            now = datetime.now()
            date_str = now.strftime('%d-%m-%Y')

            if name not in recognized_faces:
                recognized_faces[name] = {'date': date_str, 'in_time': now, 'out_time': None}
                print(f"{name} entered at {now.strftime('%H:%M:%S')}")
                time.sleep(5)  # Reduced delay to improve responsiveness

            # Check again for the same face
            ret, frame = video_capture.read()
            if ret:
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces([known_face_encodings[best_match_index]], face_encoding, tolerance=0.5)
                    if matches[0]:
                        recognized_faces[name]['out_time'] = datetime.now()
                        
                        # Store attendance in CSV
                        with open(ATTENDANCE_CSV_FILE, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([recognized_faces[name]['date'], name,
                                             recognized_faces[name]['in_time'].strftime('%H:%M:%S'),
                                             recognized_faces[name]['out_time'].strftime('%H:%M:%S')])
                        print(f"Attendance recorded: {name} | Date: {recognized_faces[name]['date']} | In: {recognized_faces[name]['in_time'].strftime('%H:%M:%S')} | Out: {recognized_faces[name]['out_time'].strftime('%H:%M:%S')}")
                        
                        del recognized_faces[name]

        cv2.rectangle(frame, (left * 2, top * 2), (right * 2, bottom * 2), (0, 255, 0), 2)
        cv2.putText(frame, name, (left * 2, top * 2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return frame

while True:
    frame = process_frame()

    if frame is not None:
        cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
