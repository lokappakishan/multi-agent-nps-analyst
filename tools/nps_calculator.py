import pandas as pd

def calculate_nps(df: pd.DataFrame) -> dict:
    """Calculate Net Promoter Score from validated survey responses.

    Args:
        df: DataFrame containing a numeric 'score' column with integer
            NPS scores ranging from 0 to 10.

    Returns:
        A dictionary containing response counts, percentages, and NPS.

    Raises:
        KeyError: If the 'score' column is missing.
        ValueError: If the DataFrame is empty or scores are invalid.
    """

    if "score" not in df.columns:
        raise KeyError("Missing required column: 'score'")

    if df.empty:
        raise ValueError("Cannot calculate NPS from an empty DataFrame")

    scores = df["score"]

    if scores.isna().any():
        raise ValueError("Score column cannot contain missing values")

    if not pd.api.types.is_numeric_dtype(scores):
        raise ValueError("Scores must be numeric")

    if ((scores < 0) | (scores > 10)).any():
        raise ValueError("Scores must be between 0 and 10")

    if (scores % 1 != 0).any():
        raise ValueError("Scores must be whole numbers")

    total_responses = len(df)

    promoters = (scores >= 9).sum()
    passives = ((scores >= 7) & (scores <= 8)).sum()
    detractors = (scores <= 6).sum()

    promoter_percentage = (promoters / total_responses) * 100
    detractor_percentage = (detractors / total_responses) * 100

    nps = promoter_percentage - detractor_percentage

    return {
        "total_responses": total_responses,
        "promoters": int(promoters),
        "passives": int(passives),
        "detractors": int(detractors),
        "promoter_percentage": float(promoter_percentage),
        "detractor_percentage": float(detractor_percentage),
        "nps": float(nps),
    }