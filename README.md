# Automatic Attendance System Using Face Recognition

## Project Overview

The **Automatic Attendance System Using Face Recognition** is a Python-based project designed to automate student attendance marking using face recognition technology. Instead of manual attendance entry, the system captures student faces through a camera, compares them with stored student images, and marks attendance automatically.

This project helps reduce manual work, saves time, and improves accuracy in attendance management.

## Features

* Captures student face using camera
* Detects and recognizes faces automatically
* Compares captured face with stored student image database
* Marks attendance for recognized students
* Stores attendance details in a file
* Identifies unknown faces if the face is not matched
* Reduces manual attendance work

## Technologies Used

* Python
* OpenCV
* Face Recognition / Image Processing
* NumPy
* CSV / Excel file handling

## Project Workflow

1. Student images are stored in the database.
2. The camera captures the student’s face.
3. The captured image is converted into a suitable format for processing.
4. Face detection and recognition are performed.
5. The detected face is compared with stored student images.
6. If the face matches the database, attendance is marked as present.
7. If the face does not match, it is treated as an unknown person.

## Applications

* Schools
* Colleges
* Training centers
* Offices
* Exam halls
* Attendance monitoring systems

## Advantages

* Saves time compared to manual attendance
* Reduces human error
* Provides automatic attendance records
* Improves classroom monitoring
* Easy to use and implement


## Requirements

```text
opencv-python
numpy
face-recognition
pandas
```

## How to Run

Run the main Python file:

```bash
python Intime_only.py
```

After running the program, the camera will open and start detecting faces. If the detected face matches the stored image database, attendance will be marked automatically.

## Output

The attendance record is stored in a CSV file with details such as:

```text
Name, Date, Time, Status
Yuvan Bala, 07-07-2026, 10:30 AM, Present
```

## My Role

* Developed the face detection and recognition logic using Python and OpenCV
* Created the student image database for face matching
* Implemented automatic attendance marking
* Tested the system with different face images
* Improved recognition accuracy by handling unknown face cases

## Learning Outcome

Through this project, I gained practical knowledge in:

* Image processing
* Face detection
* Face recognition
* Python programming
* OpenCV library
* Real-time camera-based applications
* Automated attendance management systems

## Future Improvements

* Add a graphical user interface
* Store attendance data in a database
* Add admin login system
* Generate monthly attendance reports
* Improve accuracy under low-light conditions
* Add cloud-based attendance storage

## Conclusion

This project demonstrates how face recognition can be used to automate attendance marking. It provides a simple and efficient solution for educational institutions and organizations to manage attendance records with less manual effort.
