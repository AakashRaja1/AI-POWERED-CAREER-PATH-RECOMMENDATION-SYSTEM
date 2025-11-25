import os
import pandas as pd
from app.core.config import DATA_PATH


def load_dataset():
    """Load the CSV dataset referenced by config. Returns an empty DataFrame if file missing."""
    try:
        if not os.path.exists(DATA_PATH):
            return pd.DataFrame()
        return pd.read_csv(DATA_PATH)
    except Exception:
        return pd.DataFrame()
