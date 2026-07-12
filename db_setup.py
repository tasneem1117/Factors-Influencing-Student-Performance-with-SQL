import sqlite3
import pandas as pd
import os


def init_database():
    print(" Initializing Database and processing Milestones...")

    # Milestone 1: Read CSVs & Load into SQLite Database
    try:
        df_habits = pd.read_csv('student_habits_performance.csv')
        df_habits.columns = [c.strip() for c in df_habits.columns]
    except FileNotFoundError:
        print(" Error: 'student_habits_performance.csv' not found.")
        return

    try:
        df_school = pd.read_csv('MOCK_DATA.csv')
        df_school.columns = [c.strip() for c in df_school.columns]
    except FileNotFoundError:
        print(" Error: 'MOCK_DATA.csv' not found.")
        return

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    # Save base data
    df_habits.to_sql('student_habits', conn, if_exists='replace', index=False)
    df_school.to_sql('school_info', conn, if_exists='replace', index=False)
    print("Milestone 1: Data from both CSV files loaded into SQL successfully.")

    # --- Incorporating sql_depi.sql Logic (Corrected SQLite Translation) ---

    # Milestone 2 & 3: Views and Data Cleaning
    cursor.execute("DROP VIEW IF EXISTS student_full_data;")
    cursor.execute("""
    CREATE VIEW student_full_data AS
    SELECT
      h.*,
      s.school_type,
      s.family_income
    FROM student_habits h
    JOIN school_info s ON h.student_id = s.student_id;
    """)

    # Create the cleaned table from the joined data view
    cursor.execute("DROP TABLE IF EXISTS student_cleaned;")
    cursor.execute("""
    CREATE TABLE student_cleaned AS 
    SELECT * FROM student_full_data;
    """)

    # Clean sleep hours
    cursor.execute("UPDATE student_cleaned SET sleep_hours = 7 WHERE sleep_hours < 0 OR sleep_hours > 24;")

    # Clean attendance percentage
    cursor.execute("UPDATE student_cleaned SET attendance_percentage = 100 WHERE attendance_percentage > 100;")
    cursor.execute("UPDATE student_cleaned SET attendance_percentage = 0 WHERE attendance_percentage < 0;")

    # Clean exam score
    cursor.execute("UPDATE student_cleaned SET exam_score = 100 WHERE exam_score > 100;")
    cursor.execute("UPDATE student_cleaned SET exam_score = 0 WHERE exam_score < 0;")

    # Remove rows with missing critical values
    cursor.execute("""
    DELETE FROM student_cleaned
    WHERE exam_score IS NULL 
       OR school_type IS NULL 
       OR family_income IS NULL;
    """)

    # Remove duplicates
    cursor.execute("""
    DELETE FROM student_cleaned
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM student_cleaned
        GROUP BY student_id
    );
    """)
    print(" Milestone 2 & 3: Data Cleaning & Unified Tables executed perfectly.")

    # Recreate the Analytical Views pointing to the fully cleaned table
    cursor.execute("DROP VIEW IF EXISTS view_campus_averages;")
    cursor.execute("""
    CREATE VIEW view_campus_averages AS
    SELECT 
        AVG(study_hours_per_day) AS avg_study_hours,
        AVG(social_media_hours) AS avg_social_media,
        AVG(sleep_hours) AS avg_sleep,
        AVG(attendance_percentage) AS avg_attendance,
        AVG(exam_score) AS avg_exam_score
    FROM student_cleaned;
    """)

    cursor.execute("DROP VIEW IF EXISTS view_factor_impact;")
    cursor.execute("""
    CREATE VIEW view_factor_impact AS
    SELECT 
        internet_quality,
        diet_quality,
        AVG(exam_score) AS avg_score,
        COUNT(student_id) AS student_count
    FROM student_cleaned
    GROUP BY internet_quality, diet_quality;
    """)

    # Milestone 4: Nightly performance summary configuration
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nightly_performance_summary (
        date_calculated TEXT DEFAULT CURRENT_DATE,
        total_students INTEGER,
        top_performers_count INTEGER,
        risk_students_count INTEGER
    );
    """)

    cursor.execute("DELETE FROM nightly_performance_summary;")
    cursor.execute("""
    INSERT INTO nightly_performance_summary (total_students, top_performers_count, risk_students_count)
    SELECT 
        COUNT(student_id),
        SUM(CASE WHEN exam_score >= 85 THEN 1 ELSE 0 END),
        SUM(CASE WHEN exam_score < 50 OR attendance_percentage < 75 THEN 1 ELSE 0 END)
    FROM student_cleaned;
    """)
    print(" Milestone 4: Automated nightly metrics sync calculated.")

    # Verification logging
    res_before = cursor.execute("SELECT COUNT(*) FROM student_full_data;").fetchone()[0]
    res_after = cursor.execute("SELECT COUNT(*) FROM student_cleaned;").fetchone()[0]
    print(f"Rows before cleaning: {res_before} | Rows after cleaning: {res_after}")

    conn.commit()
    conn.close()
    print(" Database setup complete! 'students.db' has been fully reconstructed.")


if __name__ == "__main__":
    init_database()
