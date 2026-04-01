# Student Attendance System

A simple and modern Student Attendance Management System built with Flask, SQLite, and Bootstrap.

## Features

### Teacher Features
-  Login system for teachers
-  View dashboard with attendance summary
-  Mark attendance for any date
-  View monthly and subject-wise reports


### Student Features
-  Login system for students
-  View personal attendance dashboard
-  Check attendance statistics
-  View recent attendance history

### System Features
-  Clean and modern UI
-  Responsive design
-  Form validation
-  Auto-save functionality
-  SQLite database
-  Session management

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project folder**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   Navigate to `http://localhost:5000`

## Default Login Credentials

### Teacher Login
- Username: `teacher1`
- Password: `password123`

### Student Login
- Username: student's **full name** (for example: `Alice Johnson`)
- Password: common student password `student123`

## Project Structure

```
attendance-system/
├── app.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── database/
│   └── schema.sql        # Database schema and sample data
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── main.js       # JavaScript functionality
└── templates/
    ├── base.html         # Base template
    ├── login.html        # Login page
    ├── teacher_dashboard.html    # Teacher dashboard
    ├── student_dashboard.html    # Student dashboard
    ├── mark_attendance.html      # Attendance marking
    └── reports.html       # Reports page
```

## Usage

### For Teachers
1. Login with teacher credentials
2. View your classes on the dashboard
3. Click "Mark Attendance" to take attendance
4. Select date and mark students as Present/Absent/Late
5. View reports to see monthly attendance statistics

### For Students
1. Login with student credentials (roll number)
2. View your attendance dashboard
3. Check your attendance percentage
4. View recent attendance history

## Database

The system uses SQLite database with the following tables:
- `teachers` - Teacher information
- `classes` - Class/subject information
- `students` - Student records
- `attendance` - Attendance records

## Technologies Used

- **Backend:** Python Flask
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **UI Framework:** Custom CSS with modern design
- **Security:** Password hashing, session management

## Development

To modify or extend the system:

1. **Database changes:** Edit `database/schema.sql`
2. **Backend logic:** Modify `app.py`
3. **Frontend:** Update templates in `templates/` folder
4. **Styling:** Edit `static/css/style.css`
5. **JavaScript:** Update `static/js/main.js`

## Troubleshooting

### Common Issues

1. **Database not found:** The app automatically creates the database on first run
2. **Port already in use:** Change the port in `app.py` (line ending)
3. **Login issues:** Check credentials in database schema

### Reset Database
Delete `database/attendance.db` and restart the app to recreate with sample data.

## License

This project is open source and available under the MIT License.
