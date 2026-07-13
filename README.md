# 🎓 Factors Influencing Student Performance with SQL & Machine Learning

## Project Overview

This project analyzes factors that influence student academic performance using **SQL, Python, Data Analysis, and Machine Learning**.

The system loads student performance data into a SQLite database, performs analytical SQL queries, creates a dashboard for exploring student behaviors, and uses a Machine Learning model to predict exam scores based on student habits and characteristics.

The project combines:

- SQL data management and analysis
- Interactive dashboard visualization
- Machine Learning prediction
- Automated performance summaries

Project Milestones : 
- Milestone 1: Data Collection, Exploration & Preprocessing• Load educational datasets into a database.
* Explore key relationships.
- Milestone 2: Model / System Development & Evaluation• Build analytical queries for hypothesis testing.
- Milestone 3: Deployment (Real-Time or Batch)• Structure stored procedures for repeat analysis.
- Milestone 4: MLOps / Monitoring / Automation• Automate nightly query runs.
- Milestone 5: Final Documentation, Demo & Presentation• Document insights with SQL examples.


---

# Project Features

## 1. SQL Database Management

The project uses SQLite to store and analyze student performance data.

The database setup script:

- Loads CSV data into SQLite
- Cleans column names
- Creates analytical SQL views
- Generates automated performance summaries


Implemented SQL views:

### `view_campus_averages`

Calculates overall campus metrics:

- Average study hours
- Average social media usage
- Average sleep hours
- Average attendance
- Average exam score


### `view_factor_impact`

Analyzes how different factors influence exam performance:

- Internet quality
- Diet quality
- Average scores
- Number of students


### `nightly_performance_summary`

Simulates an automated batch process that tracks:

- Total students
- Number of high performers
- Number of students at academic risk



---

# Interactive Dashboard

The project includes a Streamlit dashboard that allows users to:

### Student Performance Dashboard

Search for students using Student ID and view:

- Exam score comparison
- Attendance performance
- Mental health rating
- Part-time job status
- Study hours comparison
- Sleep and social media habits
- Environmental factors


### Data Visualization

The dashboard provides:

- Bar charts
- Performance comparisons
- Factor analysis
- Campus average comparisons



---

# Machine Learning Model

A Linear Regression model was implemented to predict student exam scores.

## Model Input Features

The model uses student-related features:

### Numerical Features

- Age
- Study hours per day
- Social media hours
- Netflix hours
- Attendance percentage
- Sleep hours
- Exercise frequency
- Mental health rating


### Categorical Features

- Gender
- Internet quality
- Diet quality
- Parental education level
- Extracurricular participation
- Part-time job



---

# Machine Learning Workflow

The model follows these steps:

1. Load student performance data
2. Remove duplicates
3. Handle missing target values
4. Split data into training and testing sets
5. Separate numerical and categorical features
6. Handle missing values using imputation
7. Scale numerical features using StandardScaler
8. Encode categorical features using One-Hot Encoding
9. Train Linear Regression model
10. Evaluate performance using R² score



---

# Technologies & Tools Used

## Programming Language

- Python


## Data Processing

- Pandas
- NumPy


## Database

- SQLite
- SQL


## Machine Learning

- Scikit-learn
    - Linear Regression
    - Train/Test Split
    - One Hot Encoder
    - StandardScaler
    - SimpleImputer


## Dashboard & Visualization

- Streamlit
- Plotly


## Development Tools

- VS Code
- Git & GitHub



---
# Project Structure

```
Factors-Influencing-Student-Performance-with-SQL
│
├── app.py
│   └── Streamlit dashboard application
│
├── db_setup.py
│   └── Creates SQLite database and analytical views
│
├── model.py
│   └── Machine Learning model training and prediction
│
├── student_habits_performance.csv
│   └── Main dataset used for analysis and modeling
│
├── MOCK_DATA.csv
│   └── Additional sample data
│
├── students.db
│   └── SQLite database containing processed data and SQL views
│
└── README.md
    └── Project documentation
```
