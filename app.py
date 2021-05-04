# importing libraries and dependencies
import os
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State


# data source 1 - datafiles/iranian_students.csv
# Iranian Students from 1968 to 2017 | Owner: Chubak Bidpaa
# https://www.kaggle.com/chubak/iranian-students-from-1968-to-2017
# preprocessing notes: iranian calendar format converted to english and first three years with incomplete rows removed

df_iran = pd.read_csv("datafiles/iranian_students.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# content styling
CONTENT_STYLE_COLLAPSED = {
    "transition": "margin-left 0.3s",
    "padding": "1rem",
    "margin-left": "1rem",
    "border-radius": "1rem",
    "background-color":  "#161a28",
    "box-shadow": "3px 3px #111",
    "margin-right": "1rem"
}

CONTENT_STYLE = {
    "transition": "margin-left 0.3s",
    "padding": "1rem",
    "margin-left": "17rem",
    "border-radius": "1rem",
    "background-color":  "#161a28",
    "box-shadow": "3px 3px #111",
    "margin-right": "1rem"
}

# button styling
BUTTON_STYLE = {
    "padding": "1rem 1rem",
    "transition": "margin-left .3s",
    "margin-left": "16rem",
}

BUTTON_STYLE_COLLAPSED = {
    "padding": "1rem 1rem",
    "transition": "margin-left .3s",
    "margin-left": 0,
}

# sidebar styling
SIDEBAR_STYLE = {
    "height": "100%",
    "width": "16rem",
    "position": "fixed",
    "z-index": "1",
    "padding": "1rem",
    "top": 0,
    "left": 0,
    "background-color":   "#161a28",
    "overflow-x": "hidden",
    "transition": "0.3s",
}

SIDEBAR_STYLE_COLLAPSED = {
    "height": "100%",
    "width": "0rem",
    "position": "fixed",
    "z-index": "1",
    "top": 0,
    "left": 0,
    "background-color":  "#161a28",
    "overflow-x": "hidden",
    "transition": "0.3s",
    "padding-top": "1rem",
}

# sidebar object
sidebar = html.Div(
    [
        html.H2("Moodle Analytics", className="display-4"),
        
        html.Hr(),
        html.P("Iranian Education Dataset"),
        dbc.Nav(
            [
                dbc.NavLink("Kindergarten", href="/", active="exact"),
                dbc.NavLink("Grade School", href="/page-1", active="exact"),
                dbc.NavLink("High School", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr()
    ],
    id="sidebar",
    style=SIDEBAR_STYLE
)

# button object
button = html.Div(
    [
        dbc.Button("☰", outline=True, id="show_hide", color="light")
    ],
    id="button",
    style=BUTTON_STYLE
)

# content object
content = html.Div(
    id="page-content",
    style=CONTENT_STYLE
)

# defining app layout
app.layout = html.Div([
    dcc.Store(id='side_click'),
    dcc.Location(id="url"),
    sidebar,
    button,
    content,
]

)

# content callback
@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("button", "style"),
        Output("side_click", "data")
    ],

    [Input("show_hide", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
# function to toggle sidebar on click
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_STYLE_COLLAPSED
            content_style = CONTENT_STYLE_COLLAPSED
            button_style = BUTTON_STYLE_COLLAPSED
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            button_style = BUTTON_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        button_style = BUTTON_STYLE
        cur_nclick = "SHOW"

    return sidebar_style, content_style, button_style, cur_nclick

# page content callback
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
# render page
def render_page_content(pathname):
    if pathname == "/":
        return [
            html.H1('Kindergarten in Iran',
                    style={'textAlign': 'center'}),
            dcc.Graph(id='bargraph',
                      figure=px.bar(df_iran, barmode='group', x='Years',
                                    y=['Girls Kindergarten', 'Boys Kindergarten']
                                    )),
        ]
    elif pathname == "/page-1":
        return [
            html.H1('Grad School in Iran',
                    style={'textAlign': 'center'}),
            dcc.Graph(id='bargraph',
                      figure=px.bar(df_iran, barmode='group', x='Years',
                                    y=['Girls Grade School', 'Boys Grade School'],))
        ]
    elif pathname == "/page-2":
        return [
            html.H1('High School in Iran',
                    style={'textAlign': 'center'}),
            dcc.Graph(id='bargraph',
                      figure=px.bar(df_iran, barmode='group', x='Years',
                                    y=['Girls High School', 'Boys High School']))
        ]
    # if the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Page not found"),
            html.Hr(),
            html.P(
                f"The page with URL ending '{pathname}' was not found. Please try another page."),
        ]
    )


# run
server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)
