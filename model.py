import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def train_model():
    df = pd.read_csv("student_habits_performance.csv")
    df.columns = df.columns.str.strip()
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["exam_score"], inplace=True)

    X = df.drop(columns=["student_id", "exam_score"])
    y = df["exam_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()
    numerical_features = X.select_dtypes(exclude=["object"]).columns.tolist()

    # Define separate pipelines for numerical and categorical preprocessing
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy="median")),
        ('scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy="most_frequent")),
        ('encoder', OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    # Combine preprocessing steps using ColumnTransformer
    preprocessor = ColumnTransformer([
        ('num', num_pipeline, numerical_features),
        ('cat', cat_pipeline, categorical_features)
    ])

    # Create a full model pipeline combining preprocessing and the model
    full_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # Train the whole pipeline
    full_pipeline.fit(X_train, y_train)

    train_pred = full_pipeline.predict(X_train)
    test_pred = full_pipeline.predict(X_test)

    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)

    print(f"Training R² : {train_r2:.4f}")
    print(f"Testing R²  : {test_r2:.4f}")

    # Return the entire pipeline so it handles raw text automatically
    return full_pipeline
