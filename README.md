# Computer Vision Attendance Tracker

A Flask web application for registering students, detecting faces from a webcam, recording attendance, and exporting daily reports.

## Features

- Admin login and admin registration
- Student registration with an uploaded face photo
- Live webcam face detection and attendance marking
- One attendance record per student per day
- Date-based attendance reports
- Excel report export
- SQLite database created automatically on startup

## Requirements

- Python 3.8 or newer
- A working webcam for live attendance tracking
- Windows, macOS, or Linux

The application uses Flask, OpenCV, pandas, NumPy, Pillow, and SQLite. SQLite is included with Python, so a separate database server is not required.

### Password recovery email

Password recovery sends a one-time link that expires after 30 minutes. Configure these environment variables before using the recovery flow:

```text
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your-sender@example.com
MAIL_PASSWORD=your-smtp-password
```

The application uses STARTTLS. Keep the SMTP password outside source control.

## Installation

1. Clone or download this repository and open a terminal in the project directory.

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the application

Start the Flask server:

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

The SQLite database file, `attendance.db`, and the `static/uploads/` directory are created automatically when the application starts. `setup_database.py` is a legacy MySQL setup script and is not required by the current application.

## Default admin account

On first startup, the application creates this default administrator:

| Email | Password |
| --- | --- |
| `1032272@cuea.edu` | `admin123` |

Change or remove the default credentials before using the application in a real deployment. The current implementation stores passwords as plain text and uses a development Flask secret key, so it is intended for local or academic demonstration use.

## Typical workflow

1. Sign in with an administrator account.
2. Open **Register Student**, enter the student ID and name, and upload a clear image containing a face.
3. Open **Live Attendance** and select **Start Camera**.
4. Allow the application to access the webcam. Detected faces are labelled and attendance is recorded once per student per day.
5. Open **Reports**, choose a date, and use the Excel export option when needed.

## Project structure

```text
.
├── app.py                       # Flask routes and application entry point
├── database_sqlite.py           # SQLite connection and database operations
├── face_detection_basic.py      # OpenCV face detection and attendance logic
├── database.py                  # Older MySQL database implementation
├── setup_database.py            # Older MySQL database setup script
├── requirements.txt             # Runtime dependencies
├── base.js                      # Browser-side controls for the live feed
├── styling.css                  # Application styles
├── templates/                   # Jinja HTML templates
└── static/uploads/              # Uploaded student photos
```

## Important implementation notes

- Face registration verifies that the uploaded image contains at least one detectable face.
- The current live recognition implementation uses OpenCV's Haar cascade and randomly selects a registered student when a face is detected. It is a demonstration flow, not biometric identity verification.
- Attendance is stored in `attendance.db` in the project directory.
- Camera index `0` is used by default in `app.py`. Change it if the required webcam is exposed under another index.
- Do not commit `attendance.db`, uploaded photos, or production secrets to source control.

## Troubleshooting

### Dependencies fail to install

Upgrade packaging tools and try again inside the virtual environment:

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Some OpenCV or NumPy combinations may require a compatible Python version.

### The camera does not start

- Confirm that the browser or another application is not holding the webcam.
- Check the operating system camera permissions.
- Try another camera index by changing `cv2.VideoCapture(0)` in `app.py`.

### No face is detected

Use a well-lit, front-facing photo with a clearly visible face. The Haar cascade is sensitive to lighting, angle, and image quality.

### Database or report errors

Stop the application and verify that the project directory is writable. For a fresh local database, remove `attendance.db` and start the application again. This deletes existing local attendance and registration data.

## License

No license has been specified for this project.
