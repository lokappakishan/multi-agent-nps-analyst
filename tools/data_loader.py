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
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )

    return df


def load_survey_data():
    print("Loading survey data")

    df = pd.read_csv(DEFAULT_DATA_PATH)

    df = validate_required_columns(df)

    return df