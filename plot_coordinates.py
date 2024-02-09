import plotly.graph_objs as go

def plot_coordinates_on_map(tcK, tyK, tcV, tyV, mapbox_access_token):
    # Create Scattermapbox traces for tcK and tyK with light red color
    go.Figure(data=[
        go.Scattermapbox(
            lat=list(tcK.values()),
            lon=list(tyK.values()),
            mode='markers',
            marker=dict(size=20, color='coral'),
            text=[f"Bus line {key} (tcK, tyK)" for key in tcK.keys()],
            showlegend=False
        ),
        go.Scattermapbox(
            lat=list(tcV.values()),
            lon=list(tyV.values()),
            mode='markers',
            marker=dict(size=20, color='blue'),
            text=[f"Charger {key} (tcV, tyV)" for key in tcV.keys()],
            showlegend=False
        )
    ],
    layout=go.Layout(
        title="Charging Stations Facility Location Problem for Electric Busses in Athens, Greece",
        mapbox=dict(
            accesstoken=mapbox_access_token,
            center=dict(lat=37.9751127, lon=23.7276736),  # Adjust the center based on your data
            style="mapbox://styles/mapbox/streets-v11",  # You can change the map style
            zoom=11,
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )).show()
