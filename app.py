import streamlit as st
import numpy as np
import sqlite3
import pandas as pd
import plotly.express as px
from model import train_model

RECOMMENDATIONS = [
    {
        "condition": lambda s: s["study_hours_per_day"] < 3,
        "message": "Increase study hours to at least 3-4 hours per day."
    },
    {
        "condition": lambda s: s["attendance_percentage"] < 75,
        "message": "Improve attendance. Students with attendance below 75% usually perform worse."
    },
    {
        "condition": lambda s: s["sleep_hours"] < 6,
        "message": "Try sleeping 7-8 hours every night."
    },
    {
        "condition": lambda s: s["social_media_hours"] > 4,
        "message": "Reduce social media usage."
    },
    {
        "condition": lambda s: s["exercise_frequency"] < 2,
        "message": "Exercise more frequently."
    },
    {
        "condition": lambda s: s["mental_health_rating"] < 5,
        "message": "Consider improving mental well-being."
    }
]

# Helper function to query the local SQL database
def query_db(query, params=()):
    with sqlite3.connect('students.db') as conn:
        return pd.read_sql_query(query, conn, params=params)

# Page Layout Configuration
st.set_page_config(page_title="Student Performance Dashboard", layout="wide", initial_sidebar_state="expanded")

# Initialize and cache model to prevent re-training on every widget interaction
@st.cache_resource
def load_trained_model():
    return train_model()

model = load_trained_model()

# --- Custom Styling ---
st.markdown("""
    <style>
    .metric-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #4A90E2; }
    </style>
""", unsafe_allow_html=True)

# Title Header
st.title("Student Performance & Influencing Factors Dashboard")
st.markdown("Analyze an individual student's performance metrics and compare them against campus averages using backend SQL execution.")

# --- Milestone 4 Display: System Health / Batch Run Info ---
try:
    automation_df = query_db("SELECT * FROM nightly_performance_summary")
    if not automation_df.empty:
        last_run = automation_df.iloc[0]
        st.sidebar.caption(f"**SQL Nightly Automation Sync:** {last_run['date_calculated']}")
        st.sidebar.caption(f"Total Cohort Size: {last_run['total_students']} students")
except Exception:
    pass

# --- Sidebar Search ---
st.sidebar.header("Student Registry Lookup")
student_id_input = st.sidebar.text_input("Enter Student ID:", placeholder="e.g., S1001, S1002").strip()

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "AI Prediction"]
)

