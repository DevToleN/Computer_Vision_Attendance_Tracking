# Computer Vision Attendance Tracking System

A facial recognition-based attendance system for CUEA using Python, OpenCV, and Flask.

## Features

- Student registration with photo upload
- Real-time facial recognition attendance tracking
- Attendance reports and analytics
- Web-based interface
- MySQL database integration

## Requirements

- Python 3.8+
- MySQL Server
- Webcam/Camera
- Windows/Linux/macOS

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install MySQL Server:**
   - Download and install MySQL from https://dev.mysql.com/downloads/
   - Create a user with password (default: root/password)

3. **Setup Database:**
   ```bash
   python setup_database.py
   ```

4. **Update database credentials:**
   - Edit `database.py` and update MySQL credentials:
   ```python
   self.connection = mysql.connector.connect(
       host='localhost',
       user='your_username',
       password='your_password',
       database='attendance_system'
   )
   ```

## Usage

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Access the web interface:**
   - Open browser and go to `http://localhost:5000`

3. **Register students:**
   - Go to Register page
   - Fill student details and upload clear face photo
   - Submit form

4. **Track attendance:**
   - Go to Attendance page
   - Click "Start Camera"
   - Students look at camera for automatic recognition
   - Attendance is marked automatically

5. **View reports:**
   - Go to Reports page
   - Select date to view attendance records

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Interface │────│   Flask App      │────│   MySQL DB      │
│   (HTML/CSS/JS) │    │   (Python)       │    │   (Students/    │
└─────────────────┘    └──────────────────┘    │   Attendance)   │
                                │               └─────────────────┘
                                │
                       ┌──────────────────┐
                       │   Face Recognition│
                       │   (OpenCV +       │
                       │   face_recognition)│
                       └──────────────────┘
```

## File Structure

```
├── app.py                 # Main Flask application
├── database.py            # Database operations
├── face_recognition_system.py  # Face recognition logic
├── setup_database.py      # Database setup script
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── attendance.html
│   └── reports.html
└── static/
    └── uploads/          # Student photos
```

## Troubleshooting

1. **Camera not working:**
   - Check if camera is connected and not used by other apps
   - Try changing camera index in `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`

2. **Face not recognized:**
   - Ensure good lighting conditions
   - Student should look directly at camera
   - Re-register with better quality photo

3. **Database connection error:**
   - Verify MySQL server is running
   - Check credentials in `database.py`
   - Ensure database exists

## Technical Details

- **Face Recognition:** Uses face_recognition library (based on dlib)
- **Database:** MySQL for storing student data and attendance records
- **Web Framework:** Flask for web interface
- **Computer Vision:** OpenCV for camera operations
- **Frontend:** Bootstrap for responsive UI

## Security Considerations

- Face encodings are stored securely in database
- No raw images stored after processing
- Attendance marked only once per day per student
- Input validation on all forms

## Future Enhancements

- Multiple camera support
- Mobile app integration
- Advanced analytics dashboard
- Email notifications
- Integration with existing university systems