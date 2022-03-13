#  registration div
#import dash
import dash_bootstrap_components as dbc
from dash import html

def registration_div():

    registration = html.Div(
            dbc.Container(
            [  
                html.Br(),
                html.H4("Colorado Voter Information"),
                html.Br(),
                html.P(
                    "Look up your official Colorado Voter Registration here "
                    "to see what district and precinct you are in.",
                    className="lead",
                ),
                html.Br(),
                html.A(
                   "Check your Colorado Voter Registration here.", href='https://www.sos.state.co.us/voter/pages/pub/olvr/findVoterReg.xhtml', target="_blank"
                ),
                html.Br(),
                html.Hr(className="my-2"),
                html.Br(),
                html.P(

                    "Please note that the voter lookup is very particular."
                    "  You MUST enter the requested information exactly"
                    "like your voter registration "
                    "(i.e. 'Sam A. Smith' will return an error if you registered as 'Sam Adam Smith.')"
        
                ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br()

           ],
           fluid=False,
           className="py-3",
        ),
        className="p-2 bg-light rounded-3",
    )

    return registration