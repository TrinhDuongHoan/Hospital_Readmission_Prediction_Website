from pathlib import Path
from typing import List, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from src.common.constants import (
    RAW_DATA_PATH,
    MISSING_VALUES,
    TARGET_COLUMN,
    TARGET_BINARY_COLUMN,
    DROP_COLUMNS,
    HIGH_MISSING_DROP_COLUMNS,
    DIAG_COLUMNS,
    SELECTED_FEATURES,
)



def load_data(file_path: str) -> pd.DataFrame:
    """Load the diabetes readmission dataset from a CSV file.

    Args:
        file_path (str): The path to the CSV file containing the dataset.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded dataset.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = pd.read_csv(file_path, na_values=MISSING_VALUES)
    return df

def create_target(df: pd.DataFrame) -> pd.DataFrame:
    """Create a binary target variable for readmission.

    Args:
        df (pd.DataFrame): The input DataFrame containing the dataset.

    Returns:
        pd.DataFrame: A DataFrame with the new target variable.
    """
    df = df.copy()
    df[TARGET_BINARY_COLUMN] = df[TARGET_COLUMN].apply(lambda x: 1 if x in ["<30", ">30"] else 0)
    return df

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the DataFrame by dropping unnecessary columns and handling missing values.

    Args:
        df (pd.DataFrame): The input DataFrame containing the dataset.
    Returns:
        pd.DataFrame: A cleaned DataFrame ready for analysis.
    """
    df = df.copy()
    drop_cols = [col for col in DROP_COLUMNS + HIGH_MISSING_DROP_COLUMNS if col in df.columns]
    df = df.drop(columns=drop_cols)

    for col in DIAG_COLUMNS:
        if col in df.columns:
            df[col] = df[col].fillna("missing").astype(str)

    object_cols = df.select_dtypes(include=["object"]).columns.tolist()

    for col in object_cols:
        if col not in [TARGET_BINARY_COLUMN]:
            df[col] = df[col].fillna("missing").astype(str)

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    for col in numeric_cols:
        if col not in [TARGET_BINARY_COLUMN]:
            df[col] = df[col].fillna(df[col].median())

    return df

def prepare_xy(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Prepare the feature matrix X and target vector y for modeling.

    Args:
        df (pd.DataFrame): The input DataFrame containing the dataset.
    Returns:
        Tuple[pd.DataFrame, pd.Series]: A tuple containing the feature matrix X and target
        vector y.
    """
    df = df.copy()

    y = df[TARGET_BINARY_COLUMN]

    missing_features = [col for col in SELECTED_FEATURES if col not in df.columns]
    if missing_features:
        raise ValueError(f"Missing selected features: {missing_features}")

    X = df[SELECTED_FEATURES].copy()

    for bad_col in [TARGET_COLUMN, TARGET_BINARY_COLUMN]:
        if bad_col in X.columns:
            raise ValueError(f"Leakage detected: {bad_col} is still in X")

    return X, y

def split_data(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split the dataset into training and testing sets.

    Args:
        X (pd.DataFrame): The feature matrix.
        y (pd.Series): The target vector.
        test_size (float, optional): The proportion of the dataset to include in the test split. Defaults to 0.2.
        random_state (int, optional): Controls the randomness of the split. Defaults to 42.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: A tuple containing the training and testing sets for features and target.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def get_feature_types(X: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """Identify categorical and numerical feature columns.

    Args:
        X (pd.DataFrame): The feature matrix.
    Returns:
        Tuple[List[str], List[str]]: A tuple containing lists of categorical and numerical feature column
        names.
    """
    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()
    numerical_features = X.select_dtypes(include=["number"]).columns.tolist()
    return categorical_features, numerical_features

def preprocess_pipeline(file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, List[str], List[str]]:
    """Preprocess the diabetes readmission dataset.

    Args:
        file_path (str): The path to the CSV file containing the dataset.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, List[str], List[str]]: A tuple containing the training and testing sets for features and target, as well as lists of categorical and numerical feature column names.
    """
    df = load_data(file_path)
    df = create_target(df)
    df = clean_dataframe(df)
    X, y = prepare_xy(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    categorical_features, numerical_features = get_feature_types(X_train)

    return X_train, X_test, y_train, y_test, categorical_features, numerical_features

if __name__ == "__main__" :
    X_train, X_test, y_train, y_test, cat_cols, num_cols = preprocess_pipeline(
        RAW_DATA_PATH
    )

    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)
    print("\nTarget distribution in y_train:")
    print(y_train.value_counts(normalize=True))

    print("\nNumber of categorical features:", len(cat_cols))
    print("Number of numeric features:", len(num_cols))

    print("\nSample categorical columns:", cat_cols[:10])
    print("Sample numeric columns:", num_cols[:10])