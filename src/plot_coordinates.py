# Railways and Transport Laboratory, National Technical University of Athens
# Charging Stations Location Problem for Electric Buses (EB-CSLP)
# Module to print coordinates based on data input and model results

import plotly.graph_objs as go

def plot_coordinates_on_map(tcK, tyK, tcV, tyV, mapbox_access_token):
    go.Figure(data=[
        go.Scattermapbox(
            lat=list(tcK.values()),
            lon=list(tyK.values()),
            mode='markers+text',                # Display markers and optionally text
            marker=dict(size=25, color='coral'),
            text=[f"Bus line #{key}" for key in tcK.keys()],                                 # Label text next to the marker
            hovertext=[f"Coordinates: {lat}, {lon}" for lat, lon in zip(tcK.values(), tyK.values())],   # Text displayed on hover
            hoverinfo="text",                   # Display hovertext only
            textposition="bottom center",       # Position the text
            showlegend=False,
            textfont=dict(
                size=18,
                color='black'
            )
        ),
        go.Scattermapbox(
            lat=list(tcV.values()),
            lon=list(tyV.values()),
            mode='markers+text',            # Display markers and optionally text
            marker=dict(size=25, color='blue'),
            text=[f"Candidate Charger #{key}" for key in tcV.keys()],                                    # Label text next to the marker
            hovertext=[f"Coordinates: {lat}, {lon}" for lat, lon in zip(tcV.values(), tyV.values())],   # Text displayed on hover
            hoverinfo="text",               # Display hovertext only
            textposition="bottom center",   # Position the text
            showlegend=False,
            textfont=dict(
                size=18,
                color='blue'
            )
        )
    ],
    layout=go.Layout(
        title="Charging Stations Facility Location Problem for Electric Busses in Athens, Greece",
        mapbox=dict(
            accesstoken=mapbox_access_token,
            center=dict(lat=37.9751127, lon=23.7276736),
            style="open-street-map",
            zoom=11,
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )).show()
