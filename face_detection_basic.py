import cv2
import os
from database_sqlite import Database

class FaceRecognitionSystem:
    def __init__(self):
        self.db = Database()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.registered_students = {}
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load registered students"""
        students = self.db.get_all_students()
        for student_id, name, _ in students:
            self.registered_students[student_id] = name
    
    def register_student(self, student_id, name, image_path):
        """Register a new student"""
        img = cv2.imread(image_path)
        if img is None:
            return False
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            self.db.add_student(student_id, name, "registered")
            self.load_known_faces()
            return True
        return False
    
    def recognize_faces(self, frame, lecture_id=None):
        """Detect faces and simulate recognition"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        face_locations = []
        face_names = []
        
        for (x, y, w, h) in faces:
            # For demo: randomly assign to registered students
            if self.registered_students:
                import random
                student_id = random.choice(list(self.registered_students.keys()))
                name = f"{self.registered_students[student_id]} ({student_id})"
                
                # Mark attendance (but only once per session to avoid spam)
                if lecture_id is not None and lecture_id in self.db.get_student_lecture_ids(student_id):
                    marked_key = (lecture_id, student_id)
                    if not hasattr(self, '_marked_students'):
                        self._marked_students = set()
                    if marked_key not in self._marked_students and self.db.mark_attendance(student_id, lecture_id):
                        print(f"Attendance marked for {name}")
                        self._marked_students.add(marked_key)
            else:
                name = "Unknown"
            
            face_locations.append((y, x+w, y+h, x))
            face_names.append(name)
        
        return face_locations, face_names
    
    def draw_results(self, frame, face_locations, face_names):
        """Draw rectangles and names on the frame"""
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        return frame