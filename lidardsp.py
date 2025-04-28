import pandas as pd
import numpy as np


def apply_L0(channel: str):
    return

def spatial_avg(channel: str):
    return

def time_avg(channel: str):
    return

def log_y(channel: str):
    return

def spatial_moving_average(volts, n=3):
    volts = np.zeros((4082))
    for i in range(len(volts)):
        volts_avg = np.vstack([volts_avg, moving_average(volts[i], n)])
    return volts_avg

def height_correction(volts, height, spatial_resol = 7.5)
    return np.power(volts,2)/spatial_resol**2
    return

def binval2volt():
    return

def binnum2height():
    return

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def bias_correction(volts, bias_window = 500):
    for i in range(len(volts)):
        volts[i] = volts[i] - np.average(volts[i,-bias_window:])
    return volts


