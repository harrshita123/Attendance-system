from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from config import SECRET_KEY
from utils.db import get_db_connection, init_database
from utils.calculations import (
    calculate_student_attendance_stats,
    get_monthly_attendance_report,
)

# Authentication settings
# Common password used for all students when logging in by name
STUDENT_COMMON_PASSWORD = 'student123'

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user_type = request.form['user_type']

    conn = get_db_connection()

    if user_type == 'teacher':
        teacher = conn.execute('SELECT * FROM teachers WHERE username = ?', (username,)).fetchone()
        if teacher and check_password_hash(teacher['password'], password):
            session.clear()
            session['teacher_id'] = teacher['id']
            session['teacher_name'] = teacher['name']
            session['user_type'] = 'teacher'
            flash('Login successful!', 'success')
            conn.close()
            return redirect(url_for('teacher_dashboard'))
    elif user_type == 'student':
        # Student login: username is the student's name, password is a common value for all students
        student = conn.execute('SELECT * FROM students WHERE name = ?', (username,)).fetchone()
        if student and password == STUDENT_COMMON_PASSWORD:
            session.clear()
            session['student_id'] = student['id']
            session['student_name'] = student['name']
            session['user_type'] = 'student'
            flash('Login successful!', 'success')
            conn.close()
            return redirect(url_for('student_dashboard'))

    conn.close()
    flash('Invalid username or password', 'error')
    return redirect(url_for('index'))

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'teacher_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    
    # Get teacher's classes
    classes = conn.execute('SELECT * FROM classes WHERE teacher_id = ?', 
                          (session['teacher_id'],)).fetchall()
    
    # Get today's attendance summary
    today = date.today().strftime('%Y-%m-%d')
    attendance_summary = []
    
    for cls in classes:
        total_students = conn.execute('SELECT COUNT(*) as count FROM students WHERE class_id = ?', 
                                     (cls['id'],)).fetchone()['count']
        
        present_today = conn.execute('SELECT COUNT(*) as count FROM attendance WHERE class_id = ? AND date = ? AND status = "present"', 
                                   (cls['id'], today)).fetchone()['count']
        
        attendance_summary.append({
            'class': cls,
            'total_students': total_students,
            'present_today': present_today,
            'attendance_rate': round((present_today / total_students * 100) if total_students > 0 else 0, 1)
        })
    
    conn.close()
    
    return render_template('teacher_dashboard.html', 
                         classes=classes, 
                         attendance_summary=attendance_summary)


@app.route('/add_student', methods=['POST'])
def add_student():
    """Allow a logged-in teacher to add a new student to one of their classes."""
    if 'teacher_id' not in session:
        return redirect(url_for('index'))

    name = request.form.get('name', '').strip()
    roll_number = request.form.get('roll_number', '').strip()
    email = request.form.get('email', '').strip()
    class_id = request.form.get('class_id')

    if not name or not roll_number or not class_id:
        flash('Name, roll number, and class are required.', 'error')
        return redirect(url_for('teacher_dashboard'))

    conn = get_db_connection()

    try:
        # Ensure the selected class belongs to the logged-in teacher
        cls = conn.execute(
            'SELECT * FROM classes WHERE id = ? AND teacher_id = ?',
            (class_id, session['teacher_id']),
        ).fetchone()

        if not cls:
            flash('You are not allowed to add students to this class.', 'error')
            conn.close()
            return redirect(url_for('teacher_dashboard'))

        # Store a hashed version of the common student password (for consistency)
        hashed_password = generate_password_hash(STUDENT_COMMON_PASSWORD)
        conn.execute(
            'INSERT INTO students (roll_number, name, email, class_id, password) VALUES (?, ?, ?, ?, ?)',
            (roll_number, name, email or None, class_id, hashed_password),
        )
        conn.commit()
        flash('Student added successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error adding student: {e}', 'error')
    finally:
        conn.close()

    return redirect(url_for('teacher_dashboard'))

