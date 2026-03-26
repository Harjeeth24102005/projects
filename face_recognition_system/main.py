import cv2
import sqlite3
import os
import time
from datetime import datetime
import face_recognition
import numpy as np

class FaceRecognitionSystem:
    def __init__(self):
        self.db_name = "face_database.db"
        self.setup_database()
        self.last_captured_encoding = None

    def setup_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")

    # ---------------------------------------------------------------------
    # 🔹 Face Encoding and Recognition
    # ---------------------------------------------------------------------

    def get_face_encoding(self, image):
        """Extract 128-D face encoding using dlib via face_recognition"""
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)
        if len(encodings) > 0:
            return encodings[0]
        return None

    def find_similar_face(self, new_encoding, tolerance=0.5):
        """Find a matching face in the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name, image_path FROM faces")
        rows = cursor.fetchall()
        conn.close()

        known_encodings = []
        known_names = []

        for name, img_path in rows:
            if not os.path.exists(img_path):
                continue
            known_img = face_recognition.load_image_file(img_path)
            encs = face_recognition.face_encodings(known_img)
            if len(encs) > 0:
                known_encodings.append(encs[0])
                known_names.append(name)

        if not known_encodings:
            return None

        matches = face_recognition.compare_faces(known_encodings, new_encoding, tolerance)
        if True in matches:
            match_index = matches.index(True)
            return known_names[match_index]
        return None

    # ---------------------------------------------------------------------
    # 🔹 Database Operations
    # ---------------------------------------------------------------------

    def save_face_to_db(self, name, image):
        """Save new face data"""
        if not os.path.exists('captured_faces'):
            os.makedirs('captured_faces')

        image_path = f"captured_faces/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(image_path, image)

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO faces (name, image_path) VALUES (?, ?)", (name, image_path))
            conn.commit()
            print(f"✅ Saved new face: {name}")
            return True
        except sqlite3.IntegrityError:
            print(f"⚠️ Face with this name already exists in database")
            return False
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False
        finally:
            conn.close()

    def get_next_person_id(self):
        """Get next available person ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM faces")
        count = cursor.fetchone()[0]
        conn.close()
        return count + 1

    def get_all_faces(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, image_path FROM faces ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def rename_face(self, old_name, new_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE faces SET name = ? WHERE name = ?", (new_name, old_name))
            conn.commit()
            print(f"✅ Renamed {old_name} → {new_name}")
            return True
        except sqlite3.IntegrityError:
            print(f"❌ Name '{new_name}' already exists")
            return False
        finally:
            conn.close()

    def delete_face(self, name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT image_path FROM faces WHERE name = ?", (name,))
            result = cursor.fetchone()
            if result:
                image_path = result[0]
                if os.path.exists(image_path):
                    os.remove(image_path)
                cursor.execute("DELETE FROM faces WHERE name = ?", (name,))
                conn.commit()
                print(f"🗑️ Deleted face: {name}")
                return True
            else:
                print(f"❌ Face '{name}' not found")
                return False
        finally:
            conn.close()

    # ---------------------------------------------------------------------
    # 🔹 Management Menu
    # ---------------------------------------------------------------------

    def show_management_menu(self):
        print("\n" + "="*50)
        print("👤 FACE MANAGEMENT MENU")
        print("="*50)
        print("1. Rename a person")
        print("2. Delete a person")
        print("3. View all persons")
        print("4. Return to recognition")
        print("5. Quit")
        print("="*50)
        return input("Enter your choice (1-5): ").strip()

    def manage_faces(self):
        while True:
            choice = self.show_management_menu()
            if choice == '1':
                self.rename_person()
            elif choice == '2':
                self.delete_person()
            elif choice == '3':
                self.view_all_persons()
            elif choice == '4':
                print("🔙 Returning to recognition...")
                break
            elif choice == '5':
                print("👋 Goodbye!")
                return 'quit'
            else:
                print("❌ Invalid choice.")
        return 'continue'

    def rename_person(self):
        faces = self.get_all_faces()
        if not faces:
            print("❌ No faces in database")
            return
        for id, name, _ in faces:
            print(f"{id}. {name}")
        try:
            person_id = int(input("Enter person ID to rename: "))
            new_name = input("Enter new name: ").strip()
            target = next((name for id, name, _ in faces if id == person_id), None)
            if target:
                self.rename_face(target, new_name)
            else:
                print("❌ Invalid ID")
        except ValueError:
            print("❌ Enter a valid number")

    def delete_person(self):
        faces = self.get_all_faces()
        if not faces:
            print("❌ No faces in database")
            return
        for id, name, _ in faces:
            print(f"{id}. {name}")
        try:
            person_id = int(input("Enter person ID to delete: "))
            target = next((name for id, name, _ in faces if id == person_id), None)
            if target:
                confirm = input(f"Are you sure you want to delete {target}? (y/n): ").lower()
                if confirm == 'y':
                    self.delete_face(target)
        except ValueError:
            print("❌ Enter a valid number")

    def view_all_persons(self):
        faces = self.get_all_faces()
        if not faces:
            print("❌ No faces in database")
            return
        print("\n📊 REGISTERED PERSONS:")
        for id, name, _ in faces:
            print(f"ID: {id}, Name: {name}")
        print(f"Total: {len(faces)}")

    # ---------------------------------------------------------------------
    # 🔹 Face Capture & Recognition Loop
    # ---------------------------------------------------------------------

    def capture_new_face(self, frame, face_region):
        x, y, w, h = face_region
        face_image = frame[y:y+h, x:x+w]
        encoding = self.get_face_encoding(face_image)
        if encoding is None:
            print("❌ No clear face found, skipping capture")
            return None

        # Prevent immediate duplicate captures
        if self.last_captured_encoding is not None:
            similarity = np.linalg.norm(self.last_captured_encoding - encoding)
            if similarity < 0.45:
                print("⚠️ Same face detected, skipping capture")
                return None

        name = f"Person_{self.get_next_person_id():03d}"
        if self.save_face_to_db(name, face_image):
            self.last_captured_encoding = encoding
            return name
        return None

    def run_recognition(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Cannot open webcam")
            return

        # 🔽 Reduce webcam resolution for smoother performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("📷 Initializing webcam...")
        time.sleep(2)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        last_capture_time = 0
        capture_delay = 5
        current_name = None

        print("🚀 Face Recognition Started (press 'q' to quit, 'm' for menu)")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
            current_time = time.time()

            if len(faces) > 0:
                x, y, w, h = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[0]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                face_roi = frame[y:y+h, x:x+w]
                encoding = self.get_face_encoding(face_roi)

                if encoding is not None:
                    recognized_name = self.find_similar_face(encoding)
                    if recognized_name:
                        current_name = recognized_name
                        cv2.putText(frame, f"✅ Known: {recognized_name}", (x, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        last_capture_time = current_time
                    else:
                        if current_time - last_capture_time >= capture_delay:
                            new_name = self.capture_new_face(frame, (x, y, w, h))
                            if new_name:
                                current_name = new_name
                                cv2.putText(frame, f"🆕 New: {new_name}", (x, y - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                                last_capture_time = current_time
                        else:
                            remaining = capture_delay - (current_time - last_capture_time)
                            cv2.putText(frame, f"⏰ Capturing in {remaining:.1f}s", (x, y - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            else:
                cv2.putText(frame, "❌ No face detected", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.putText(frame, "Press 'q' to Quit | 'm' for Menu", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.imshow('Face Recognition System', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('m'):
                cv2.destroyAllWindows()
                cap.release()
                result = self.manage_faces()
                if result == 'quit':
                    return
                return self.run_recognition()

        cap.release()
        cv2.destroyAllWindows()
        print("✅ System shutdown successfully")


def main():
    system = FaceRecognitionSystem()
    system.run_recognition()


if __name__ == "__main__":
    main()
