import cv2
import numpy as np
import os
import pickle
from database_sqlite import Database

class FaceRecognitionSystem:
    def __init__(self):
        self.db = Database()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.known_faces = {}
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load known faces from database"""
        students = self.db.get_all_students()
        faces = []
        labels = []
        
        for i, (student_id, name, encoding_str) in enumerate(students):
            if encoding_str and os.path.exists(f"static/uploads/{student_id}.jpg"):
                self.known_faces[i] = {"id": student_id, "name": name}
                
                # Load and process image
                img = cv2.imread(f"static/uploads/{student_id}.jpg")
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces_detected = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                if len(faces_detected) > 0:
                    x, y, w, h = faces_detected[0]
                    face_roi = gray[y:y+h, x:x+w]
                    face_roi = cv2.resize(face_roi, (100, 100))
                    faces.append(face_roi)
                    labels.append(i)
        
        if faces:
            self.recognizer.train(faces, np.array(labels))
    
    def register_student(self, student_id, name, email, image_path):
        """Register a new student with their face"""
        img = cv2.imread(image_path)
        if img is None:
            return False
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            self.db.add_student(student_id, name, email, "encoded")
            self.load_known_faces()  # Reload faces
            return True
        return False
    
    def recognize_faces(self, frame):
        """Recognize faces in a frame and return results"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        face_locations = []
        face_names = []
        
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (100, 100))
            
            if self.known_faces:
                label, confidence = self.recognizer.predict(face_roi)
                
                if confidence < 100 and label in self.known_faces:
                    student_info = self.known_faces[label]
                    name = f"{student_info['name']} ({student_info['id']})"
                    
                    # Mark attendance
                    if self.db.mark_attendance(student_info['id']):
                        print(f"Attendance marked for {name}")
                else:
                    name = "Unknown"
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