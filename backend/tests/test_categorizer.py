import pytest
import pandas as pd
from app.services.categorizer import categorize_transactions


class TestCategorizer:
    """Tests for the categorizer service."""

    def test_categorize_exact_match(self):
        """Test exact keyword matching (case-insensitive)."""
        df = pd.DataFrame({
            'Details': ['STARBUCKS', 'UBER', 'SALARY', 'UNKNOWN MERCHANT'],
            'Category': ['Uncategorized'] * 4
        })
        
        keyword_map = {
            'starbucks': 1,
            'uber': 2,
            'salary': 3
        }
        uncategorized_id = 99
        
        result = categorize_transactions(df, keyword_map, uncategorized_id)
        
        assert result.iloc[0]['Category'] == 1  # STARBUCKS -> Food
        assert result.iloc[1]['Category'] == 2  # UBER -> Transport
        assert result.iloc[2]['Category'] == 3  # SALARY -> Salary
        assert result.iloc[3]['Category'] == 99  # UNKNOWN MERCHANT -> Uncategorized

    def test_categorize_case_insensitive(self):
        """Test that matching is case-insensitive."""
        df = pd.DataFrame({
            'Details': ['starbucks', 'Starbucks', 'STARBUCKS', 'StArBuCkS'],
            'Category': ['Uncategorized'] * 4
        })
        
        keyword_map = {'starbucks': 1}
        uncategorized_id = 99
        
        result = categorize_transactions(df, keyword_map, 99)
        
        for i in range(4):
            assert result.iloc[i]['Category'] == 1

    def test_categorize_strips_whitespace(self):
        """Test that details are stripped before matching."""
        df = pd.DataFrame({
            'Details': [' STARBUCKS ', ' STARBUCKS', 'STARBUCKS ', 'STARBUCKS'],
            'Category': ['Uncategorized'] * 4
        })
        
        keyword_map = {'starbucks': 1}
        uncategorized_id = 99
        
        result = categorize_transactions(df, keyword_map, 99)
        
        for i in range(4):
            assert result.iloc[i]['Category'] == 1

    def test_categorize_partial_match(self):
        """Test that matching works with keyword contained in details."""
        df = pd.DataFrame({
            'Details': ['STARBUCKS', 'STARBUCKS COFFEE', 'COFFEE STARBUCKS', 'STARBUCKS COFFEE SHOP #123'],
            'Category': ['Uncategorized'] * 4
        })
        
        keyword_map = {'starbucks': 1}
        uncategorized_id = 99
        
        result = categorize_transactions(df, keyword_map, 99)
        
        assert result.iloc[0]['Category'] == 1  # Exact match
        assert result.iloc[1]['Category'] == 1  # Partial match - STARBUCKS in STARBUCKS COFFEE
        assert result.iloc[2]['Category'] == 1  # Partial match - STARBUCKS in COFFEE STARBUCKS
        assert result.iloc[3]['Category'] == 1  # Partial match - STARBUCKS in STARBUCKS COFFEE SHOP #123

    def test_categorize_handles_none_uncategorized(self):
        """Test behavior when uncategorized_id is None."""
        df = pd.DataFrame({
            'Details': ['STARBUCKS', 'UNKNOWN'],
            'Category': ['Uncategorized', 'Uncategorized']
        })
        
        keyword_map = {'starbucks': 1}
        uncategorized_id = None
        
        result = categorize_transactions(df, keyword_map, None)
        
        assert result.iloc[0]['Category'] == 1
        assert result.iloc[1]['Category'] == 'Uncategorized'

    def test_categorize_preserves_other_columns(self):
        """Test that categorization doesn't modify other columns."""
        df = pd.DataFrame({
            'Date': ['2024-01-15', '2024-01-16'],
            'Details': ['STARBUCKS', 'UBER'],
            'Amount': [25.50, 45.00],
            'Currency': ['AED', 'AED'],
            'Debit/Credit': ['Debit', 'Debit'],
            'Status': ['SETTLED', 'SETTLED'],
            'Category': ['Uncategorized', 'Uncategorized']
        })
        
        keyword_map = {'starbucks': 1, 'uber': 2}
        uncategorized_id = 99
        
        result = categorize_transactions(df, keyword_map, 99)
        
        # Check original columns preserved
        assert result.iloc[0]['Date'] == '2024-01-15'
        assert result.iloc[0]['Amount'] == 25.50
        assert result.iloc[0]['Currency'] == 'AED'
        assert result.iloc[0]['Debit/Credit'] == 'Debit'
        assert result.iloc[0]['Status'] == 'SETTLED'
        assert result.iloc[0]['Category'] == 1

    def test_categorize_empty_dataframe(self):
        """Test categorizing empty DataFrame."""
        df = pd.DataFrame({
            'Details': [],
            'Category': []
        })
        
        keyword_map = {'starbucks': 1}
        uncategorized_id = 99
        
        result = categorize_transactions(df, keyword_map, 99)
        
        assert len(result) == 0

    def test_categorize_keyword_map_empty(self):
        """Test categorization with empty keyword map."""
        df = pd.DataFrame({
            'Details': ['STARBUCKS', 'UBER'],
            'Category': ['Uncategorized', 'Uncategorized']
        })
        
        keyword_map = {}
        uncategorized_id = 99
        
        result = categorize_transactions(df, keyword_map, 99)
        
        assert result.iloc[0]['Category'] == 99
        assert result.iloc[1]['Category'] == 99

    def test_categorize_longer_keywords_matched_first(self):
        """Test that longer keywords are matched before shorter ones."""
        df = pd.DataFrame({
            'Details': ['STARBUCKS COFFEE', 'STARBUCKS'],
            'Category': ['Uncategorized'] * 2
        })
        
        # Both keywords exist, longer one should match first
        keyword_map = {'starbucks': 1, 'starbucks coffee': 2}
        uncategorized_id = 99
        
        result = categorize_transactions(df, keyword_map, 99)
        
        # STARBUCKS COFFEE should match the longer keyword (category 2)
        assert result.iloc[0]['Category'] == 2
        # STARBUCKS should match the shorter keyword (category 1)
        assert result.iloc[1]['Category'] == 1

    def test_categorize_preserves_dataframe_order(self):
        """Test that row order is preserved."""
        df = pd.DataFrame({
            'Details': ['STARBUCKS', 'UBER', 'SALARY', 'AMAZON'],
            'Category': ['Uncategorized'] * 4
        })
        
        keyword_map = {'starbucks': 1, 'uber': 2, 'salary': 3, 'amazon': 4}
        uncategorized_id = 99
        
        result = categorize_transactions(df, keyword_map, 99)
        
        categories = result['Category'].tolist()
        assert categories == [1, 2, 3, 4]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])