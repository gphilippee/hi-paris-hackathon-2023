from .utils import (
    read_data,
    save_data,
    calculate_utils,
    apply_regex,
    apply_ordinal,
)
from .columns import (
    columns_to_drop,
    columns_to_ohe,
    float_columns,
    binary_columns,
    re_columns,
    compute_conditions,
)

from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

import pandas as pd
import os
from pathlib import Path
import numpy as np
import sys


def process_with_ordinal(data, metrics):
    """Process data with ordinal encoding.

    Args:
        data (pd.DataFrame): Data to process.
        metrics (list): List of metrics to process.

    Returns:
        pd.DataFrame: Processed data.
    """

    # transform lower_floor_material
    data["lower_floor_material"] = (
        data["lower_floor_material"].str.lower().str.contains("concrete")
    )

    # transform upper_floor_material
    data["upper_floor_material"] = (
        data["upper_floor_material"].str.lower().str.contains("wood")
    )

    # transform outer_wall_thickness
    data["outer_wall_thickness"] = (
        data["outer_wall_thickness"]
        .astype(str)
        .apply(lambda x: x.split()[0])
        .replace("nan", np.nan)
        .astype(float)
    )

    data["outer_wall_thickness"] = (
        data["outer_wall_thickness"]
        .fillna(metrics["outer_wall_thickness"])
        .astype(float)
    )

    ordinal_columns = compute_conditions(data)

    for column, condlist, choicelist in ordinal_columns:
        data = apply_ordinal(data, column, condlist, choicelist)

    return data


def process_columns_with_regex(data):
    """Process columns with regex

    Args
        data (pd.DataFrame): Dataframe to process

    Returns
        data (pd.DataFrame): Processed dataframe
    """
    for column, labels, regexes in re_columns:
        data = apply_regex(data, column, labels, regexes)
    return data


def preprocess_pandas(data_train, data_test):
    """Preprocess the data using pandas.

    Args:
        data_train: training data
        data_test: test data

    Returns:
        data_train: preprocessed training data
        data_test: preprocessed test data
    """
    # drop columns
    data_train = data_train.drop(columns=columns_to_drop)
    data_test = data_test.drop(columns=columns_to_drop)

    metrics = calculate_utils(data_train)

    # process columns with ordinal encoding
    X_train = process_with_ordinal(data_train, metrics)
    X_test = process_with_ordinal(data_test, metrics)

    # process columns with regex
    X_train = process_columns_with_regex(X_train)
    X_test = process_columns_with_regex(X_test)

    return X_train, X_test


def init_pipeline():
    """Initialize the pipeline."""
    # Pipeline for binary categorical features
    binary_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="constant", fill_value=False)),
            ("binary_ohe", OneHotEncoder(drop="first", sparse_output=False)),
        ]
    )

    # Column transformer with 3 strategies for different column types
    # 1. Binary categorical features
    # 2. One hot encoding
    # 3. Numeric features
    preprocessing = ColumnTransformer(
        [
            ("to_binary_preproc", binary_pipeline, binary_columns),
            (
                "ohe",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                columns_to_ohe,
            ),
            ("impute", SimpleImputer(), float_columns),
        ],
        remainder="passthrough",
    )

    pipe = Pipeline(
        [
            ("preproc", preprocessing),
        ]
    )

    return pipe


def preprocess(data_dir: Path, output_dir: Path):
    """Main entry point to preprocess the preprocessing on the data.
    Args:
        data_dir: input data directory
        output_dir: directory where to write the output file

    Returns:
        None
    """
    output_dir.mkdir(exist_ok=True)

    if not os.path.exists(data_dir):
        raise Exception("Please run download_data.py first")

    # Create train and test folder
    train_dir = output_dir / "train"
    test_dir = output_dir / "test"
    train_dir.mkdir(exist_ok=True)
    test_dir.mkdir(exist_ok=True)

    data_train, labels_train, data_test = read_data(data_dir)

    # Delete outliers target
    idx_outliers = labels_train[
        (labels_train["energy_consumption_per_annum"] > 50000)
        | (labels_train["energy_consumption_per_annum"] < 0)
    ].index
    data_train = data_train.drop(idx_outliers)
    labels_train = labels_train.drop(idx_outliers)

    print("Initial shape", data_train.shape)

    # Preprocessing with pandas
    X_train_processed, X_test_processed = preprocess_pandas(data_train, data_test)

    # Preprocessing with sklearn
    pipe = init_pipeline()

    # Fit the pipeline and transform the data
    X_train_processed = pipe.fit_transform(X_train_processed)
    X_test_processed = pipe.transform(X_test_processed)

    print("Final shape", X_train_processed.shape)

    # Assert that the number of features is the same in train and test
    assert X_test_processed.shape[1] == X_train_processed.shape[1]
    assert len(pipe.get_feature_names_out()) == X_train_processed.shape[1]

    # Get the feature names
    columns_name = pipe.get_feature_names_out()

    # To dataframe and give column names
    X_train_processed = pd.DataFrame(
        X_train_processed, columns=columns_name, index=data_train.index
    )
    X_test_processed = pd.DataFrame(
        X_test_processed, columns=columns_name, index=data_test.index
    )

    # Save
    save_data(train_dir, test_dir, X_train_processed, X_test_processed, labels_train)
    print("CSVs saved")
