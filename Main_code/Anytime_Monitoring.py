import cv2
import face_recognition
import numpy as np
import os
import csv
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
                if encodings:
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(person_name)

# Store recognized faces and their times
recognized_faces = {}
last_seen = {}

# Open a single camera
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    current_time = datetime.now()
    detected_names = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else None

        if best_match_index is not None and matches[best_match_index]:
            name = known_face_names[best_match_index]
            detected_names.append(name)

            if name not in recognized_faces:
                recognized_faces[name] = {'in_time': current_time, 'out_time': None}
                print(f"{name} entered at {current_time}")
            else:
                last_seen[name] = current_time
    
    for name in list(recognized_faces.keys()):
        if name not in detected_names:
            if name in last_seen and (current_time - last_seen[name]).total_seconds() > 5:
                recognized_faces[name]['out_time'] = current_time
                
                with open(ATTENDANCE_CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([recognized_faces[name]['in_time'].strftime('%d-%m-%Y'), name,
                                     recognized_faces[name]['in_time'].strftime('%H:%M:%S'),
                                     recognized_faces[name]['out_time'].strftime('%H:%M:%S')])
                
                print(f"Attendance recorded: {name} | In: {recognized_faces[name]['in_time']} | Out: {recognized_faces[name]['out_time']}")
                del recognized_faces[name]

    for (top, right, bottom, left), name in zip(face_locations, detected_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Face Recognition & Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()