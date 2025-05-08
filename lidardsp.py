import pandas as pd
import numpy as np


def spatial_avg(channel: str):

    return

def time_avg(volt):
    return

def offset_correction(volts, offset):
    
    return

def spatial_moving_average(volts, n=10):
    volts = np.zeros(len(volts))
    for i in range(len(volts)):
        volts_avg = np.vstack([volts_avg, moving_average(volts[i], n)])
    return volts_avg

def volts_height_correction(volts, height, spatial_resol = 7.5):
    return np.power(height,height)*volts/spatial_resol**2

def binval2volt(binval, lp={'volt_resolution': 50, 'bit_resolution': 16}):
    return binval * (lp['volt_resolution']/(2**lp['bit_resolution']-1))

def binnum2height(spatial_resol = 7.5, use_Km = True, bins = []):
    if use_Km:
        return np.array(bins*spatial_resol/1e3)
    else:
        return np.array(bins*spatial_resol)


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def bias_correction(volts, bias_window = 500):
    for i in range(len(volts)):
        volts[i] = volts[i] - np.average(volts[i,-bias_window:])
    return volts


