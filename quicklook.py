import os
import numpy as np
import xarray as xr
import time
import read_licel as rl
import plot
from datetime import datetime as dt, timedelta as tdelta
from yml_load import lidarConfig

start = time.time()

import warnings
warnings.filterwarnings('ignore')

lc = lidarConfig(config_folder="./config")

directory = lc.get_src()
days = []
date_interval = lc.get_dateinterval()

try:
    for f in os.scandir(directory):
        if f.is_dir() and dt.strptime(f.name, "%Y%m%d") >= date_interval[0] and dt.strptime(f.name, "%Y%m%d") <= date_interval[1]:
            print(f.name)
            days.append(rl.dtfs(directory + "/" + f.name, optimize_reading=True, file_prefix=lc.location_prefix)[3]) #[1:2] metadata [3] data
except Exception as e:
    print(f"Error reading directory: {e}")
    
data = xr.concat(days, dim='time')

#possible_channels = data.coords['channel'].values
channel_name = lc.get_channel  # First channel
time_index = 0  

#slice the data for the selected channel
data_slice = data.sel(channel=channel_name)  # Slice by channel

height = np.array(data_slice.coords['bins'].values *7.5/1e3)
voltage = np.array(data_slice.values * (50/(2**16-1)))
timestamp = [np.datetime64(dt).astype('datetime64[s]').astype(object).strftime('%Y-%m-%d %H:%M') for dt in data_slice.coords['time'].values]

#voltage_bc = voltage - voltage[:,-1]


voltage_rc = voltage * height * height *1e3/30**2



print(time.time()-start)

time_data = 

use_log = False

if use_log is True:
    z_axis = np.log10(np.transpose(voltage_avg)[:-2048])
else:
    z_axis = np.transpose(voltage_avg)[:-2048]



# <code to time>
end = time.time()