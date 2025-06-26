import numpy as np
import sys
import xarray as xr
import time
from datetime import datetime as dt, timedelta as tdelta
from yml_load import lidarConfig
import lidardsp
from plot import plot_signal
start = time.time()

import warnings
warnings.filterwarnings('ignore')

lc = lidarConfig(config_folder="./config")


signal, first_sample_channel_info = lidardsp.read_folder(directory=lc.src, date_interval=lc.get_dateinterval(), file_prefix=lc.location_prefix)


#slice the data for the selected channel
channel_name = lc.channel
signal = signal.sel(channel=channel_name)  # Slice by channel
signal = signal.sortby('time')


##---------------FILTERING ------------------##
#signal = lidardsp.time_avg(signal, time=tdelta(minutes=lc.time_avg))
channel_info = first_sample_channel_info.loc[channel_name]
##---------------APPLY L0-------------------##
signal = lidardsp.offset_correction(signal, lc.zb)
signal = signal.assign_coords(height = ('bins', lidardsp.binnum2height(signal.coords['bins'].values, channel_info, use_Km=True)))
signal.values = lidardsp.binval2volt(signal, channel_info)
signal.values = lidardsp.bias_correction(signal,  bias_window = lc.bias_window)
signal.values = lidardsp.volts_height_correction(signal, channel_info)
signal.values = lidardsp.bw_filter(signal)
##---------------END OF L0-------------------##
#signal.values = lidardsp.spatial_moving_average(signal, n=lc.local_config['mv_avg_window'])
#signal = lidardsp.spatial_avg(signal, n=lc.spatial_avg_h)
##---------------FILTERING ------------------##



timestamp = [np.datetime64(dt).astype('datetime64[s]').astype(object).strftime('%Y-%m-%d %H:%M') for dt in signal.coords['time'].values]

# use height as main dim coord
signal = signal.swap_dims({"bins": "height"})
# slice for max height
signal = signal.sel(height=slice(0, lc.plot_limits['h_max']))

plot_signal(signal_set = signal, time_data=timestamp, channel_info=channel_info, limits=lc.plot_limits, use_log=lc.use_log, site=lc.site, auto_scale=lc.auto_scale)
print(time.time()-start)
# NOTA: Autoescala funciona bien con 1/3 para arriba y para abajo de la media.
# <code to time>
end = time.time()