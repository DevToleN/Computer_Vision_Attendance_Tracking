import cv2
import face_recognition
import numpy as np
import pickle
from database import Database

class FaceRecognitionSystem:
    def __init__(self):
        self.db = Database()
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load known faces from database"""
        students = self.db.get_all_students()
        self.known_face_encodings = []
        self.known_face_names = []
        
        for student_id, name, encoding_str in students:
            if encoding_str:
                encoding = pickle.loads(encoding_str.encode('latin-1'))
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(f"{name} ({student_id})")
    
    def register_student(self, student_id, name, email, image_path):
        """Register a new student with their face"""
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if face_encodings:
            face_encoding = face_encodings[0]
            encoding_str = pickle.dumps(face_encoding).decode('latin-1')
            self.db.add_student(student_id, name, email, encoding_str)
            self.load_known_faces()  # Reload faces
            return True
        return False
    
    def recognize_faces(self, frame):
        """Recognize faces in a frame and return results"""
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index] and face_distances[best_match_index] < 0.6:
                name = self.known_face_names[best_match_index]
                # Extract student ID and mark attendance
                student_id = name.split('(')[1].split(')')[0]
                if self.db.mark_attendance(student_id):
                    print(f"Attendance marked for {name}")
            
            face_names.append(name)
        
        # Scale back up face locations
        face_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations]
        
        return face_locations, face_names
    
    def draw_results(self, frame, face_locations, face_names):
        """Draw rectangles and names on the frame"""
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw rectangle
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw label
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
        
        return frame