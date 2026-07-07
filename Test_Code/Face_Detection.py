import cv2
from insightface.app import FaceAnalysis

# -----------------------------------------------
# 1. Initialize the InsightFace detector
# -----------------------------------------------
app = FaceAnalysis(
    name='buffalo_l',
    providers=['CPUExecutionProvider']  # use ['CUDAExecutionProvider'] if you have GPU
)
app.prepare(ctx_id=-1, det_size=(640, 640))  # ctx_id=-1 = CPU, ctx_id=0 = GPU

# -----------------------------------------------
# 2. Start webcam stream
# -----------------------------------------------
cap = cv2.VideoCapture(0)  # 0 = default webcam

if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

print("📷 Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Failed to grab frame.")
        break

    # Detect faces in current frame
    faces = app.get(frame)

    # Draw detections
    for face in faces:
        # Draw bounding box
        x1, y1, x2, y2 = map(int, face.bbox)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Draw 5 landmarks
        for (x, y) in face.kps:
            cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 0), -1)

    # Show result
    cv2.imwrite("frame.jpg", frame)


# -----------------------------------------------
# 3. Cleanup
# -----------------------------------------------
cap.release()

