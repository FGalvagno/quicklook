import numpy as np
import sys
import xarray as xr
import time
from datetime import datetime as dt, timedelta as tdelta
from yml_load import lidarConfig
import lidardsp
from plot import plot_signal
start = time.time()

#TODO: Lista de cambios
# - Agregar último perfil: vertical  altura con altura. Del lado derecho de la pantalla
# - Agregar suma de la señal depolarizada
# - Unidad que va color
# - Fecha y hora y si es UTC
# - Señal lidar corregida en rango de titulo
# - Autoescala



import warnings
warnings.filterwarnings('ignore')

lc = lidarConfig(config_folder="./config")


signal, first_sample_channel_info = lidardsp.read_folder(directory=lc.src, date_interval=lc.get_dateinterval(), file_prefix=lc.location_prefix)


#slice the data for the selected channel
channel_name = lc.channel
signal = signal.sel(channel=channel_name)  # Slice by channel
signal = signal.sortby('time')


import read_licel as rl

dark_current = rl.dtfs("./dark_current", optimize_reading=True)[3]
dark_current = dark_current.sel(channel=channel_name)
    
# Ensure dark_current has the same shape as signal along 'time'
#if dark_current.sizes['time'] == 1 and signal.sizes['time'] > 1:
#    dark_current = dark_current.isel(time=0)
#    # Expand dark_current along 'time' to match signal
#    dark_current = dark_current.expand_dims(time=signal['time'])
#    dark_current['time'] = signal['time']

#signal = dark_current
import matplotlib.pyplot as plt
#da = signal
#da = dark_current

#signal = dark_current
channel_info = first_sample_channel_info.loc[channel_name]
signal = lidardsp.offset_correction(signal, lc.zb)
signal = signal.assign_coords(height = ('bins', lidardsp.binnum2height(signal.coords['bins'].values, channel_info, use_Km=True)))
signal.values = lidardsp.binval2volt(signal, channel_info)
signal.values = lidardsp.bias_correction(signal,  bias_window = lc.bias_window)
signal.values = lidardsp.volts_height_correction(signal, channel_info)

da = signal

from scipy.signal import butter, filtfilt
import numpy as np
import matplotlib.pyplot as plt

# Extract 1D signal
signal = signal.values[0]  # If it's a DataArray
#signal = signal.values  # If it's a DataArray

n_bins = signal.shape[0]
bin_spacing = 7.5  # meters between bins
heights = np.arange(n_bins) * bin_spacing  # height axis

# Butterworth low-pass filter
f0 = 0.009  # cutoff freq (cycles/meter)
fs = 1 / bin_spacing  # spatial sampling frequency (samples per meter)
nyq = fs / 2
Wn = f0 / nyq
b, a = butter(N=8, Wn=Wn, btype='low')


# Gaussian low-pass filter
from scipy.ndimage import gaussian_filter1d
sigma = 5  # standard deviation for Gaussian filter
signal_filtered = gaussian_filter1d(signal, sigma=sigma, axis=0)


# Apply zero-phase filtering
#signal_filtered = filtfilt(b, a, signal, axis =1 )
signal_filtered = filtfilt(b, a, signal, axis=0)
# FFT of original signal
fft_vals = np.fft.fft(signal)
freqs = np.fft.fftfreq(n_bins, d=bin_spacing)
power = np.abs(fft_vals)**2

# Plot
half_n = n_bins // 2
freqs_half = freqs[:half_n]
power_half = power[:half_n]

fig, axs = plt.subplots(2, 1, figsize=(10, 8), constrained_layout=True)

# Top: original and filtered signal
axs[0].plot(heights, signal, label="Original", alpha=0.6)
axs[0].plot(heights, signal_filtered, label="Filtered (Butterworth)", linewidth=2)
axs[0].set_title("Signal Before and After Low-Pass Filter")
axs[0].set_xlabel("Height (m)")
axs[0].set_ylabel("Amplitude")
axs[0].legend()
axs[0].grid(True)

# Bottom: power spectrum with cutoff marked
axs[1].plot(freqs_half, power_half, label="Original Spectrum")
axs[1].axvline(f0, color='red', linestyle='--', label=f"Cutoff f0 = {f0}")
axs[1].set_title("Spatial Power Spectrum")
axs[1].set_xlabel("Spatial Frequency (cycles/meter)")
axs[1].set_ylabel("Log Power")
axs[1].legend()
axs[1].grid(True)
#axs[1].set_xlim(0, 0.2)  # Adjust x-axis limit for better visibility

filtered_fft = np.fft.fft(signal_filtered)
filtered_power = np.log(np.abs(filtered_fft)**2)
axs[1].plot(freqs_half, filtered_power[:half_n], label="Filtered Spectrum", linestyle='--')
plt.show()

da.values = signal_filtered
signal = da

##---------------FILTERING ------------------##
#signal = lidardsp.time_avg(signal, time=tdelta(minutes=lc.time_avg))
channel_info = first_sample_channel_info.loc[channel_name]
##---------------APPLY L0-------------------##
#signal = lidardsp.offset_correction(signal, lc.zb)
#signal = signal.assign_coords(height = ('bins', lidardsp.binnum2height(signal.coords['bins'].values, channel_info, use_Km=True)))
#signal.values = lidardsp.binval2volt(signal, channel_info)
#signal.values = lidardsp.bias_correction(signal,  bias_window = lc.bias_window)
#signal.values = lidardsp.volts_height_correction(signal, channel_info)
##---------------END OF L0-------------------##
#signal.values = lidardsp.spatial_moving_average(signal, n=lc.local_config['mv_avg_window'])
#signal = lidardsp.spatial_avg(signal, n=lc.spatial_avg_h)
##---------------FILTERING ------------------##



timestamp = [np.datetime64(dt).astype('datetime64[s]').astype(object).strftime('%Y-%m-%d %H:%M') for dt in signal.coords['time'].values]

# use height as main dim coord
signal = signal.swap_dims({"bins": "height"})
# slice for max height
signal = signal.sel(height=slice(0, lc.plot_limits['h_max']))

plot_signal(signal_set = signal, time_data=timestamp, channel_info=channel_info, limits=lc.plot_limits, use_log=lc.use_log, site=lc.site)
print(time.time()-start)
# NOTA: Autoescala funciona bien con 1/3 para arriba y para abajo de la media.
# <code to time>
end = time.time()