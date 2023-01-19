import pandas as pd
import numpy as np
from pathlib import Path
from typing import List


def read_data(base_path: Path) -> tuple:
    """Read data from csv files and return X_train, y_train and X_test

    Args:
        base_path (str): path to the data directory

    Returns:
        data_train (pd.DataFrame): training data
        labels_train (pd.DataFrame): training labels
        data_test (pd.DataFrame): test data
    """
    data_train = pd.read_csv(
        base_path / "train/train_features_sent.csv",
        index_col="level_0",
        low_memory=False,
    )
    labels_train = pd.read_csv(
        base_path / "train/train_labels_sent.csv", index_col="level_0", low_memory=False
    )
    data_test = pd.read_csv(
        base_path / "test/test_features_sent.csv", index_col="level_0", low_memory=False
    )
    return data_train, labels_train, data_test


def save_data(train_dir, test_dir, X_train, X_test, y_train):
    """Save data to csv files

    Args:
        train_dir (str): path to the train directory
        test_dir (str): path to the test directory
        X_train (pd.DataFrame): training data
        y_train (pd.DataFrame): training labels
        X_test (pd.DataFrame): test data

    """
    X_train.to_csv(train_dir / "X_train_processed.csv")
    y_train.to_csv(train_dir / "labels_train_processed.csv")
    X_test.to_csv(test_dir / "X_test_processed.csv")


def calculate_utils(data_train):
    """Calculate metrics for the preprocessing pipeline

    Args:
        data_train (pd.DataFrame): training data

    Returns:
        metrics (dict): dictionary of metrics
    """
    metrics = dict()
    data_train["outer_wall_thickness"] = (
        data_train["outer_wall_thickness"].str.split(expand=True)[0].astype(float)
    )
    metrics["outer_wall_thickness"] = data_train["outer_wall_thickness"].mean()
    return metrics


def apply_regex(data, column_name, columns, regexs):
    """Apply regex to a column of a dataframe

    Args:
        data (pd.DataFrame): dataframe
        column_name (str): name of the column to apply the regex to
        columns (list): list of columns to create
        regexs (list): list of regexs to apply

    Returns:
        data (pd.DataFrame): dataframe with new columns
    """
    for col, regex in zip(columns, regexs):
        data[col] = (
            data[column_name]
            .str.lower()
            .fillna("other")
            .apply(lambda x: float(bool(regex.search(x))))
        )
    return data.drop(columns=[column_name])


def apply_ordinal(data, column_name, condlist: List, choicelist: List):
    data[column_name] = np.select(condlist, choicelist)
    return data
