-- Student Attendance System Database Schema
-- SQLite Database

-- Teachers table
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Classes table
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject TEXT,
    teacher_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_number TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT,
    class_id INTEGER,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id)
);

-- Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('present', 'absent', 'late')),
    marked_by INTEGER,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (marked_by) REFERENCES teachers(id),
    UNIQUE(student_id, class_id, date)
);

-- Insert sample data with hashed passwords
INSERT OR IGNORE INTO teachers (username, password, name, email) VALUES 
('teacher1', 'scrypt:32768:8:1$salt$hash', 'Mr. John Smith', 'john.smith@school.edu'),
('teacher2', 'scrypt:32768:8:1$salt$hash', 'Ms. Sarah Johnson', 'sarah.johnson@school.edu'),
('admin', 'scrypt:32768:8:1$salt$hash', 'Administrator', 'admin@school.edu');

INSERT OR IGNORE INTO classes (name, subject, teacher_id) VALUES 
('Computer Science - A', 'Computer Science', 1),
('Computer Science - B', 'Computer Science', 1),
('Mathematics - A', 'Mathematics', 2),
('Mathematics - B', 'Mathematics', 2);

INSERT OR IGNORE INTO students (roll_number, name, email, class_id, password) VALUES 
('CS001', 'Alice Johnson', 'alice.j@school.edu', 1, 'student123'),
('CS002', 'Bob Smith', 'bob.s@school.edu', 1, 'student123'),
('CS003', 'Charlie Brown', 'charlie.b@school.edu', 1, 'student123'),
('CS004', 'Diana Prince', 'diana.p@school.edu', 2, 'student123'),
('CS005', 'Eva Green', 'eva.g@school.edu', 2, 'student123'),
('MATH001', 'Frank Miller', 'frank.m@school.edu', 3, 'student123'),
('MATH002', 'Grace Lee', 'grace.l@school.edu', 3, 'student123'),
('MATH003', 'Henry Wilson', 'henry.w@school.edu', 4, 'student123'),
('MATH004', 'Iris Taylor', 'iris.t@school.edu', 4, 'student123');
