
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
custom_jet = ['rgb(255,255,255)','rgb(0,0,131)', 'rgb(0,60,170)', 'rgb(5,255,255)', 'rgb(255,255,0)', 'rgb(250,0,0)', 'rgb(128,0,0)']
    
def plot_signal(signal_set, time_data, channel_info, use_log=False, limits = {'z_max': 20, 'z_min': -10, 'h_max': 15,}, site = 'N/D'):
    if use_log is True:
        z = np.log10(np.transpose(signal_set.values))
        zmax = 1
        zmin = -1
    else:
        z = np.transpose(signal_set.values)
        zmax = limits['z_max']
        zmin = limits['z_min']
    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z,  # Transpose to align bins (y) and time (x)
        y=signal_set['height'].values,  
        x=time_data,
        #x=np.datetime_as_string(data_slice.coords['time'].values, unit='m'),  # Time on the x-axis
        colorbar=dict(title="Bin Value"),  # Add a color bar with a title
        zmax = zmax,
        zmin = zmin,
        colorscale=custom_jet,
        connectgaps = False
    ))  
    
    # Log scale en Y 
    # Corregiar el BIAS
    # Vemos si el promedio movil es necesario 
    
    # Añadir suavizado configurable 
    # Update layout
    fig.update_layout(
        title="Señal Lidar: " + str(channel_info['detected_wavelength']) + " nm, Sitio: " + site,
        xaxis_title='Tiempo',
        yaxis_title='Altura (Km)',
        xaxis=dict(type="category", tickmode="linear", dtick = 72 ),  # Adjust time format if needed
        yaxis=dict(autorange=False, range=[0,limits['h_max']]),
        plot_bgcolor='white'
        
    )
    
    #show the plot
    fig.show()

    #export plot
    fig.write_html('LiDAR_' + site +'_' + str(channel_info['detected_wavelength']) + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '.html')