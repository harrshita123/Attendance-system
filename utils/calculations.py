"""Attendance-related calculation and reporting helpers."""

from typing import Optional
import sqlite3


def calculate_student_attendance_stats(conn: sqlite3.Connection, student_id: int):
    """Return aggregate attendance statistics for a single student.

    The result matches the structure previously used in student_dashboard:
    - total_classes
    - present_classes
    - absent_classes
    - attendance_percentage
    """
    return conn.execute(
        """
        SELECT 
            COUNT(*) as total_classes,
            SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_classes,
            SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent_classes,
            ROUND((SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) as attendance_percentage
        FROM attendance 
        WHERE student_id = ?
        """,
        (student_id,),
    ).fetchone()


def get_monthly_attendance_report(
    conn: sqlite3.Connection,
    class_id: int,
    month: str,
):
    """Return monthly attendance report for a given class and month (YYYY-MM).

    The result matches the previous reports implementation and includes:
    - roll_number
    - name
    - total_classes
    - present_classes
    - percentage
    """
    query = """
        SELECT s.roll_number, s.name,
               COUNT(*) as total_classes,
               SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as present_classes,
               ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) as percentage
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date LIKE ?
        WHERE s.class_id = ?
        GROUP BY s.id
        ORDER BY s.roll_number
    """

    return conn.execute(query, (f"{month}%", class_id)).fetchall()
