
import plotly.graph_objects as go
import numpy as np

custom_jet = ['rgb(255,255,255)','rgb(0,0,131)', 'rgb(0,60,170)', 'rgb(5,255,255)', 'rgb(255,255,0)', 'rgb(250,0,0)', 'rgb(128,0,0)']
    
def plot_signal(volt_data, height_data, time_data, channel_name, use_log=False, limits = {'z_max': 20, 'z_min': -10, 'h_max': 15,}):
    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=np.transpose(volt_data),  # Transpose to align bins (y) and time (x)
        y=height_data[:-2048],  
        x=time_data,
        #x=np.datetime_as_string(data_slice.coords['time'].values, unit='m'),  # Time on the x-axis
        colorbar=dict(title="Bin Value"),  # Add a color bar with a title
        zmax = limits['z_max'],
        zmin = limits['z_min'],
        colorscale=custom_jet,
        connectgaps = False
    ))  
    
    # Log scale en Y 
    # Corregiar el BIAS
    # Vemos si el promedio movil es necesario 
    
    # Añadir suavizado configurable 
    # Update layout
    fig.update_layout(
        title=f"Señal Lidar {channel_name}",
        xaxis_title='Tiempo',
        yaxis_title='Altura (Km)',
        xaxis=dict(type="category", tickmode="linear", dtick = 72 ),  # Adjust time format if needed
        yaxis=dict(autorange=False, range=[0,limits['h_max']]),
        
    )
    
    # Show the plot
    fig.show()
    fig.write_html("fig.html")