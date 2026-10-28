from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "nps_survey.csv"

REQUIRED_COLUMNS = {
    "response_id",
    "date",
    "month",
    "product",
    "tenure",
    "channel",
    "score",
    "comment",
    "annual_revenue_inr",
}


def validate_required_columns(df):
    """Ensure that all expected columns exist."""
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )

    return df


def validate_unique_response_ids(df):
    """Ensure response IDs are present and unique."""
    response_ids = df["response_id"]

    missing_mask = response_ids.isna() | (
        response_ids.astype("string").str.strip() == ""
    )

    if missing_mask.any():
        raise ValueError("Dataset contains missing or empty response IDs.")

    duplicate_mask = response_ids.duplicated(keep=False)

    if duplicate_mask.any():
        duplicate_ids = (
            response_ids[duplicate_mask]
            .unique()
            .tolist()
        )

        raise ValueError(
            f"Dataset contains duplicate response IDs: {duplicate_ids}"
        )

    return df


def validate_scores(df):
    """Ensure NPS scores are whole numbers between 0 and 10."""
    original_scores = df["score"]
    scores = pd.to_numeric(original_scores, errors="coerce")

    invalid_mask = (
        scores.isna()
        | ~scores.between(0, 10)
        | (scores % 1 != 0)
    )

    if invalid_mask.any():
        invalid_scores = (
            original_scores[invalid_mask]
            .unique()
            .tolist()
        )

        raise ValueError(
            f"Dataset contains invalid NPS scores: {invalid_scores}. "
            "Scores must be whole numbers between 0 and 10."
        )

    return df


def validate_dates(df):
    """Ensure dates are valid and use the YYYY-MM-DD format."""
    original_dates = df["date"]

    dates = pd.to_datetime(
        original_dates,
        format="%Y-%m-%d",
        errors="coerce",
    )

    invalid_mask = dates.isna()

    if invalid_mask.any():
        invalid_dates = (
            original_dates[invalid_mask]
            .unique()
            .tolist()
        )

        raise ValueError(
            f"Dataset contains missing or invalid dates: {invalid_dates}. "
            "Dates must use the YYYY-MM-DD format."
        )

    return df


def validate_months(df):
    """Ensure months are valid and match their corresponding dates."""
    original_months = df["month"]

    months = pd.to_datetime(
        original_months,
        format="%Y-%m",
        errors="coerce",
    )

    invalid_mask = months.isna()

    if invalid_mask.any():
        invalid_months = (
            original_months[invalid_mask]
            .unique()
            .tolist()
        )

        raise ValueError(
            f"Dataset contains missing or invalid months: {invalid_months}. "
            "Months must use the YYYY-MM format."
        )

    # Convert dates to datetime values instead of assuming they are strings.
    dates = pd.to_datetime(
        df["date"],
        format="%Y-%m-%d",
        errors="coerce",
    )

    # Compare the year and month, not the full date.
    expected_months = dates.dt.to_period("M")
    actual_months = months.dt.to_period("M")

    mismatch_mask = actual_months != expected_months

    if mismatch_mask.any():
        mismatches = df.loc[
            mismatch_mask, ["response_id", "date", "month"]
        ].to_dict("records")

        raise ValueError(
            "Dataset contains dates that do not match their assigned months: "
            f"{mismatches}"
        )

    return df


def validate_required_values(df):
    """Ensure required fields are not missing or empty."""
    required_value_columns = [
        "response_id",
        "date",
        "month",
        "product",
        "tenure",
        "channel",
        "score",
        "annual_revenue_inr",
    ]

    missing_counts = df[required_value_columns].isna().sum()
    columns_with_missing_values = missing_counts[missing_counts > 0]

    if not columns_with_missing_values.empty:
        raise ValueError(
            "Dataset contains missing values in required fields: "
            f"{columns_with_missing_values.to_dict()}"
        )

    # Reject empty or whitespace-only strings in required text fields.
    required_text_columns = [
        "response_id",
        "date",
        "month",
        "product",
        "tenure",
        "channel",
    ]

    empty_columns = {}

    for column in required_text_columns:
        empty_mask = (
            df[column]
            .astype("string")
            .str.strip()
            .eq("")
            .fillna(False)
        )

        if empty_mask.any():
            empty_columns[column] = int(empty_mask.sum())

    if empty_columns:
        raise ValueError(
            "Dataset contains empty values in required fields: "
            f"{empty_columns}"
        )

    return df


def validate_revenue(df):
    """Ensure annual revenue is numeric and non-negative."""
    original_revenue = df["annual_revenue_inr"]
    revenue = pd.to_numeric(original_revenue, errors="coerce")

    invalid_mask = (
        revenue.isna()
        | (revenue < 0)
    )

    if invalid_mask.any():
        invalid_values = (
            original_revenue[invalid_mask]
            .unique()
            .tolist()
        )

        raise ValueError(
            "Dataset contains missing, non-numeric, or negative revenue "
            f"values: {invalid_values}"
        )

    return df


def load_survey_data():
    """Load the survey CSV and validate it before analysis."""
    print("Loading survey data")

    df = pd.read_csv(DEFAULT_DATA_PATH)

    df = validate_required_columns(df)
    df = validate_required_values(df)
    df = validate_unique_response_ids(df)
    df = validate_scores(df)
    df = validate_dates(df)
    df = validate_months(df)
    df = validate_revenue(df)

    return df