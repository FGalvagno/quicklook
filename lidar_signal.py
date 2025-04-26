import pandas as pd
import numpy as np

class lidar_Signal:
    def __init__(self, channels: dict[str, pd.DataFrame], metadata: pd.DataFrame):
        self.channels = channels  # Dictionary with channel names as keys and DataFrames as values
        self.metadata = metadata  # DataFrame with metadata

    def apply_L0(self, channel: str):
        return

    def spatial_avg(self, channel: str):
        return

    def time_avg(self, channel: str):
        return

    def log_y(self, channel: str):
        return
