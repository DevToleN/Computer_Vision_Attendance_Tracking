import sqlite3
from datetime import datetime
import os
from werkzeug.security import check_password_hash, generate_password_hash

class Database:
    def __init__(self):
        self.db_path = 'attendance.db'
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Lectures and student enrollments
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lectures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                day_of_week TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lecture_lecturers (
                lecture_id INTEGER,
                lecturer_id INTEGER,
                PRIMARY KEY (lecture_id, lecturer_id),
                FOREIGN KEY (lecture_id) REFERENCES lectures(id),
                FOREIGN KEY (lecturer_id) REFERENCES admins(id)
            )
        ''')

        # Students table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE,
                name TEXT,
                face_encoding TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                student_id TEXT,
                lecture_id INTEGER,
                PRIMARY KEY (student_id, lecture_id),
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (lecture_id) REFERENCES lectures(id)
            )
        ''')
        
        # Attendance table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                lecture_id INTEGER,
                timestamp DATETIME,
                status TEXT DEFAULT 'present',
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (lecture_id) REFERENCES lectures(id)
            )
        ''')

        attendance_columns = [row[1] for row in self.cursor.execute("PRAGMA table_info(attendance)").fetchall()]
        if 'lecture_id' not in attendance_columns:
            self.cursor.execute('ALTER TABLE attendance ADD COLUMN lecture_id INTEGER')
        
        # Admin table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT,
                name TEXT DEFAULT '',
                role TEXT DEFAULT 'admin'
                
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token_hash TEXT UNIQUE NOT NULL,
                expires_at DATETIME NOT NULL,
                used INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES admins(id)
            )
        ''')

        user_columns = [row[1] for row in self.cursor.execute("PRAGMA table_info(admins)").fetchall()]
        if 'name' not in user_columns:
            self.cursor.execute("ALTER TABLE admins ADD COLUMN name TEXT DEFAULT ''")
        if 'role' not in user_columns:
            self.cursor.execute("ALTER TABLE admins ADD COLUMN role TEXT DEFAULT 'admin'")
        
        # Create default admin if not exists
        self.cursor.execute("SELECT * FROM admins WHERE email = '1032272@cuea.edu'")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO admins (email, password) VALUES (?, ?)",
            ('1032272@cuea.edu', 'admin123'))
        self.connection.commit()
    
    def add_user(self, email, password, name, role):
        try:
            self.cursor.execute("SELECT 1 FROM admins WHERE email = ?", (email,))
            if self.cursor.fetchone():
                return False
            query = "INSERT INTO admins (email, password, name, role) VALUES (?, ?, ?, ?)"
            self.cursor.execute(query, (email, generate_password_hash(password), name, role))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False

    def add_admin(self, email, password):
        return self.add_user(email, password, '', 'admin')

    def get_user(self, user_id):
        self.cursor.execute("SELECT id, email, password, name, role FROM admins WHERE id = ?", (user_id,))
        return self.cursor.fetchone()

    def update_user(self, user_id, email, name, password=None):
        try:
            if password:
                self.cursor.execute("UPDATE admins SET email = ?, name = ?, password = ? WHERE id = ?", (email, name, generate_password_hash(password), user_id))
            else:
                self.cursor.execute("UPDATE admins SET email = ?, name = ? WHERE id = ?", (email, name, user_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False

    def set_password(self, user_id, password_hash):
        self.cursor.execute("UPDATE admins SET password = ? WHERE id = ?", (password_hash, user_id))
        self.connection.commit()

    def create_password_reset(self, user_id, token_hash, expires_at):
        self.cursor.execute("UPDATE password_reset_tokens SET used = 1 WHERE user_id = ? AND used = 0", (user_id,))
        self.cursor.execute(
            "INSERT INTO password_reset_tokens (user_id, token_hash, expires_at) VALUES (?, ?, ?)",
            (user_id, token_hash, expires_at)
        )
        self.connection.commit()

    def get_password_reset(self, token_hash):
        self.cursor.execute(
            "SELECT id, user_id, expires_at FROM password_reset_tokens WHERE token_hash = ? AND used = 0",
            (token_hash,)
        )
        return self.cursor.fetchone()

    def consume_password_reset(self, token_id, user_id, password_hash):
        self.cursor.execute("UPDATE admins SET password = ? WHERE id = ?", (password_hash, user_id))
        self.cursor.execute("UPDATE password_reset_tokens SET used = 1 WHERE id = ?", (token_id,))
        self.connection.commit()

    def get_lecturers(self):
        self.cursor.execute("SELECT id, email, name FROM admins WHERE role = 'lecturer' ORDER BY name, email")
        return self.cursor.fetchall()

    def assign_lecturer(self, lecture_id, lecturer_id):
        try:
            self.cursor.execute("INSERT INTO lecture_lecturers (lecture_id, lecturer_id) VALUES (?, ?)", (lecture_id, lecturer_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False

    def get_lecture_lecturer_ids(self, lecture_id):
        self.cursor.execute("SELECT lecturer_id FROM lecture_lecturers WHERE lecture_id = ?", (lecture_id,))
        return {row[0] for row in self.cursor.fetchall()}

    def get_lecturer_lecture_ids(self, lecturer_id):
        self.cursor.execute("SELECT lecture_id FROM lecture_lecturers WHERE lecturer_id = ?", (lecturer_id,))
        return {row[0] for row in self.cursor.fetchall()}

    def get_lectures_for_user(self, user_id, role):
        if role == 'admin':
            return self.get_lectures()
        lecture_ids = self.get_lecturer_lecture_ids(user_id)
        return [lecture for lecture in self.get_lectures() if lecture[0] in lecture_ids]

    def add_student(self, student_id, name, face_encoding):
        query = "INSERT INTO students (student_id, name, face_encoding) VALUES (?, ?, ?)"
        self.cursor.execute(query, (student_id, name, face_encoding))
        self.connection.commit()
    
    def get_all_students(self):
        self.cursor.execute("SELECT student_id, name, face_encoding FROM students")
        return self.cursor.fetchall()

    def add_lecture(self, code, name, day_of_week, start_time, end_time):
        try:
            self.cursor.execute(
                "INSERT INTO lectures (code, name, day_of_week, start_time, end_time) VALUES (?, ?, ?, ?, ?)",
                (code, name, day_of_week, start_time, end_time)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False

    def get_lectures(self):
        self.cursor.execute("SELECT id, code, name, day_of_week, start_time, end_time FROM lectures ORDER BY code")
        return self.cursor.fetchall()

    def enroll_student(self, student_id, lecture_id):
        try:
            self.cursor.execute(
                "INSERT INTO enrollments (student_id, lecture_id) VALUES (?, ?)",
                (student_id, lecture_id)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False

    def get_student_lecture_ids(self, student_id):
        self.cursor.execute("SELECT lecture_id FROM enrollments WHERE student_id = ?", (student_id,))
        return {row[0] for row in self.cursor.fetchall()}

    def mark_attendance(self, student_id, lecture_id):
        # Check if already marked today
        today = datetime.now().date()
        query = "SELECT * FROM attendance WHERE student_id = ? AND lecture_id = ? AND DATE(timestamp) = ?"
        self.cursor.execute(query, (student_id, lecture_id, today))
        
        if not self.cursor.fetchone():
            query = "INSERT INTO attendance (student_id, lecture_id, timestamp) VALUES (?, ?, ?)"
            self.cursor.execute(query, (student_id, lecture_id, datetime.now()))
            self.connection.commit()
            return True
        return False
    
    def get_attendance_report(self, date=None, lecture_id=None):
        lecture_filter = " AND e.lecture_id = ?" if lecture_id else ""
        if date:
            query = '''
                SELECT s.student_id, s.name, a.timestamp
                FROM enrollments e
                JOIN students s ON s.student_id = e.student_id
                LEFT JOIN attendance a ON s.student_id = a.student_id AND a.lecture_id = e.lecture_id AND DATE(a.timestamp) = ?
                WHERE (DATE(a.timestamp) = ? OR a.timestamp IS NULL)''' + lecture_filter
            params = [date, date]
            if lecture_id:
                params.append(lecture_id)
            self.cursor.execute(query, params)
        else:
            query = '''
                SELECT s.student_id, s.name, a.timestamp
                FROM enrollments e
                JOIN students s ON s.student_id = e.student_id
                LEFT JOIN attendance a ON s.student_id = a.student_id AND a.lecture_id = e.lecture_id
                WHERE DATE(a.timestamp) = DATE('now')''' + lecture_filter
            params = [lecture_id] if lecture_id else []
            self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_report_dates(self, lecture_id=None):
        """Return every report date grouped by lecture."""
        query = '''
            SELECT DATE(a.timestamp), l.id, l.code, l.name, COUNT(*)
            FROM attendance a
            JOIN lectures l ON l.id = a.lecture_id
        '''
        params = []
        if lecture_id:
            query += ' WHERE l.id = ?'
            params.append(lecture_id)
        query += ' GROUP BY DATE(a.timestamp), l.id ORDER BY DATE(a.timestamp) DESC, l.code'
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_all_attendance_records(self, lecture_id=None):
        """Return all attendance records for CSV export."""
        query = '''
            SELECT DATE(a.timestamp), l.code, l.name, s.student_id, s.name, a.timestamp, a.status
            FROM attendance a
            JOIN lectures l ON l.id = a.lecture_id
            LEFT JOIN students s ON s.student_id = a.student_id
        '''
        params = []
        if lecture_id:
            query += ' WHERE l.id = ?'
            params.append(lecture_id)
        query += ' ORDER BY a.timestamp DESC'
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def verify_admin(self, email, password):
        user = self.get_user_by_email(email)
        if not user:
            return None
        stored_password = user[2]
        valid = False
        if stored_password.startswith(('pbkdf2:', 'scrypt:', 'argon2:')):
            valid = check_password_hash(stored_password, password)
        elif stored_password == password:
            valid = True
            self.set_password(user[0], generate_password_hash(password))
        return user if valid else None

    def get_user_by_email(self, email):
        self.cursor.execute("SELECT id, email, password, name, role FROM admins WHERE email = ?", (email,))
        return self.cursor.fetchone()