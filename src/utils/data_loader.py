import pandas as pd
from typing import Optional

def load_kb(filepath: str) -> pd.DataFrame:
    """Load knowledge base from Excel file."""
    try:
        df = pd.read_excel(filepath)
        df = df.dropna(subset=['Note Title', 'Description'])
        df['combined_text'] = df['Note Title'] + ". " + df['Description']
        return df
    except Exception as e:
        raise Exception(f"Error loading knowledge base: {str(e)}")

def validate_kb_structure(df: pd.DataFrame) -> bool:
    """Validate that the knowledge base has required columns."""
    required_columns = ['Note Title', 'Description']
    return all(col in df.columns for col in required_columns)