
import dash_leaflet as dl
from dash import dcc, html, Input, Output, State
import dash
app = dash.Dash(__name__)

app.layout = html.Div([
    dl.Map(center=[80.0522, -118.2437], zoom=10, children=[
        dl.TileLayer(),  # Base map layer
        dl.Marker(position=[34.0522, -118.2437], children=dl.Tooltip("Los Angeles"))
    ], style={'width': '100%', 'height': '500px'})
])

if __name__ == "__main__":
    app.run_server(debug=True)

"""
import dash
from dash import dcc, html, Input, Output, State
import dash_leaflet as dl
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__)

# Initial layout with hidden form and coordinates display
app.layout = html.Div([
    dl.Map(center=[34.0522, -118.2437], zoom=8, children=[
        dl.TileLayer(),
        dl.LayerGroup(id="marker-layer")
    ], style={'width': '100%', 'height': '50vh'}, id="map", click_lat_lng="map-click"),
    
    html.Div(id="form-container", children=[
        html.H4("Log Your Trip Details"),
        html.Div(id="click-coords"),
        html.Label("Time:"),
        dcc.Input(id="time-input", type="text", placeholder="Time"),
        html.Label("Weather:"),
        dcc.Input(id="weather-input", type="text", placeholder="Weather"),
        html.Label("Lure:"),
        dcc.Input(id="lure-input", type="text", placeholder="Lure"),
        html.Button("Submit", id="submit-btn", n_clicks=0),
    ], style={'padding': '10px', 'display': 'none'})  # Initially hidden
])

# Save data function
def save_to_csv(data, filename='trip_data.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, mode='a', index=False, header=False)

# Callback to display form and show coordinates upon clicking on the map
@app.callback(
    [Output("form-container", "style"),
     Output("click-coords", "children")],
    Input("map", "click_lat_lng")
)
def display_form(lat_lng):
    if lat_lng:
        lat, lng = lat_lng
        coords_text = f"Coordinates: Latitude {lat}, Longitude {lng}"
        form_style = {'padding': '10px', 'display': 'block'}  # Show form
        return form_style, coords_text
    else:
        return {'display': 'none'}, ""  # Hide form if no click

# Callback to add a marker and save data when the form is submitted
@app.callback(
    Output("marker-layer", "children"),
    [Input("submit-btn", "n_clicks")],
    [State("time-input", "value"),
     State("weather-input", "value"),
     State("lure-input", "value"),
     State("click-coords", "children"),
     State("marker-layer", "children")]
)
def add_marker(n_clicks, time, weather, lure, coords_text, markers):
    if n_clicks > 0 and coords_text:
        # Extract coordinates from the text
        lat, lng = [float(coord.split()[-1]) for coord in coords_text.split(',')]
        
        # Create a new marker
        marker = dl.Marker(position=[lat, lng], children=[
            dl.Tooltip(f"Time: {time}, Weather: {weather}, Lure: {lure}")
        ])
        
        # Save data to CSV
        data = [{"Latitude": lat, "Longitude": lng, "Time": time, "Weather": weather, "Lure": lure}]
        save_to_csv(data)
        
        return markers + [marker]  # Add marker to the layer

    return markers

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

"""