if page == "Dashboard":

    if student_id_input:
        student_query = """
        SELECT *
        FROM student_cleaned
        WHERE student_id = ?
        """

        student_data = query_db(
            student_query,
            (student_id_input,)
        )

        if not student_data.empty:
            student = student_data.iloc[0]

            campus_averages = query_db(
                "SELECT * FROM view_campus_averages"
            ).iloc[0]

            st.header(
                f"📊 Report Card for Student: {student_id_input}"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                score_diff = float(
                    student["exam_score"]
                    -
                    campus_averages["avg_exam_score"]
                )

                st.metric(
                    label=" Exam Score",
                    value=f"{student['exam_score']}%",
                    delta=f"{score_diff:.1f}% vs Average"
                )

            with col2:
                att_diff = float(
                    student["attendance_percentage"]
                    -
                    campus_averages["avg_attendance"]
                )

                st.metric(
                    label=" Attendance Rate",
                    value=f"{student['attendance_percentage']}%",
                    delta=f"{att_diff:.1f}% vs Average"
                )

            with col3:
                st.metric(
                    label=" Mental Health Level",
                    value=f"{student['mental_health_rating']}/10",
                    help="1 = Poor, 10 = Excellent"
                )

            with col4:
                st.metric(
                    label=" Part-Time Job",
                    value=f"{student['part_time_job']}"
                )

            st.markdown("---")

            left_chart_col, right_chart_col = st.columns(2)

            with left_chart_col:
                st.subheader(
                    " Time Allocation Comparison (Hours/Day)"
                )

                time_comparison = pd.DataFrame({
                    "Activity": [
                        "Study Hours",
                        "Social Media",
                        "Sleep Hours"
                    ],
                    "This Student": [
                        student["study_hours_per_day"],
                        student["social_media_hours"],
                        student["sleep_hours"]
                    ],
                    "Campus Average": [
                        campus_averages["avg_study_hours"],
                        campus_averages["avg_social_media"],
                        campus_averages["avg_sleep"]
                    ]
                }).melt(
                    id_vars="Activity",
                    var_name="Group",
                    value_name="Hours"
                )

                fig_time = px.bar(
                    time_comparison,
                    x="Activity",
                    y="Hours",
                    color="Group",
                    barmode="group",
                    color_discrete_sequence=[
                        "#1f77b4",
                        "#aec7e8"
                    ],
                    template="plotly_white"
                )

                st.plotly_chart(
                    fig_time,
                    use_container_width=True
                )

            with right_chart_col:
                st.subheader(
                    " Household & Environment Context"
                )

                env_data = pd.DataFrame({
                    "Environmental Factor": [
                        "Internet Quality",
                        "School Type",
                        "Family Income Level",
                        "Diet Quality",
                        "Parental Education",
                        "Extracurriculars"
                    ],
                    "Status / Level": [
                        student["internet_quality"],
                        student["school_type"],
                        student["family_income"],
                        student["diet_quality"],
                        student["parental_education_level"],
                        student["extracurricular_participation"]
                    ]
                })

                st.table(env_data)

            st.subheader(
                "💡 System Diagnosis & Observations"
            )

            insights = []

            if (
                student["study_hours_per_day"]
                <
                campus_averages["avg_study_hours"]
            ):
                insights.append(
                    f"• This student studies **{campus_averages['avg_study_hours'] - student['study_hours_per_day']:.1f} fewer hours** than average. Increasing structured study sessions might yield higher scores."
                )

            if student["attendance_percentage"] < 75:
                insights.append(
                    "• Critical Alert: Attendance is below 75%. Absenteeism might be heavily dampening comprehension."
                )

            if student["sleep_hours"] < 6:
                insights.append(
                    "• Rest deficit flagged! Sleeping under 6 hours regularly correlates with lower mental health ratings across this cohort."
                )

            if insights:
                for insight in insights:
                    st.markdown(insight)
            else:
                st.success(
                    "• Academic habits look highly optimal. Student is operating at or above target benchmarks across key habits."
                )

        else:
            st.error(
                f" Record '{student_id_input}' not found in database. Double-check the ID naming standard (e.g., S1001)."
            )

    else:
        st.info(
            "Welcome! Please enter a valid Student ID in the left sidebar menu to compute SQL metrics and visualize analytical charts dynamically."
        )

        st.subheader(
            "Overall Dataset Distribution Matrix (Global View)"
        )

        query = """
        SELECT
            CASE
                WHEN attendance_percentage >= 85 THEN 'High Attendance (85%+)'
                WHEN attendance_percentage >= 75 THEN 'Average Attendance (75-84%)'
                ELSE 'Low Attendance (<75%)'
            END AS attendance_group,
            AVG(exam_score) AS average_exam_score
        FROM student_cleaned
        GROUP BY attendance_group
        ORDER BY average_exam_score DESC
        """

        factors_df = query_db(query)

        fig_global = px.bar(
            factors_df,
            x="attendance_group",
            y="average_exam_score",
            title="Does Attendance Matter? Average Exam Scores by Attendance Group",
            labels={
                "attendance_group": "Attendance Category",
                "average_exam_score": "Average Score (%)"
            },
            color="attendance_group",
            color_discrete_sequence=[
                "#2ecc71",
                "#f1c40f",
                "#e74c3c"
            ]
        )

        st.plotly_chart(
            fig_global,
            use_container_width=True
        )


elif page == "AI Prediction":

    st.header(" WELCOME TO CORTEXIO - An AI Exam Score Prediction Model")
    st.write("Enter the student's information below and click **Predict Score**.")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 15, 30, 20)
        gender = st.selectbox("Gender", ["Male", "Female"])
        study_hours = st.slider("Study Hours Per Day", 0.0, 12.0, 4.0)
        social_media = st.slider("Social Media Hours", 0.0, 12.0, 2.0)
        netflix = st.slider("Netflix Hours", 0.0, 12.0, 1.0)
        attendance = st.slider("Attendance Percentage", 0.0, 100.0, 85.0)
        sleep = st.slider("Sleep Hours", 0.0, 12.0, 7.0)
        school_type = st.selectbox("School Type",["Public", "Private" , "International"])


    with col2:
        exercise = st.slider("Exercise Frequency", 0, 7, 3)
        mental_health = st.slider("Mental Health Rating", 1, 10, 7)
        internet = st.selectbox("Internet Quality", ["Poor", "Average", "Good"])
        diet = st.selectbox("Diet Quality", ["Poor", "Average", "Good"])
        parental = st.selectbox("Parental Education", ["High School", "Bachelor", "Master", "PhD"])
        extracurricular = st.selectbox("Extracurricular Participation", ["Yes", "No"])
        part_time = st.selectbox("Part Time Job", ["Yes", "No"])
        family_income = st.selectbox("Family Income",["Low", "Medium", "High"])

    st.divider()

    if st.button("Predict Exam Score", use_container_width=True):

        # Crucial Adjustment: Match exact column names used during model.fit() in CSV
        student = pd.DataFrame({
            "age": [age],
            "gender": [gender],
            "study_hours_per_day": [study_hours],
            "social_media_hours": [social_media],
            "netflix_hours": [netflix],
            "attendance_percentage": [attendance],
            "sleep_hours": [sleep],
            "exercise_frequency": [exercise],
            "mental_health_rating": [mental_health],
            "internet_quality": [internet],
            "diet_quality": [diet],
            "parental_education_level": [parental],
            "extracurricular_participation": [extracurricular],
            "part_time_job": [part_time],
            "school_type": [school_type],
            "family_income": [family_income]
        })

        # Run pipeline prediction seamlessly
        prediction = float(np.clip(model.predict(student)[0], 0, 100))
        st.subheader("Prediction Result")
        st.metric(
            "Predicted Exam Score",
            f"{prediction:.2f}%"
        )

        if prediction >= 85:
            st.success("Excellent! This student is predicted to perform exceptionally well.")
        elif prediction >= 70:
            st.info("Good performance expected.")
        elif prediction >= 50:
            st.warning("Average performance. There is room for improvement.")
        else:
            st.error("High academic risk. Consider improving study habits and attendance.")

        recommendations = []

        for rule in RECOMMENDATIONS:
            if rule["condition"](student.iloc[0]):
                recommendations.append(rule["message"])

        if recommendations:
            st.subheader("Recommendations")
            for rec in recommendations:
                st.write("•", rec)
        else:
            st.success("No recommendations. Excellent habits!")