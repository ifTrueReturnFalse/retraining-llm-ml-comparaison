import pandas as pd


def get_filling_rate(column: pd.Series) -> float:
    """
    Calculates the percentage of non-null values in a pandas Series.

    :param column: The pandas Series to analyze.
    :return: The filling rate as a percentage (0.0 to 100.0).
    """
    if column.empty:
        return 0.0
    # column.notnull() creates a boolean mask, .mean() calculates the ratio of True values
    return column.notnull().mean() * 100