@app.route('/mark_attendance/<int:class_id>')
def mark_attendance(class_id):
    if 'teacher_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    
    # Get class info
    class_info = conn.execute('SELECT * FROM classes WHERE id = ?', (class_id,)).fetchone()
    
    # Get students in this class
    students = conn.execute('SELECT * FROM students WHERE class_id = ? ORDER BY roll_number', 
                          (class_id,)).fetchall()
    
    # Get selected date
    selected_date = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    
    # Get existing attendance for this date
    existing_attendance = {}
    attendance_records = conn.execute('SELECT * FROM attendance WHERE class_id = ? AND date = ?', 
                                    (class_id, selected_date)).fetchall()
    
    for record in attendance_records:
        existing_attendance[record['student_id']] = record['status']
    
    conn.close()
    
    return render_template('mark_attendance.html', 
                         class_info=class_info, 
                         students=students, 
                         selected_date=selected_date,
                         existing_attendance=existing_attendance)

@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    if 'teacher_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    class_id = request.form['class_id']
    attendance_date = request.form['date']
    marked_by = session['teacher_id']
    
    conn = get_db_connection()
    
    try:
        for student_id, status in request.form.items():
            if student_id.startswith('student_'):
                student_id = student_id.replace('student_', '')
                
                # Check if attendance already exists
                existing = conn.execute('SELECT * FROM attendance WHERE student_id = ? AND class_id = ? AND date = ?', 
                                      (student_id, class_id, attendance_date)).fetchone()
                
                if existing:
                    # Update existing record
                    conn.execute('UPDATE attendance SET status = ?, marked_by = ? WHERE id = ?', 
                               (status, marked_by, existing['id']))
                else:
                    # Insert new record
                    conn.execute('INSERT INTO attendance (student_id, class_id, date, status, marked_by) VALUES (?, ?, ?, ?, ?)', 
                               (student_id, class_id, attendance_date, status, marked_by))
        
        conn.commit()
        flash('Attendance saved successfully!', 'success')
        return jsonify({'success': True, 'message': 'Attendance saved successfully!'})
    
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
    finally:
        conn.close()

@app.route('/student_dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    
    # Get student info
    student = conn.execute(
        'SELECT s.*, c.name as class_name, c.subject as subject '
        'FROM students s LEFT JOIN classes c ON s.class_id = c.id WHERE s.id = ?',
        (session['student_id'],),
    ).fetchone()
    
    # Calculate attendance statistics using helper function
    stats = calculate_student_attendance_stats(conn, session['student_id'])
    
    # Get recent attendance
    recent_attendance = conn.execute('''
        SELECT a.*, c.name as class_name, c.subject as subject
        FROM attendance a
        JOIN classes c ON a.class_id = c.id
        WHERE a.student_id = ?
        ORDER BY a.date DESC
        LIMIT 20
    ''', (session['student_id'],)).fetchall()
    
    conn.close()
    
    return render_template(
        'student_dashboard.html',
        student=student,
        stats=stats,
        recent_attendance=recent_attendance,
    )


@app.route('/view_attendance')
def view_attendance():
    """Detailed attendance view for students with optional month filter."""
    if 'student_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()

    # Get student info (same as dashboard)
    student = conn.execute(
        'SELECT s.*, c.name as class_name, c.subject as subject '
        'FROM students s LEFT JOIN classes c ON s.class_id = c.id WHERE s.id = ?',
        (session['student_id'],),
    ).fetchone()

    month = request.args.get('month', '')

    base_query = '''
        SELECT a.*, c.name as class_name, c.subject as subject
        FROM attendance a
        JOIN classes c ON a.class_id = c.id
        WHERE a.student_id = ?
    '''
    params = [session['student_id']]

    if month:
        base_query += ' AND a.date LIKE ?'
        params.append(f'{month}%')

    base_query += ' ORDER BY a.date DESC'

    attendance_records = conn.execute(base_query, params).fetchall()

    conn.close()

    return render_template(
        'view_attendance.html',
        student=student,
        attendance_records=attendance_records,
        selected_month=month,
    )

@app.route('/reports')
def reports():
    if 'teacher_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    
    # Get teacher's classes
    classes = conn.execute(
        'SELECT * FROM classes WHERE teacher_id = ?',
        (session['teacher_id'],),
    ).fetchall()
    
    # Get monthly report data
    month = request.args.get('month', date.today().strftime('%Y-%m'))
    class_id = request.args.get('class_id', '')
    
    if class_id:
        monthly_report = get_monthly_attendance_report(conn, class_id, month)
    else:
        monthly_report = []
    
    conn.close()
    
    return render_template(
        'reports.html',
        classes=classes,
        monthly_report=monthly_report,
        selected_month=month,
        selected_class=class_id,
    )

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
