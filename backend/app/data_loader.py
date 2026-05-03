"""
Model artifact loader. It locates trained career recommendation files and loads them in one place so prediction code does not repeat file-handling logic.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

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
