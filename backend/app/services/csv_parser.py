import pandas as pd
import io
from typing import List, Dict, Any


def parse_csv(content: bytes) -> pd.DataFrame:
    """Parse CSV content with flexible column detection."""
    # Try to read CSV with quoted field support
    df = pd.read_csv(io.BytesIO(content), quotechar='"')
    
    # Normalize column names (strip whitespace, case-insensitive matching)
    df.columns = [col.strip() for col in df.columns]
    
    # Required columns mapping (case-insensitive)
    col_map = {}
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ['date', 'transaction date', 'txn date']:
            col_map[col] = 'Date'
        elif col_lower in ['details', 'description', 'merchant', 'payee', 'narration']:
            col_map[col] = 'Details'
        elif col_lower in ['amount', 'value', 'txn amount', 'transaction amount']:
            col_map[col] = 'Amount'
        elif col_lower in ['currency', 'curr']:
            col_map[col] = 'Currency'
        elif col_lower in ['debit/credit', 'debit credit', 'type', 'dr/cr', 'debit_credit']:
            col_map[col] = 'Debit/Credit'
        elif col_lower in ['status', 'state']:
            col_map[col] = 'Status'
    
    # Check required columns
    required = ['Date', 'Details', 'Amount', 'Debit/Credit']
    for req in required:
        if req not in col_map.values():
            raise ValueError(f'Required column not found: {req}')
    
    # Rename columns
    df = df.rename(columns=col_map)
    
    # Parse dates with multiple format support
    date_formats = ['%d %b %Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']
    for fmt in date_formats:
        try:
            df['Date'] = pd.to_datetime(df['Date'], format=fmt)
            break
        except:
            continue
    else:
        # Try pandas default parsing
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Clean amount: remove commas, currency symbols, backslashes
    df['Amount'] = df['Amount'].astype(str).str.replace(r'[,\$\\]', '', regex=True).astype(float)
    
    # Normalize debit/credit
    df['Debit/Credit'] = df['Debit/Credit'].str.strip().str.capitalize()
    
    # Default currency and status
    if 'Currency' not in df.columns:
        df['Currency'] = 'AED'
    if 'Status' not in df.columns:
        df['Status'] = 'SETTLED'
    
    return df[['Date', 'Details', 'Amount', 'Currency', 'Debit/Credit', 'Status']]