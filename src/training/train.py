from pathlib import Path
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression

from src.training.preprocess import preprocess_pipeline

MODEL_OUTPUT_PATH = "artifacts/models/logistic_baseline.joblib"

def build_model_pipeline(categorical_features, numerical_features) -> Pipeline:
    """Build a machine learning pipeline for training a logistic regression model.

    Args:
        categorical_features (List[str]): A list of names of categorical features.
        numerical_features (List[str]): A list of names of numerical features.

    Returns:
        Pipeline: A scikit-learn Pipeline object that can be used for training.
    """
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    numerical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_transformer, numerical_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = LogisticRegression(
        max_iter = 1000,
        class_weight = "balanced",
        random_state = 42
    )

    pipeline = Pipeline(
        steps = [
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    return pipeline

def train_model():
    X_train, X_test, y_train, y_test, categorical_features, numerical_features = preprocess_pipeline(
        "data/raw/diabetic_data.csv"
    )

    pipeline = build_model_pipeline(categorical_features, numerical_features)

    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, MODEL_OUTPUT_PATH)

    print(f"Model trained and saved to {MODEL_OUTPUT_PATH}")
    print("Training complete.")

    return pipeline, X_test, y_test

if __name__ == "__main__":
    model_pipeline, X_test, y_test = train_model()