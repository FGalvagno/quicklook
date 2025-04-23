import pandas as pd
import numpy as np

class lidar_Signal:
    def __init__(self, channels: dict[str, pd.DataFrame], metadata: pd.DataFrame):
        """
        Initialize the Signal class.

        Args:
            channels (dict): Dictionary of channel names mapping to their respective DataFrames.
            metadata (pd.DataFrame): Metadata associated with the signal.
        """
        self.channels = channels  # Dictionary with channel names as keys and DataFrames as values
        self.metadata = metadata  # DataFrame with metadata

    def apply_L0(self, channel: str):
        """
        Set negative values in the specified channel to 0.
        """
        if channel in self.channels:
            self.channels[channel] = self.channels[channel].clip(lower=0)

    def spatial_avg(self, channel: str):
        """
        Replace channel data with its spatial average (mean over rows).
        """
        if channel in self.channels:
            mean_vals = self.channels[channel].mean(axis=1)
            self.channels[channel] = pd.DataFrame(mean_vals, columns=[channel])

    def time_avg(self, channel: str):
        """
        Replace channel data with its time average (mean over columns).
        """
        if channel in self.channels:
            mean_vals = self.channels[channel].mean(axis=0)
            self.channels[channel] = pd.DataFrame([mean_vals], columns=self.channels[channel].columns)

    def log_y(self, channel: str):
        """
        Apply log10 to all values in the channel. Values <= 0 are set to NaN.
        """
        if channel in self.channels:
            self.channels[channel] = self.channels[channel].applymap(lambda x: np.log10(x) if x > 0 else np.nan)
