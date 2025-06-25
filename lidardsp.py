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
    return data.resample(time=time, skipna=True).mean() #Time average

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def spatial_moving_average(signal, n=10):
    kernel = np.ones(n) / n
    smoothed_values = np.apply_along_axis(lambda m: np.convolve(m, kernel, mode='same'), axis=1, arr=signal.values)
    return smoothed_values

## L0 FUNCTIONS

def offset_correction(signal, offset): 
    signal = signal.isel(bins=slice(offset, None)) #index all but first offset samples
    signal = signal.assign_coords(bins=signal.coords['bins'].values - offset) #reassign bins correct values
    return signal 
    

def volts_height_correction(signal, channel_info):
    height = signal['height'].values
    return np.power(height,2)*signal.values

def binval2volt(signal, channel_info):
    return signal.values * (channel_info['data_acquisition_range']/1000/(2**channel_info['analog_to_digital_resolution']-1))

def binnum2height(bins, channel_info, use_Km = True):
    if use_Km:
        return np.array(bins*channel_info['range_resolution']/1e3)
    else:
        return np.array(bins*channel_info['range_resolution'])

def bias_correction(signal, bias_window = 500):
    volts = signal.values
    volts = volts[:, -bias_window:].mean(axis=1, keepdims=True)
    return signal.values - volts

#def remove_dark_current(dark_current_file, signal, channel_name):
