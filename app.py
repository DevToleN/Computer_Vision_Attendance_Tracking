from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, session, send_file, send_from_directory
import cv2
import os
import pandas as pd
from io import BytesIO, StringIO
import csv
from face_detection_basic import FaceRecognitionSystem
from database_sqlite import Database
from datetime import datetime

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if db.verify_admin(email, password):
            session['admin_logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/adminregister', methods=['GET', 'POST'])
def adminregister():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            return render_template('adminregistration.html', error='Email and password are required')

        # Add admin to database
        success = db.add_admin(email, password)
    
        if success:
            return render_template('adminregistration.html', success='Admin registered successfully')
        else:
            return render_template('adminregistration.html', error='Failed to register admin (username may already exist)')

    return render_template('adminregistration.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        
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
                return render_template('register.html', success='Student registered successfully')
            else:
                return render_template('register.html', error='No face detected in photo')
    
    return render_template('register.html')

@app.route('/attendance')
def attendance():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    return render_template('attendance.html')

@app.route('/start_camera')
def start_camera():
    global camera, streaming
    if not streaming:
        camera = cv2.VideoCapture(0)
        streaming = True
    return jsonify({'status': 'started'})

@app.route('/stop_camera')
def stop_camera():
    global camera, streaming
    if streaming:
        camera.release()
        streaming = False
    return jsonify({'status': 'stopped'})

def generate_frames():
    global camera, streaming
    while streaming and camera is not None:
        success, frame = camera.read()
        if not success:
            break
        
        # Process frame for face recognition
        face_locations, face_names = face_system.recognize_faces(frame)
        frame = face_system.draw_results(frame, face_locations, face_names)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reports')
def reports():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    date = request.args.get('date', datetime.now().date())
    attendance_data = db.get_attendance_report(date)
    report_dates = db.get_report_dates()
    return render_template('reports.html', attendance_data=attendance_data, date=date, report_dates=report_dates)

@app.route('/export_excel')
def export_excel():
    date = request.args.get('date', datetime.now().date())
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
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    records = db.get_all_attendance_records()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Student ID', 'Name', 'Timestamp', 'Status'])
    writer.writerows(records)

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=attendance_reports.csv'
    return response

if __name__ == '__main__':
    app.run(debug=True)