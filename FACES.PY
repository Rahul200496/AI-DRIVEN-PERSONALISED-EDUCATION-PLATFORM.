import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime

# Directories
KNOWN_FACES_DIR = "known_faces"
TRAINER_FILE = "face_trainer.yml"
ATTENDANCE_FILE = "attendance.csv"

# Create necessary folders
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

# Load face recognizer and cascade
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Function to capture face images
def collect_faces():
    name = input("Enter your name: ").strip()
    person_path = os.path.join(KNOWN_FACES_DIR, name)
    if not os.path.exists(person_path):
        os.makedirs(person_path)

    cap = cv2.VideoCapture(0)
    count = 0
    while count < 30:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            cv2.imwrite(f"{person_path}/{count}.jpg", face_roi)
            count += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Face Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Face data saved for {name}!")

# Function to train the model
def train_faces():
    faces = []
    labels = []
    label_map = {}

    for label, person_name in enumerate(os.listdir(KNOWN_FACES_DIR)):
        person_path = os.path.join(KNOWN_FACES_DIR, person_name)
        label_map[label] = person_name

        for image in os.listdir(person_path):
            image_path = os.path.join(person_path, image)
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            faces.append(img)
            labels.append(label)

    if len(faces) > 0:
        face_recognizer.train(faces, np.array(labels))
        face_recognizer.save(TRAINER_FILE)
        np.save("label_map.npy", label_map)
        print("✅ Training complete!")
    else:
        print("⚠️ No faces found. Please collect face data first.")

# Function to mark attendance
def mark_attendance(name):
    df = pd.read_csv(ATTENDANCE_FILE) if os.path.exists(ATTENDANCE_FILE) else pd.DataFrame(columns=["Name", "Time"])
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if name not in df["Name"].values:
        new_entry = pd.DataFrame([[name, now]], columns=["Name", "Time"])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(ATTENDANCE_FILE, index=False)
        print(f"✅ Attendance marked for {name}")

# Function to recognize faces
def recognize_faces():
    if not os.path.exists(TRAINER_FILE):
        print("⚠️ No trained model found. Train the model first!")
        return

    face_recognizer.read(TRAINER_FILE)
    label_map = np.load("label_map.npy", allow_pickle=True).item()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            label, confidence = face_recognizer.predict(face_roi)
            name = label_map.get(label, "Unknown")

            if confidence < 50:
                mark_attendance(name)
                color = (0, 255, 0)
            else:
                name = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Face Recognition Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main menu
while True:
    print("\n📌 Face Recognition Attendance System")
    print("1. Collect Face Data")
    print("2. Train Face Model")
    print("3. Start Face Recognition")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        collect_faces()
    elif choice == "2":
        train_faces()
    elif choice == "3":
        recognize_faces()
    elif choice == "4":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Try again.")
