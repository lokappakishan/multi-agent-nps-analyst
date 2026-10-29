import pandas as pd
import pytest

from tools.nps_calculator import calculate_nps


def test_calculate_nps_with_mixed_responses():
    scores = [10] * 50 + [8] * 30 + [6] * 20
    df = pd.DataFrame({"score": scores})

    result = calculate_nps(df)

    assert result["total_responses"] == 100
    assert result["promoters"] == 50
    assert result["passives"] == 30
    assert result["detractors"] == 20

    assert result["promoter_percentage"] == pytest.approx(50.0)
    assert result["detractor_percentage"] == pytest.approx(20.0)
    assert result["nps"] == pytest.approx(30.0)


def test_calculate_nps_with_all_promoters():
    df = pd.DataFrame({"score": [9, 10, 9, 10]})

    result = calculate_nps(df)

    assert result["promoters"] == 4
    assert result["passives"] == 0
    assert result["detractors"] == 0
    assert result["nps"] == pytest.approx(100.0)


def test_calculate_nps_with_all_passives():
    df = pd.DataFrame({"score": [7, 8, 7, 8]})

    result = calculate_nps(df)

    assert result["promoters"] == 0
    assert result["passives"] == 4
    assert result["detractors"] == 0
    assert result["nps"] == pytest.approx(0.0)


def test_calculate_nps_with_all_detractors():
    df = pd.DataFrame({"score": [0, 3, 6, 4]})

    result = calculate_nps(df)

    assert result["promoters"] == 0
    assert result["passives"] == 0
    assert result["detractors"] == 4
    assert result["nps"] == pytest.approx(-100.0)


def test_calculate_nps_with_empty_dataframe():
    df = pd.DataFrame({"score": []})

    with pytest.raises(ValueError):
        calculate_nps(df)


def test_calculate_nps_with_missing_score_column():
    df = pd.DataFrame({"rating": [9, 8, 6]})

    with pytest.raises(KeyError):
        calculate_nps(df)

def test_calculate_nps_rejects_scores_above_10():
    df = pd.DataFrame({"score": [10, 8, 15]})

    with pytest.raises(ValueError, match="between 0 and 10"):
        calculate_nps(df)


def test_calculate_nps_rejects_negative_scores():
    df = pd.DataFrame({"score": [9, 5, -1]})

    with pytest.raises(ValueError, match="between 0 and 10"):
        calculate_nps(df)


def test_calculate_nps_rejects_missing_scores():
    df = pd.DataFrame({"score": [10, None, 6]})

    with pytest.raises(ValueError, match="missing values"):
        calculate_nps(df)


def test_calculate_nps_rejects_fractional_scores():
    df = pd.DataFrame({"score": [9, 8.5, 6]})

    with pytest.raises(ValueError, match="whole numbers"):
        calculate_nps(df)