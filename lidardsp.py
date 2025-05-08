import pandas as pd
import numpy as np
import xarray as xr
from datetime import datetime as dt, timedelta as tdelta
import read_licel as rl
import os

def read_folder(directory, date_interval, file_prefix):
    sig_raw = []
    metadata = []
    try:
        for f in os.scandir(directory):
            if f.is_dir() and dt.strptime(f.name, "%Y%m%d") >= date_interval[0] and dt.strptime(f.name, "%Y%m%d") <= date_interval[1]:
                print(f.name)
                output = rl.dtfs(directory + "/" + f.name, optimize_reading=True, file_prefix=file_prefix)
                sig_raw.append(output[3]) #[1:2] metadata [3] data
                metadata.append(output[1])
    except Exception as e:
        print(f"Error reading directory: {e}")
    
    data = xr.concat([set for set in sig_raw if len(set)], dim='time')
    first_channel_info = metadata[0]

    return data, first_channel_info

## AVG FUNCTIONS
def spatial_avg(data, n=8):
    return data.coarsen(bins=n, boundary='trim').mean()

def time_avg(data, time=tdelta(minutes=15)):
    return data.sortby('time').resample(time=time, skipna=True).mean() #Time average

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def spatial_moving_average(volts, n=10):
    volts = np.zeros(len(volts))
    for i in range(len(volts)):
        volts_avg = np.vstack([volts_avg, moving_average(volts[i], n)])
    return volts_avg

## L0 FUNCTIONS

def offset_correction(volts, offset):    
    return

def volts_height_correction(signal, channel_info):
    height = signal['height'].values
    return np.power(height,height)*signal.values/channel_info['range_resolution']**2

def binval2volt(signal, channel_info):
    return signal.values * (channel_info['data_acquisition_range']/(2**channel_info['analog_to_digital_resolution']-1))

def binnum2height(bins, channel_info, use_Km = True):
    if use_Km:
        return np.array(bins*channel_info['range_resolution']/1e3)
    else:
        return np.array(bins*channel_info['range_resolution'])

def bias_correction(signal, bias_window = 500):
    volts = signal.values
    for i in range(len(volts)):
        volts[i] = volts[i] - np.average(volts[i,-bias_window:])
    return volts


