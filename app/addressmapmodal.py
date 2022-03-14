import plotly.express as px
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import plotly.graph_objects as go
from content_style import CONTENT_STYLE
from sidebar_style import SIDEBAR_STYLE


def make_map(lat,lon,address):
    d = {"latitude" : lat,
         "longitude" : lon,
        "address" : address
        }
    df = pd.DataFrame().append(d, ignore_index=True)        
    
    fig = go.Figure()

    fig = px.scatter_mapbox(
        df,  # Our DataFrame
        lat = "latitude",
        lon = "longitude",
        center = {"lat": lat , "lon": lon}, # where map will be centered
        width = 500,  # Width of map
        height = 500,  # Height of map
        zoom = 14,
        hover_data = ["address"],  # what to display when hovering mouse over coordinate
    )

    fig.update_layout(mapbox_style="open-street-map") # adding beautiful street layout to map
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}),
    fig.update_traces(marker={'size': 10})
    return fig

def popover(lat, lon, address):
    fig = make_map(lat, lon, address)
    
    modal = html.Div(
    [
        
        dbc.Button(
            "Verify Address", id="open-body-scroll", n_clicks=0
        ),
        dbc.Modal(
            [
                #dbc.ModalHeader(dbc.ModalTitle("Modal with scrollable body")),
                dbc.ModalBody(
        
                   dcc.Graph(figure=fig, id="fig"),
                   
                
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-body-scroll",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-body-scroll",
            scrollable=True,
            is_open=False,
        ),
    ]
    )
    
    return modal
    
def blank_popover():
    
    modal = html.Div(
    [
        
        html.Div(
            "", id="open-body-scroll", n_clicks=0
        ),
        dbc.Modal(
            [
                #dbc.ModalHeader(dbc.ModalTitle("Modal with scrollable body")),
                dbc.ModalBody(
        
                   
                   
                
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-body-scroll",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-body-scroll",
            scrollable=True,
            is_open=False,
        ),
    ]
    )
    
    return modal

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open




