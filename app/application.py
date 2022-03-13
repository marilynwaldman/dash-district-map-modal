# https://stackoverflow.com/questions/62732631/how-to-collapsed-sidebar-in-dash-plotly-dash-bootstrap-components
import os
import sys
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash_bootstrap_components._components.Container import Container
from geocode import extract_lat_long_via_address, get_district
from addressmapmodal import  blank_popover
from content_style import CONTENT_STYLE, CONTENT_STYLE1
from sidebar_style import SIDEBAR_HIDEN, SIDEBAR_STYLE


#GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY'] = os.environ['GOOGLE_API_KEY']
try:  
  os.environ['GOOGLE_API_KEY']
except KeyError: 
  print('[error]: `GOOGLE_#API_KEY` environment variable required')
  sys.exit(1)

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']  

# Build list that determines app routing : /about, 'map.html etc
maps = os.listdir("./app/static")
maps = [ map for map in maps if map.endswith( '.html') ]
maps = [os.path.splitext(map)[0] for map in maps]
home_about = ['about']
maps.remove('about')
maps.sort()
maps = maps + home_about

# create a dictionary of routing labels used in sidebar
dict = {}
index =0
for map in maps:
    dict[map] = map
dict['about'] = "About"
   
dict['colorado_districtmap_1mar22'] = "District Map"

application = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN],prevent_initial_callbacks=True)


PLOTLY_LOGO = "./static/img/IX_PCarto_sm_23Feb21.png"

# Create empty modal to satisfy initial callback stuff

modal = blank_popover()

# Define navbar - search is not the sidebar toggle
sidebar_toggle = dbc.Row(
    [    dbc.Col(
            dbc.Button(
                "Sidebar",  color="primary", className="ms-2", id="btn_sidebar", size="sm"
            ),
            width="auto",
        ),  
        
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="60px")),
                        dbc.Col(dbc.NavbarBrand("Colorado Congressional Districts", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://ixwater.com/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                sidebar_toggle,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ],
        
    ),
    style={
           "background-image": "url(/assets/banner.png)",
           "background-repeat": "no-repeat",
           "background-size" : "cover",
           },
    color="dark",
    dark=True,
)



# add callback for toggling the collapse on small screens
@application.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# define address field for sidebar - input/output callback below
address = html.Div(
    [
        html.H3(
            "Enter your address:  ", className="lead"
        ),
        dbc.Input(id="input", placeholder="ex: 17301 W Colfax Golden", size="md", className="mb-3", type="text",debounce=True),

        html.P(id="output"),
        
    ],
    
)

#define sidebar 
sidebar = html.Div(
    [
         
        html.Br(),
        html.H5("Colorado Congressional Districts"),
        html.Br(),      
        address,
        modal,
        dbc.Nav(
            [  
                dbc.NavLink(str(dict[map]), href="/" + str(map), id="page-" + str(map) + "-link") for map in maps
            
            ],
            vertical=True,
            pills=True,
        ),         
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

# define content section - empty list filled with map below
content = html.Div(

    [
    ],
    id="page-content",
    style=CONTENT_STYLE)


#define application layout
application.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
    style={ "background-color": "#f2f1ed"}
)

#  callbacks 
    

# callback for address
# api call to Google to get lat/lon from address input
# returns a modal with mapbox map for verification
# will extent to determine district and county
@application.callback(Output("output", "children"), [Input("input", "value")])
def output_text(value):

    global modal
    
    lat, lon, modal = extract_lat_long_via_address(value, GOOGLE_API_KEY)
    
    #districts = extract_lat_long_via_address(value, GOOGLE_API_KEY)
    
    return lat, lon, modal

#callback for sidebar button
@application.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

# app routing callbacks below:    

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on

@application.callback(

    [Output("page-" + str(map) + "-link", "active") for map in maps],
    [Input("url", "pathname")],
)   

def toggle_active_links(pathname):
    if pathname == ["/"]:
        # Treat page 1 as the homepage / index
        #return True, False, False, False
        #list = [False for i in len(maps)]
        #list[0] = True
        return [True] + [False for i in range(len(maps)-1)]
    return [pathname == "/" + str(map) for map in maps]


@application.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/"]:
        #return html.P("IX Power Maps")
        mymap = "./app/static/colorado_districtmap_1mar22.html"
        return html.Div(
              html.Iframe(id="map", srcDoc= open(mymap,'r').read(), width='100%', height='600' )
        )
    elif pathname in ["/" + str(map) for map in maps]:


        mymap = "./app/static/" + pathname[1:] + ".html"
        return html.Div(
              html.Iframe(id="map", srcDoc= open(mymap,'r').read(), width='100%', height='600' )
        )
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P("The pathname {pathname} was not recognised..."),
        ]
    )
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


#callbacks for modal - scroll 

application.callback(
    
    Output("modal-body-scroll", "is_open"),
    
    [
        Input("open-body-scroll", "n_clicks"),
        Input("close-body-scroll", "n_clicks"),
    ],
    [State("modal-body-scroll", "is_open")],
)(toggle_modal)

if __name__ == "__main__":
      
    #print(f"file_name: {file&#91;'Key']}, size: {file&#91;'Size']}")
    application.run_server(debug=True,port=8050,host='0.0.0.0')
