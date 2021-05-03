import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd

# data source 1 - datafiles/iranian_students.csv
# Iranian Students from 1968 to 2017 | Owner: Chubak Bidpaa
# https://www.kaggle.com/chubak/iranian-students-from-1968-to-2017
# preprocessing notes: iranian calendar format converted to english and first three years with incomplete rows removed

df_iran = pd.read_csv("datafiles/iranian_students.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# sidebar styling
""" SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "4rem 1rem",
    "background-color": "#712177", # old - #712177
    "transition": "all .5s",
    #"z-index": "-1"
}

SIDEBAR_COLLAPSED = {
    "position": "fixed",
    "top": 0,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#712177",
    "transition": "all .5s",
    #"z-index": "-1"
}

CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "left": "18rem",
    "padding": "1rem 1rem",
    "background-color": "#86428b", # old - #86428b
    "border-radius": "1rem",
    "z-index": "-2"
}
CONTENT_STYLE_COLLAPSED = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
    "background-color": "#86428b",
    "border-radius": "1rem",
    "z-index": "-2"
}"""

CONTENT_STYLE_COLLAPSED = {
    "transition": "margin-left 0.5s",
    "padding": "1rem",
    "margin-left": 0,
    "border-radius": "1rem",
}

CONTENT_STYLE = {
    "transition": "margin-left 0.5s",
    "padding": "1rem",
    "margin-left": "16rem",
    "border-radius": "1rem",
}

BUTTON_STYLE = {
    "padding": "1rem 1rem",
    "transition": "margin-left .5s",
    "margin-left": "16rem",
}

BUTTON_STYLE_COLLAPSED = {
    "padding": "1rem 1rem",
    "transition": "margin-left .5s",
    "margin-left": 0,
}

SIDEBAR_STYLE = {
    "height": "100%",
    "width": "16rem",
    "position": "fixed",
    "z-index": "1",
    "padding": "4rem 1rem",
    "top": 0,
    "left": 0,
    "background-color":   "#111",
    "overflow-x": "hidden",
    "transition": "0.5s",
    "padding-top": "4rem",
}

SIDEBAR_STYLE_COLLAPSED = {
    "height": "100%",
    "width": "0rem",
    "position": "fixed",
    "z-index": "1",
    "top": 0,
    "left": 0,
    "background-color":  "#111",
    "overflow-x": "hidden",
    "transition": "0.5s",
    "padding-top": "4rem",
}


sidebar = html.Div(
    [
        html.H2("Moodle Analytics", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE

)

button = html.Div(
    [
        dbc.Button("☰", outline=True, id="show_hide", color="light")
    ],
    id="button",
    style=BUTTON_STYLE
) 


content = html.Div(
    id="page-content",
    style=CONTENT_STYLE
)

app.layout = html.Div([
    dcc.Store(id='side_click'),
    dcc.Location(id="url"),
    sidebar,
    button,
    content
])


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
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, button_style, cur_nclick


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
            html.H1('Kindergarten in Iran',
                    style={'textAlign': 'center'}),
            dcc.Graph(id='bargraph',
                      figure=px.bar(df_iran, barmode='group', x='Years',
                                    y=['Girls Kindergarten', 'Boys Kindergarten']))
        ]
    elif pathname == "/page-1":
        return [
            html.H1('Grad School in Iran',
                    style={'textAlign': 'center'}),
            dcc.Graph(id='bargraph',
                      figure=px.bar(df_iran, barmode='group', x='Years',
                                    y=['Girls Grade School', 'Boys Grade School']))
        ]
    elif pathname == "/page-2":
        return [
            html.H1('High School in Iran',
                    style={'textAlign': 'center'}),
            dcc.Graph(id='bargraph',
                      figure=px.bar(df_iran, barmode='group', x='Years',
                                    y=['Girls High School', 'Boys High School']))
        ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Page not found"),
            html.Hr(),
            html.P(
                f"The page with URL ending '{pathname}' was not found. Please try another page."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
