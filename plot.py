import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

custom_jet = ['rgb(255,255,255)','rgb(0,0,131)', 'rgb(0,60,170)', 'rgb(5,255,255)', 'rgb(255,255,0)', 'rgb(250,0,0)', 'rgb(128,0,0)']

    
def plot_signal(signal_set, time_data, channel_info, use_log=False, limits = {'z_max': 20, 'z_min': -10, 'h_max': 15,}, site = 'N/D', auto_scale = True):
    if use_log is True:
        z = np.log10(np.transpose(signal_set.values))
        zmax = 1
        zmin = -0.5
    else:
        z = np.transpose(signal_set.values)
        zmax = limits['z_max']
        zmin = limits['z_min']
        if auto_scale is True:
            # Override zmax and zmin with the actual min and max of the data
            zmax = np.average(z) * 2
            zmin = np.average(z) *(-1.3)

    
    
    fig = make_subplots(
        rows=1,
        cols=2,
        shared_yaxes=True,
        horizontal_spacing=0.05,
        column_widths=[0.75, 0.25],
        specs=[[{"type": "heatmap"}, {"type": "scatter"}]]
    )


    # Create the heatmap
    fig.add_trace(go.Heatmap(
        z=z,  # Transpose to align bins (y) and time (x)
        y=signal_set['height'].values,  
        x=time_data,
        #x=np.datetime_as_string(data_slice.coords['time'].values, unit='m'),  # Time on the x-axis
        colorbar=dict(title="UA"),  
        zmax = zmax,
        zmin = zmin,
        colorscale=custom_jet,
        connectgaps = False
    ), 
        row=1, col=1
    )  
    
    fig.add_trace(
        go.Scatter(
            x=np.log(z[:, -1]) ,
            y=signal_set['height'].values,
            mode='lines',
            name='Último perfil',
            line=dict(width=2)
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title="Señal Lidar Corregida en Rango: " + str(channel_info['detected_wavelength']) + " nm, Sitio: " + site + " (Hora UTC)",
        xaxis_title='Tiempo',
        yaxis_title='Altura (Km)',
        xaxis=dict(type="category", tickmode="linear", dtick = 72 ), 
        yaxis=dict(autorange=False, range=[0,limits['h_max']]),
        xaxis2_title = 'UA',
        plot_bgcolor='white'
        
    )
    
    fig.add_annotation(
        text="Último Perfil: " + str(time_data[-1]) + " (UTC)",  
        xref="paper", yref="paper",
        x=0.91, y=1.05,  
        showarrow=False,
        font=dict(size=14)
    )

    #show the plot
    fig.show()

    #export plot
    #fig.write_html('LiDAR_' + site +'_' + str(channel_info['detected_wavelength']) + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '.html', include_plotlyjs='cdn', full_html=False)
    fig.write_html('lidar.html', include_plotlyjs='cdn', full_html=False)