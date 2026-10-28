import pandas as pd
import pytest

from tools.data_loader import (
    load_survey_data,
    validate_dates,
    validate_months,
    validate_required_columns,
    validate_required_values,
    validate_revenue,
    validate_scores,
    validate_unique_response_ids,
)


def make_valid_dataframe():
    """Return a small, valid DataFrame for testing."""
    return pd.DataFrame(
        {
            "response_id": ["R0001", "R0002"],
            "date": ["2026-07-15", "2026-08-20"],
            "month": ["2026-07", "2026-08"],
            "product": ["Credit Card", "Wealth"],
            "tenure": ["1 year", "2 years"],
            "channel": ["Mobile App", "Branch"],
            "score": [9, 4],
            "comment": ["Great service", None],
            "annual_revenue_inr": [10000, 20000],
        }
    )


def test_required_columns_accept_valid_dataframe():
    df = make_valid_dataframe()

    result = validate_required_columns(df)

    assert len(result.columns) == 9


def test_required_columns_reject_missing_column():
    df = make_valid_dataframe().drop(columns=["product"])

    with pytest.raises(ValueError, match="product"):
        validate_required_columns(df)


def test_unique_response_ids_accept_unique_ids():
    df = make_valid_dataframe()

    result = validate_unique_response_ids(df)

    assert len(result) == 2


def test_unique_response_ids_reject_duplicates():
    df = make_valid_dataframe()
    df.loc[1, "response_id"] = "R0001"

    with pytest.raises(ValueError, match="R0001"):
        validate_unique_response_ids(df)


def test_scores_accept_valid_values():
    df = make_valid_dataframe()

    result = validate_scores(df)

    assert result["score"].tolist() == [9, 4]


@pytest.mark.parametrize(
    "score",
    [-1, 11, 5.5, None],
)
def test_scores_reject_invalid_values(score):
    df = make_valid_dataframe().astype({"score": object})
    df.loc[0, "score"] = score

    with pytest.raises(ValueError, match="invalid NPS scores"):
        validate_scores(df)


def test_dates_accept_valid_dates():
    df = make_valid_dataframe()

    result = validate_dates(df)

    assert len(result) == 2


@pytest.mark.parametrize(
    "date",
    ["not-a-date", "2026-02-30", None],
)
def test_dates_reject_invalid_values(date):
    df = make_valid_dataframe()
    df.loc[0, "date"] = date

    with pytest.raises(ValueError, match="invalid dates"):
        validate_dates(df)


def test_months_accept_consistent_values():
    df = make_valid_dataframe()

    result = validate_months(df)

    assert len(result) == 2


@pytest.mark.parametrize(
    "month",
    ["not-a-month", "2026-13", None],
)
def test_months_reject_invalid_values(month):
    df = make_valid_dataframe()
    df.loc[0, "month"] = month

    with pytest.raises(ValueError, match="invalid months"):
        validate_months(df)


def test_months_reject_date_month_mismatch():
    df = make_valid_dataframe()
    df.loc[0, "month"] = "2026-08"

    with pytest.raises(ValueError, match="do not match"):
        validate_months(df)


def test_required_values_allow_missing_comment():
    df = make_valid_dataframe()

    result = validate_required_values(df)

    assert result["comment"].isna().sum() == 1


def test_required_values_reject_missing_product():
    df = make_valid_dataframe()
    df.loc[0, "product"] = None

    with pytest.raises(ValueError, match="product"):
        validate_required_values(df)


def test_revenue_accepts_valid_values():
    df = make_valid_dataframe()

    result = validate_revenue(df)

    assert result["annual_revenue_inr"].tolist() == [10000, 20000]


@pytest.mark.parametrize(
    "revenue",
    [-500, None, "not-a-number"],
)
def test_revenue_rejects_invalid_values(revenue):
    df = make_valid_dataframe().astype(
        {"annual_revenue_inr": object}
    )
    df.loc[0, "annual_revenue_inr"] = revenue

    with pytest.raises(ValueError, match="revenue"):
        validate_revenue(df)

@pytest.mark.parametrize(
    "score",
    [-1, 11, 5.5, None, "five"],
)
def test_scores_reject_invalid_values(score):
    df = make_valid_dataframe().astype({"score": object})
    df.loc[0, "score"] = score

    with pytest.raises(ValueError, match="invalid NPS scores"):
        validate_scores(df)


def test_actual_survey_dataset_loads_successfully():
    df = load_survey_data()

    assert len(df) == 600
    assert df["response_id"].is_unique
    assert df["score"].between(0, 10).all()
    assert df["comment"].isna().sum() == 64