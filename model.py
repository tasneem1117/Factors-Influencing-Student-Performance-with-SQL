import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def data_preprocessing(df):
    print("Dataset Shape")
    print(df.shape)

    print("=" * 50)
    print("Duplicate rows:", df.duplicated().sum())

    print("=" * 50)
    print("Missing Values")
    print(df.isnull().sum())

    numerical_columns = df.select_dtypes(include=["number"]).columns
    categorical_columns = df.select_dtypes(include=["object" , "string"]).columns

    print("=" * 50)
    print("Numerical Columns")
    print(list(numerical_columns))

    print("=" * 50)
    print("Categorical Columns")
    print(list(categorical_columns))


    print("=" * 50)
    print(df.describe())

    print("=" * 50)
    print("Correlation Matrix")
    print(df[numerical_columns].corr())

    print("=" * 50)
    print("Outlier Detection")

    for col in numerical_columns:
        if col == "exam_score":
            continue

        Q1 = df[col].quantile(.25)
        Q3 = df[col].quantile(.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        print(f"{col}: {outliers}")

    return df

def train_model():
    df = pd.read_csv("student_habits_performance.csv")
    df.columns = df.columns.str.strip()
    mock_df = pd.read_csv("MOCK_DATA.csv")
    mock_df.columns = mock_df.columns.str.strip()

    df = df.merge(mock_df, on="student_id", how="left")
    print(df.head())
    df = data_preprocessing(df)

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["exam_score"], inplace=True)

    X = df.drop(columns=["student_id", "exam_score"])
    y = df["exam_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    categorical_features = X.select_dtypes(include=["object" , "string"]).columns.tolist()
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

    preprocessor = ColumnTransformer([
        ('num', num_pipeline, numerical_features),
        ('cat', cat_pipeline, categorical_features)
    ])

    full_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    full_pipeline.fit(X_train, y_train)

    train_pred = full_pipeline.predict(X_train)
    test_pred = full_pipeline.predict(X_test)

    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)

    print(f"Training R² : {train_r2:.4f}")
    print(f"Testing R²  : {test_r2:.4f}")

    return full_pipeline


model = train_model()