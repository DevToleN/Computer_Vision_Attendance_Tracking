from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, session, send_file, send_from_directory
import cv2
import os
import pandas as pd
from io import BytesIO, StringIO
import csv
import hashlib
import secrets
import smtplib
from email.message import EmailMessage
from functools import wraps
from werkzeug.security import generate_password_hash
from face_detection_basic import FaceRecognitionSystem
from database_sqlite import Database
from datetime import datetime, time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'your_secret_key_here'

@app.route('/styling.css')
def styling_css():
    return send_from_directory('.', 'styling.css')

@app.route('/base.js')
def base_js():
    return send_from_directory('.', 'base.js')

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize systems
face_system = FaceRecognitionSystem()
db = Database()

# Global variables for video stream
camera = None
streaming = False
active_lecture_id = None
PASSWORD_MIN_LENGTH = 8

def password_error(password):
    if len(password) < PASSWORD_MIN_LENGTH:
        return 'Password must be at least 8 characters long.'
    if not any(character.isupper() for character in password):
        return 'Password must include an uppercase letter.'
    if not any(character.islower() for character in password):
        return 'Password must include a lowercase letter.'
    if not any(character.isdigit() for character in password):
        return 'Password must include a number.'
    return None

def send_password_reset_email(recipient, reset_url):
    host = os.getenv('MAIL_SERVER')
    port = int(os.getenv('MAIL_PORT', '587'))
    sender = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')
    if not host or not sender or not password:
        return False

    message = EmailMessage()
    message['Subject'] = 'Attendance Tracker password reset'
    message['From'] = sender
    message['To'] = recipient
    message.set_content(f'Use this link to reset your password. It expires in 30 minutes:\n\n{reset_url}\n\nIf you did not request this, ignore this email.')
    with smtplib.SMTP(host, port, timeout=10) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(message)
    return True

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view

def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):
        if session.get('user_role') != 'admin':
            return redirect(url_for('index'))
        return view(*args, **kwargs)
    return wrapped_view

