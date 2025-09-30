import dash
from dash import dcc, html
import dash_player as dp

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Home page'),
    html.Summary("View the interactive data map and timeseries heart disease related data by Scottish NHS board region"),
    html.Div(
                    style={"width": "48%", "padding": "0px"},
                    children=[
                        dp.DashPlayer(
                            id="player",
                            url="https://github.com/healthbiodatascientist/heart_health/raw/refs/heads/main/heart_prev_mapped_video.mp4",
                            controls=True,
                            width="100%",
                            height="250px",
                        )]
   )
])
