import sqlite3
import pandas as pd

def init_database():
    print("🚀 Initializing Database and processing Milestones...")
    
    # Milestone 1: Read CSV & Load into SQLite Database
    try:
        df = pd.read_csv('student_habits_performance.csv')
        # Clean column names (remove spaces or anomalies if any)
        df.columns = [c.strip() for c in df.columns]
    except FileNotFoundError:
        print("❌ Error: 'student_habits_performance.csv' not found. Please place it in the same directory.")
        return

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Save raw data to a standard SQL table
    df.to_sql('student_habits', conn, if_exists='replace', index=False)
    print("✅ Milestone 1: Data successfully loaded into SQL table 'student_habits'.")

    # Milestone 2 & 3: Create Analytical Views (reusable, optimized analytical queries)
    # View 1: Overall Campus Metrics
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS view_campus_averages AS
    SELECT 
        AVG(study_hours_per_day) AS avg_study_hours,
        AVG(social_media_hours) AS avg_social_media,
        AVG(sleep_hours) AS avg_sleep,
        AVG(attendance_percentage) AS avg_attendance,
        AVG(exam_score) AS avg_exam_score
    FROM student_habits;
    """)

    # View 2: Aggregated data for factor analysis (e.g., impact of internet quality on scores)
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS view_factor_impact AS
    SELECT 
        internet_quality,
        diet_quality,
        AVG(exam_score) AS avg_score,
        COUNT(student_id) AS student_count
    FROM student_habits
    GROUP BY internet_quality, diet_quality;
    """)
    print("✅ Milestone 2 & 3: Structured SQL Views created for quick dashboard retrieval.")

    # Milestone 4: MLOps / Automation (Simulating a batch/nightly aggregation task)
    # We create a summary table that an automated job would update nightly.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nightly_performance_summary (
        date_calculated TEXT DEFAULT CURRENT_DATE,
        total_students INTEGER,
        top_performers_count INTEGER,
        risk_students_count INTEGER
    );
    """)
    
    # Clear old data and simulate the automated nightly metric run
    cursor.execute("DELETE FROM nightly_performance_summary;")
    cursor.execute("""
    INSERT INTO nightly_performance_summary (total_students, top_performers_count, risk_students_count)
    SELECT 
        COUNT(student_id),
        SUM(CASE WHEN exam_score >= 85 THEN 1 ELSE 0 END),
        SUM(CASE WHEN exam_score < 50 OR attendance_percentage < 75 THEN 1 ELSE 0 END)
    FROM student_habits;
    """)
    print("✅ Milestone 4: Automated nightly batch table generated successfully.")

    conn.commit()
    conn.close()
    print("🏁 Database setup complete! 'students.db' is ready.")

if __name__ == "__main__":
    init_database()