def current_lectures():
    return db.get_lectures_for_user(session['user_id'], session['user_role'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = db.verify_admin(email, password)
        if user:
            session['user_id'] = user[0]
            session['user_email'] = user[1]
            session['user_name'] = user[3]
            session['user_role'] = user[4]
            session['admin_logged_in'] = user[4] == 'admin'
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    message = None
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = db.get_user_by_email(email)
        if user:
            raw_token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
            expires_at = datetime.now().timestamp() + 1800
            db.create_password_reset(user[0], token_hash, datetime.fromtimestamp(expires_at))
            reset_url = url_for('reset_password', token=raw_token, _external=True)
            try:
                send_password_reset_email(email, reset_url)
            except (OSError, smtplib.SMTPException):
                app.logger.exception('Unable to send password reset email')
        message = 'If an account exists for that email, password reset instructions have been sent.'
    return render_template('forgot_password.html', message=message, error=error)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    reset = db.get_password_reset(token_hash)
    if not reset or datetime.fromisoformat(reset[2]).timestamp() < datetime.now().timestamp():
        return render_template('reset_password.html', error='This reset link is invalid or has expired.', valid=False)

    error = None
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirmation = request.form.get('confirmation', '')
        error = password_error(password)
        if not error and password != confirmation:
            error = 'Passwords do not match.'
        if not error:
            db.consume_password_reset(reset[0], reset[1], generate_password_hash(password))
            return redirect(url_for('login', reset='success'))
    return render_template('reset_password.html', error=error, valid=True)

@app.route('/adminregister', methods=['GET', 'POST'])
@admin_required
def adminregister():
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        name = request.form.get('name', '').strip()
        role = request.form.get('role', 'lecturer')

        if not email or not password or not name or role not in {'admin', 'lecturer'}:
            return render_template('adminregistration.html', error='Name, email, password, and a valid role are required')
        password_error_message = password_error(password)
        if password_error_message:
            return render_template('adminregistration.html', error=password_error_message)

        success = db.add_user(email, password, name, role)
    
        if success:
            return render_template('adminregistration.html', success='User registered successfully')
        else:
            return render_template('adminregistration.html', error='Failed to register admin (username may already exist)')

    return render_template('adminregistration.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = db.get_user(session['user_id'])
    error = None
    success = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        name = request.form.get('name', '').strip()
        password = request.form.get('password', '').strip()
        password_confirmation = request.form.get('password_confirmation', '').strip()
        if not email or not name:
            error = 'Name and email are required.'
        elif password and password_error(password):
            error = password_error(password)
        elif password and password != password_confirmation:
            error = 'Passwords do not match.'
        elif db.update_user(session['user_id'], email, name, password or None):
            session['user_email'] = email
            session['user_name'] = name
            user = db.get_user(session['user_id'])
            success = 'Profile updated successfully.'
        else:
            error = 'That email address is already in use.'
    return render_template('profile.html', user=user, error=error, success=success)

@app.route('/register', methods=['GET', 'POST'])
@admin_required
def register():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        lecture_ids = request.form.getlist('lecture_ids')

        if not lecture_ids:
            return render_template('register.html', lectures=db.get_lectures(), error='Select at least one lecture')
        
        if 'photo' not in request.files:
            return render_template('register.html', error='No photo uploaded')
        
        file = request.files['photo']
        if file.filename == '':
            return render_template('register.html', error='No photo selected')
        
        if file:
            filename = f"{student_id}.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            if face_system.register_student(student_id, name, filepath):
                for lecture_id in lecture_ids:
                    db.enroll_student(student_id, int(lecture_id))
                return render_template('register.html', lectures=db.get_lectures(), success='Student registered successfully')
            else:
                return render_template('register.html', lectures=db.get_lectures(), error='No face detected in photo')
    
    return render_template('register.html', lectures=db.get_lectures())

@app.route('/lectures', methods=['GET', 'POST'])
@login_required
def lectures():
    if request.method == 'GET' and session.get('user_role') != 'admin':
        return render_template('lectures.html', lectures=current_lectures(), lecturers=[], read_only=True)
    if session.get('user_role') != 'admin':
        return redirect(url_for('index'))

    error = None
    success = None
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        name = request.form.get('name', '').strip()
        day_of_week = request.form.get('day_of_week', '')
        start_time = request.form.get('start_time', '')
        end_time = request.form.get('end_time', '')
        valid_schedule = False
        try:
            start = datetime.strptime(start_time, '%H:%M').time()
            end = datetime.strptime(end_time, '%H:%M').time()
            duration = datetime.combine(datetime.today(), end) - datetime.combine(datetime.today(), start)
            valid_schedule = day_of_week in {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'} and start >= time(8, 0) and end <= time(17, 0) and duration.total_seconds() == 10800
        except ValueError:
            pass

        lecturer_ids = request.form.getlist('lecturer_ids')
        if not code or not name or not valid_schedule:
            error = 'Enter all details. Lectures must run exactly 3 hours on weekdays between 8:00 AM and 5:00 PM.'
        elif db.add_lecture(code, name, day_of_week, start_time, end_time):
            lecture = next(item for item in db.get_lectures() if item[1] == code)
            for lecturer_id in lecturer_ids:
                db.assign_lecturer(lecture[0], int(lecturer_id))
            success = 'Lecture created successfully'
        else:
            error = 'A lecture with that code already exists.'

    return render_template('lectures.html', lectures=db.get_lectures(), lecturers=db.get_lecturers(), error=error, success=success)

@app.route('/attendance')
@login_required
def attendance():
    return render_template('attendance.html', lectures=current_lectures())

@app.route('/start_camera')
@login_required
def start_camera():
    global camera, streaming, active_lecture_id
    lecture_id = request.args.get('lecture_id', type=int)
    if lecture_id is None:
        return jsonify({'status': 'error', 'message': 'Select a lecture first'}), 400
    allowed_lecture_ids = {lecture[0] for lecture in current_lectures()}
    if lecture_id not in allowed_lecture_ids:
        return jsonify({'status': 'error', 'message': 'You are not assigned to this lecture'}), 403
    if not streaming:
        camera = cv2.VideoCapture(0)
        streaming = True
        active_lecture_id = lecture_id
    return jsonify({'status': 'started'})

@app.route('/stop_camera')
@login_required
def stop_camera():
    global camera, streaming, active_lecture_id
    if streaming:
        camera.release()
        streaming = False
        active_lecture_id = None
    return jsonify({'status': 'stopped'})

def generate_frames():
    global camera, streaming
    while streaming and camera is not None:
        success, frame = camera.read()
        if not success:
            break
        
        # Process frame for face recognition
        face_locations, face_names = face_system.recognize_faces(frame, active_lecture_id)
        frame = face_system.draw_results(frame, face_locations, face_names)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
@login_required
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reports')
@login_required
def reports():
    date = request.args.get('date', datetime.now().date())
    lecture_id = request.args.get('lecture_id', type=int)
    attendance_data = db.get_attendance_report(date, lecture_id)
    allowed_lecture_ids = {lecture[0] for lecture in current_lectures()}
    if lecture_id and lecture_id not in allowed_lecture_ids:
        lecture_id = None
    allowed_lecture_ids = {lecture[0] for lecture in current_lectures()}
    if session.get('user_role') != 'admin' and not allowed_lecture_ids:
        attendance_data = []
        report_dates = []
    elif lecture_id:
        attendance_data = db.get_attendance_report(date, lecture_id)
        report_dates = db.get_report_dates(lecture_id)
    elif session.get('user_role') != 'admin':
        attendance_data = []
        report_dates = []
        for assigned_lecture_id in allowed_lecture_ids:
            attendance_data.extend(db.get_attendance_report(date, assigned_lecture_id))
            report_dates.extend(db.get_report_dates(assigned_lecture_id))
    else:
        attendance_data = db.get_attendance_report(date)
        report_dates = db.get_report_dates()
    return render_template('reports.html', attendance_data=attendance_data, date=date, report_dates=report_dates, lectures=current_lectures(), selected_lecture_id=lecture_id)

@app.route('/export_excel')
def export_excel():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    date = request.args.get('date', datetime.now().date())
    lecture_id = request.args.get('lecture_id', type=int)
    if lecture_id and lecture_id not in {lecture[0] for lecture in current_lectures()}:
        return redirect(url_for('reports'))
    allowed_lecture_ids = {lecture[0] for lecture in current_lectures()}
    if lecture_id:
        attendance_data = db.get_attendance_report(date, lecture_id)
    elif session.get('user_role') != 'admin':
        attendance_data = []
        for assigned_lecture_id in allowed_lecture_ids:
            attendance_data.extend(db.get_attendance_report(date, assigned_lecture_id))
    else:
        attendance_data = db.get_attendance_report(date)
    
    df = pd.DataFrame(attendance_data, columns=['Student ID', 'Name', 'Timestamp'])
    df['Status'] = df['Timestamp'].apply(lambda x: 'Present' if x else 'Absent')
    df['Timestamp'] = df['Timestamp'].fillna('-')
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Attendance')
    output.seek(0)
    
    return send_file(output, as_attachment=True, download_name=f'attendance_{date}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/export_csv')
def export_csv():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    lecture_id = request.args.get('lecture_id', type=int)
    if lecture_id and lecture_id not in {lecture[0] for lecture in current_lectures()}:
        return redirect(url_for('reports'))
    allowed_lecture_ids = {lecture[0] for lecture in current_lectures()}
    if lecture_id:
        records = db.get_all_attendance_records(lecture_id)
    elif session.get('user_role') != 'admin':
        records = []
        for assigned_lecture_id in allowed_lecture_ids:
            records.extend(db.get_all_attendance_records(assigned_lecture_id))
    else:
        records = db.get_all_attendance_records()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Lecture Code', 'Lecture Name', 'Student ID', 'Name', 'Timestamp', 'Status'])
    writer.writerows(records)

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=attendance_reports.csv'
    return response

if __name__ == '__main__':
    app.run(debug=True)