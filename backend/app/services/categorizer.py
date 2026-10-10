import pandas as pd
from typing import Dict, Optional


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    import re
    # Remove numbers and special characters, keep only letters and spaces
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned.lower()


def get_significant_words(text: str, min_length: int = 3) -> set:
    """Extract significant words from text (length >= min_length)."""
    words = text.split()
    stop_words = {'the', 'and', 'or', 'for', 'to', 'at', 'in', 'on', 'of', 'a', 'an', 'ltd', 'inc', 'corp', 'co', 'llc', 'pvt', 'plc', 'pty'}
    return {w for w in text.split() if len(w) >= 3 and w.lower() not in {'the', 'and', 'or', 'for', 'to', 'at', 'in', 'on', 'of', 'a', 'an', 'ltd', 'inc', 'corp', 'co', 'llc', 'pvt', 'plc', 'pty'}}


def keyword_match(keyword: str, details: str) -> bool:
    """Check if keyword matches details using word-based matching.
    
    A keyword matches if all its significant words are present in the details.
    """
    keyword_clean = keyword.lower().strip()
    details_clean = details.lower().strip()
    
    # Simple substring match first (fast path)
    if keyword.lower() in details.lower():
        return True
    
    # Word-based matching: all significant words of keyword must be in details
    keyword_words = set(w for w in keyword.lower().split() if len(w) >= 3)
    details_words = set(details.lower().split())
    
    # Check if all significant keyword words are in details
    significant_keyword_words = {w for w in keyword_words if len(w) >= 3}
    return significant_keyword_words.issubset(details_words)


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