import re
import pandas as pd
from typing import Dict, Optional


def normalize_for_match(text: str) -> str:
    """Lowercase and strip punctuation so 'NETFLIX.COM' and 'NETFLIX COM' compare equal."""
    return re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Z0-9\s]', ' ', text)).strip().lower()


def keyword_match(keyword: str, details: str) -> bool:
    """Check if keyword matches details using word-based matching.

    A keyword matches if all its significant words (length >= 3) are present in the details.
    Both sides are normalized (case + punctuation) so comparisons are symmetric.
    """
    keyword_clean = normalize_for_match(keyword)
    details_clean = normalize_for_match(details)

    # An empty keyword (punctuation-only) must not match everything
    if not keyword_clean:
        return False

    # Simple substring match first (fast path)
    if keyword_clean in details_clean:
        return True

    keyword_words = set(keyword_clean.split())
    details_words = set(details_clean.split())

    # All-short keywords (e.g. "CO") have no significant words and must not match everything
    return bool(keyword_words) and keyword_words.issubset(details_words)


def categorize_transactions(
    df: pd.DataFrame,
    keyword_map: Dict[str, int],
    uncategorized_id: Optional[int]
) -> pd.DataFrame:
    """Categorize transactions using keyword matching (case-insensitive).

    Matches if keyword's significant words are all contained in transaction details.
    Longer keywords are matched first for more specific matching.
    Preserves existing categories for transactions with no matching keyword.
    """
    # Initialize Category column with 'Uncategorized' only for new rows (where it doesn't exist)
    if 'Category' not in df.columns:
        df['Category'] = 'Uncategorized'

    # Sort keywords by length descending to match longer keywords first
    # (e.g., "STARBUCKS COFFEE" before "STARBUCKS")
    sorted_keywords = sorted(keyword_map.keys(), key=len, reverse=True)

    for idx, row in df.iterrows():
        details = row['Details'].lower().strip()
        matched = False

        for keyword in sorted_keywords:
            if keyword_match(keyword, details):
                df.at[idx, 'Category'] = keyword_map[keyword]
                matched = True
                break

        if not matched and uncategorized_id is not None:
            df.at[idx, 'Category'] = uncategorized_id

    return df
