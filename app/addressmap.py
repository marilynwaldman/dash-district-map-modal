import plotly.express as px
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import plotly.graph_objects as go
from content_style import CONTENT_STYLE
from sidebar_style import SIDEBAR_STYLE


def make_map(lat,lon,address):
    print(type(lat))
    d = {"latitude" : lat,
         "longitude" : lon,
        "address" : address
        }
    df = pd.DataFrame().append(d, ignore_index=True)        
    
    print("df")
    print(df)
    fig = go.Figure()

    fig = px.scatter_mapbox(
        df,  # Our DataFrame
        lat = "latitude",
        lon = "longitude",
        center = {"lat": lat , "lon": lon}, # where map will be centered
        width = 500,  # Width of map
        height = 500,  # Height of map
        zoom = 10,
        hover_data = ["address"],  # what to display when hovering mouse over coordinate
    )

    fig.update_layout(mapbox_style="open-street-map") # adding beautiful street layout to map
    fig.update_layout(margin={"r":0,"t":0,"l":50,"b":0}),
    fig.update_traces(marker={'size': 20})
    return fig

def popover(lat, lon, address):
    fig = make_map(lat, lon, address)
    popover = html.Div(
    [
        dbc.Button(
            "Verify Address",
            id="component-target",
            n_clicks=0,
        ),
        dbc.Popover(
            [
        
                html.Div([html.H1('Street Map')], style={'textAlign': 'center'}),
                dcc.Graph(figure=fig),
                
            ],
            target="component-target",
            trigger="click",
        ),
        
    ],style=CONTENT_STYLE
    )
    return popover