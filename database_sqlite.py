import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self):
        self.db_path = 'attendance.db'
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Students table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE,
                name TEXT,
                face_encoding TEXT
            )
        ''')
        
        # Attendance table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                timestamp DATETIME,
                status TEXT DEFAULT 'present',
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        ''')
        
        # Admin table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT
                
            )
        ''')
        
        # Create default admin if not exists
        self.cursor.execute("SELECT * FROM admins WHERE email = '1032272@cuea.edu'")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO admins (email, password) VALUES (?, ?)",
            ('1032272@cuea.edu', 'admin123'))
        self.connection.commit()
    
    def add_admin(self, email, password):
        try:
            self.cursor.execute("SELECT 1 FROM admins WHERE email = ?", (email,))
            if self.cursor.fetchone():
                return False
            query = "INSERT INTO admins (email, password) VALUES (?, ?)"
            self.cursor.execute(query, (email, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False

    def add_student(self, student_id, name, face_encoding):
        query = "INSERT INTO students (student_id, name, face_encoding) VALUES (?, ?, ?)"
        self.cursor.execute(query, (student_id, name, face_encoding))
        self.connection.commit()
    
    def get_all_students(self):
        self.cursor.execute("SELECT student_id, name, face_encoding FROM students")
        return self.cursor.fetchall()
    
    def mark_attendance(self, student_id):
        # Check if already marked today
        today = datetime.now().date()
        query = "SELECT * FROM attendance WHERE student_id = ? AND DATE(timestamp) = ?"
        self.cursor.execute(query, (student_id, today))
        
        if not self.cursor.fetchone():
            query = "INSERT INTO attendance (student_id, timestamp) VALUES (?, ?)"
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
                WHERE DATE(a.timestamp) = ? OR a.timestamp IS NULL
            '''
            self.cursor.execute(query, (date,))
        else:
            query = '''
                SELECT s.student_id, s.name, a.timestamp 
                FROM students s 
                LEFT JOIN attendance a ON s.student_id = a.student_id 
                WHERE DATE(a.timestamp) = DATE('now')
            '''
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_report_dates(self):
        """Return every date with recorded attendance and its present count."""
        query = '''
            SELECT DATE(timestamp) AS report_date, COUNT(*) AS present_count
            FROM attendance
            GROUP BY DATE(timestamp)
            ORDER BY report_date DESC
        '''
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_attendance_records(self):
        """Return all attendance records for CSV export."""
        query = '''
            SELECT DATE(a.timestamp), s.student_id, s.name, a.timestamp, a.status
            FROM attendance a
            LEFT JOIN students s ON s.student_id = a.student_id
            ORDER BY a.timestamp DESC
        '''
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def verify_admin(self, email, password):
        query = "SELECT * FROM admins WHERE email = ? AND password = ?"
        self.cursor.execute(query, (email, password))
        return self.cursor.fetchone() is not None