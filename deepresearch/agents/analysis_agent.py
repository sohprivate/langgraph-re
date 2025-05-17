from typing import Any, Dict
import pandas as pd

class AnalysisAgent:
    """Agent for analyzing weather data."""

    @staticmethod
    def basic_stats(weather_data: Dict[str, Any]) -> pd.DataFrame:
        """Return a DataFrame with basic stats from weather data."""
        main = weather_data.get("main", {})
        df = pd.DataFrame([main])
        stats = df.describe().T
        return stats
