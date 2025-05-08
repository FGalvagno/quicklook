import os
import numpy as np
import xarray as xr
import time
import read_licel as rl
import plot
from datetime import datetime as dt, timedelta as tdelta
from yml_load import lidarConfig
import lidardsp
from plot import plot_signal
start = time.time()

import warnings
warnings.filterwarnings('ignore')

lc = lidarConfig(config_folder="./config")

directory = lc.src
days = []
date_interval = lc.get_dateinterval()

try:
    for f in os.scandir(directory):
        if f.is_dir() and dt.strptime(f.name, "%Y%m%d") >= date_interval[0] and dt.strptime(f.name, "%Y%m%d") <= date_interval[1]:
            print(f.name)
            days.append(rl.dtfs(directory + "/" + f.name, optimize_reading=True, file_prefix=lc.location_prefix)[3]) #[1:2] metadata [3] data
except Exception as e:
    print(f"Error reading directory: {e}")
    
data = xr.concat([set for set in days if len(set)], dim='time')
data = data.sortby('time')
possible_channels = data.coords['channel'].values
data = data.resample(time=tdelta(minutes=15), skipna=True).mean()
channel_name = lc.channel  # First channel
time_index = 0  

#slice the data for the selected channel
data_slice = data.sel(channel=channel_name)  # Slice by channel

##---------------APPLY L0-------------------##
height = lidardsp.binnum2height(spatial_resol=lc.licel_parameters['spatial_resolution'], use_Km=True, bins=data_slice.coords['bins'].values)
voltage = lidardsp.binval2volt(data_slice.values, lc.licel_parameters)
voltage = lidardsp.bias_correction(voltage, bias_window = lc.bias_window)
voltage = lidardsp.volts_height_correction(voltage, height, spatial_resol=lc.licel_parameters['spatial_resolution'])
#voltage = spatial_moving_average(voltage, )

timestamp = [np.datetime64(dt).astype('datetime64[s]').astype(object).strftime('%Y-%m-%d %H:%M') for dt in data_slice.coords['time'].values]
##---------------END OF L0-------------------##
#voltage_bc = voltage - voltage[:,-1]

plot_signal(volt_data=voltage, height_data=height, time_data=timestamp, channel_name=channel_name, limits=lc.plot_limits)


print(time.time()-start)


use_log = False

#if use_log is True:
#    z_axis = np.log10(np.transpose(voltage_avg)[:-2048])
#else:
#    z_axis = np.transpose(voltage_avg)[:-2048]







# <code to time>
end = time.time()