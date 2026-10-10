import pytest
import pandas as pd
from app.services.csv_parser import parse_csv


class TestCSVParser:
    """Tests for the CSV parser service."""

    def test_parse_basic_csv(self):
        """Test parsing a basic CSV with standard columns."""
        csv_content = b"Date,Details,Amount,Debit/Credit\n15 Jan 2024,STARBUCKS,25.50,Debit\n16 Jan 2024,SALARY,5000.00,Credit"
        df = parse_csv(csv_content)
        
        assert len(df) == 2
        assert df.iloc[0]['Details'] == 'STARBUCKS'
        assert df.iloc[0]['Amount'] == 25.5
        assert df.iloc[0]['Debit/Credit'] == 'Debit'
        assert df.iloc[1]['Details'] == 'SALARY'
        assert df.iloc[1]['Amount'] == 5000.0
        assert df.iloc[1]['Debit/Credit'] == 'Credit'

    def test_parse_csv_with_commas_in_amount(self):
        """Test parsing amounts with commas (e.g., 18,551.62)."""
        csv_content = b'Date,Details,Amount,Debit/Credit\n15 Jan 2024,"LARGE PURCHASE","18,551.62",Debit'
        df = parse_csv(csv_content)
        
        assert len(df) == 1
        assert df.iloc[0]['Amount'] == 18551.62

    def test_parse_csv_with_currency_symbols(self):
        """Test parsing amounts with currency symbols."""
        csv_content = b"Date,Details,Amount,Debit/Credit\n15 Jan 2024,STARBUCKS,$25.50,Debit"
        df = parse_csv(csv_content)
        
        assert len(df) == 1
        assert df.iloc[0]['Amount'] == 25.5

    def test_parse_csv_case_insensitive_columns(self):
        """Test that column names are case-insensitive."""
        csv_content = b"date,details,amount,debit/credit\n15 Jan 2024,STARBUCKS,25.50,Debit"
        df = parse_csv(csv_content)
        
        assert len(df) == 1
        assert 'Date' in df.columns
        assert 'Details' in df.columns
        assert 'Amount' in df.columns
        assert 'Debit/Credit' in df.columns

    def test_parse_csv_alternative_column_names(self):
        """Test parsing with alternative column names."""
        csv_content = b"Transaction Date,Description,Value,Type\n15 Jan 2024,STARBUCKS,25.50,Debit"
        df = parse_csv(csv_content)
        
        assert len(df) == 1
        assert df.iloc[0]['Details'] == 'STARBUCKS'
        assert df.iloc[0]['Amount'] == 25.5
        assert df.iloc[0]['Debit/Credit'] == 'Debit'

    def test_parse_date_formats(self):
        """Test parsing various date formats."""
        test_cases = [
            (b"Date,Details,Amount,Debit/Credit\n15 Jan 2024,TEST,10.00,Debit", '2024-01-15'),
            (b"Date,Details,Amount,Debit/Credit\n2024-01-15,TEST,10.00,Debit", '2024-01-15'),
            (b"Date,Details,Amount,Debit/Credit\n15/01/2024,TEST,10.00,Debit", '2024-01-15'),
            (b"Date,Details,Amount,Debit/Credit\n01/15/2024,TEST,10.00,Debit", '2024-01-15'),
        ]
        
        for csv_content, expected_date in test_cases:
            df = parse_csv(csv_content)
            assert len(df) == 1
            assert str(df.iloc[0]['Date'].date()) == expected_date

    def test_parse_csv_missing_required_columns(self):
        """Test that missing required columns raises ValueError."""
        csv_content = b"Date,Details\n15 Jan 2024,STARBUCKS"
        
        with pytest.raises(ValueError, match="Required column not found"):
            parse_csv(csv_content)

    def test_parse_csv_defaults_currency_and_status(self):
        """Test that currency and status default to AED and SETTLED."""
        csv_content = b"Date,Details,Amount,Debit/Credit\n15 Jan 2024,STARBUCKS,25.50,Debit"
        df = parse_csv(csv_content)
        
        assert df.iloc[0]['Currency'] == 'AED'
        assert df.iloc[0]['Status'] == 'SETTLED'

    def test_parse_csv_normalizes_debit_credit(self):
        """Test that debit/credit values are normalized."""
        test_cases = [
            (b"Date,Details,Amount,Debit/Credit\n15 Jan 2024,TEST,10.00,debit", 'Debit'),
            (b"Date,Details,Amount,Debit/Credit\n15 Jan 2024,TEST,10.00,DEBIT", 'Debit'),
            (b"Date,Details,Amount,Debit/Credit\n15 Jan 2024,TEST,10.00,credit", 'Credit'),
            (b"Date,Details,Amount,Debit/Credit\n15 Jan 2024,TEST,10.00,CREDIT", 'Credit'),
            (b"Date,Details,Amount,Debit/Credit\n15 Jan 2024,TEST,10.00,Debit ", 'Debit'),
            (b"Date,Details,Amount,Debit/Credit\n15 Jan 2024,TEST,10.00, credit", 'Credit'),
        ]
        
        for csv_content, expected in test_cases:
            df = parse_csv(csv_content)
            assert df.iloc[0]['Debit/Credit'] == expected

    def test_parse_empty_csv_raises_error(self):
        """Test that empty CSV raises appropriate error."""
        csv_content = b""
        
        with pytest.raises(Exception):
            parse_csv(csv_content)

    def test_parse_csv_only_headers(self):
        """Test CSV with only headers and no data."""
        csv_content = b"Date,Details,Amount,Debit/Credit\n"
        df = parse_csv(csv_content)
        
        assert len(df) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])