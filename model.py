import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
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
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    categorical_features = X.select_dtypes(
        include=["object"]
    ).columns.tolist()

    numerical_features = X.select_dtypes(
        exclude=["object"]
    ).columns.tolist()



    num_imputer = SimpleImputer(
        strategy="median"
    )

    scaler = StandardScaler()


    X_train_num = num_imputer.fit_transform(
        X_train[numerical_features]
    )

    X_test_num = num_imputer.transform(
        X_test[numerical_features]
    )


    X_train_num = scaler.fit_transform(
        X_train_num
    )

    X_test_num = scaler.transform(
        X_test_num
    )

    cat_imputer = SimpleImputer(
        strategy="most_frequent"
    )

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    )


    X_train_cat = cat_imputer.fit_transform(
        X_train[categorical_features]
    )

    X_test_cat = cat_imputer.transform(
        X_test[categorical_features]
    )


    X_train_cat = encoder.fit_transform(
        X_train_cat
    )

    X_test_cat = encoder.transform(
        X_test_cat
    )


    X_train_final = np.hstack(
        (
            X_train_num,
            X_train_cat
        )
    )

    X_test_final = np.hstack(
        (
            X_test_num,
            X_test_cat
        )
    )


    model = LinearRegression()

    model.fit(
        X_train_final,
        y_train
    )

    train_pred = model.predict(
        X_train_final
    )

    test_pred = model.predict(
        X_test_final
    )


    train_r2 = r2_score(
        y_train,
        train_pred
    )

    test_r2 = r2_score(
        y_test,
        test_pred
    )


    print(f"Training R² : {train_r2:.4f}")
    print(f"Testing R²  : {test_r2:.4f}")


    return model