import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = sqlite3.connect(
            host='localhost',
            user='root',
            password='password',  # Change this
            database='attendance_system'
        )
        self.cursor = self.connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Students table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(20) UNIQUE,
                name VARCHAR(100),
                email VARCHAR(100),
                face_encoding TEXT
            )
        ''')
        
        # Attendance table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(20),
                timestamp DATETIME,
                status VARCHAR(20) DEFAULT 'present',
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        ''')
        

        self.connection.commit()
    
    def add_student(self, student_id, name, email, face_encoding):
        query = "INSERT INTO students (student_id, name, email, face_encoding) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (student_id, name, email, face_encoding))
        self.connection.commit()
    
    def get_all_students(self):
        self.cursor.execute("SELECT student_id, name, face_encoding FROM students")
        return self.cursor.fetchall()
    
    def mark_attendance(self, student_id):
        # Check if already marked today
        today = datetime.now().date()
        query = "SELECT * FROM attendance WHERE student_id = %s AND DATE(timestamp) = %s"
        self.cursor.execute(query, (student_id, today))
        
        if not self.cursor.fetchone():
            query = "INSERT INTO attendance (student_id, timestamp) VALUES (%s, %s)"
            self.cursor.execute(query, (student_id, datetime.now()))
            self.connection.commit()
            return True
        return False
    
    def get_attendance_report(self, date=None):
        if date:
            query = '''
                SELECT s.student_id, s.name, a.timestamp 
                FROM students s 
                LEFT JOIN attendance a ON s.student_id = a.student_id 
                WHERE DATE(a.timestamp) = %s
            '''
            self.cursor.execute(query, (date,))
        else:
            query = '''
                SELECT s.student_id, s.name, a.timestamp 
                FROM students s 
                LEFT JOIN attendance a ON s.student_id = a.student_id 
                WHERE DATE(a.timestamp) = CURDATE()
            '''
            self.cursor.execute(query)
        return self.cursor.fetchall()