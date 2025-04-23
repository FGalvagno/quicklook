import os
import numpy as np
import xarray as xr
import time
import read_licel as rl
import plot

start = time.time()

import warnings
warnings.filterwarnings('ignore')


print(time.time()-start)
directory = "./input"
days = []

for f in os.scandir(directory):
    if f.is_dir():
        print(f.name)
        days.append(rl.dtfs(directory + "/" + f.name, optimize_reading=True)[3]) #[1:2] metadata [3] data

data = xr.concat(days, dim='time')

#possible_channels = data.coords['channel'].values
channel_name = 'BT3_L1'  # First channel
time_index = 0  

#slice the data for the selected channel
data_slice = data.sel(channel=channel_name)  # Slice by channel

height = np.array(data_slice.coords['bins'].values *7.5/1e3)
voltage = np.array(data_slice.values * (50/(2**16-1)))

#voltage_bc = voltage - voltage[:,-1]
for i in range(len(voltage)):
    voltage[i] = voltage[i] - np.average(voltage[i,-500:])

voltage_rc = voltage * height * height *1e3/30**2

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

voltage_avg = np.zeros((4082))
for i in range(len(voltage_rc)):
    voltage_avg = np.vstack([voltage_avg, moving_average(voltage_rc[i], n=15)])

print(time.time()-start)

time_data = [np.datetime64(dt).astype('datetime64[s]').astype(object).strftime('%Y-%m-%d %H:%M') for dt in data_slice.coords['time'].values]

use_log = False

if use_log is True:
    z_axis = np.log10(np.transpose(voltage_avg)[:-2048])
else:
    z_axis = np.transpose(voltage_avg)[:-2048]





# <code to time>
end = time.time()