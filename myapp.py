# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
# from dash import dcc
# from dash import html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from PIL import Image

app = dash.Dash(__name__)#,
                # suppress_callback_exceptions=True)

### Real df (Saved to disk right now) ###
# sf = pd.read_csv('shots_fixed.csv')
sf = pd.read_csv('https://raw.githubusercontent.com/sealneaward/nba-movement-data/master/data/shots/shots_fixed.csv')



# build team dictionary
unique_teams = sorted(sf['TEAM_NAME'].unique())
team_dict = [{'label': i, 'value': i} for i in unique_teams]


### Create Graph ##



# Color Configurations
bball_colors = {
    'page_background' : '#23262E',
    'content_background' : '#2d3038',
    'border' : '#53555B',
    'text' : '#95969A',
    'accent' : '#FA4F56',
    'background': '#3E464F',
}

def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Basketball SportVU Visualization"),
                    html.H6("Shooting and Movement"),
                ],
            )
        ]
    )

fig = go.Figure()


### APP LAYOUT PORTION ###
app.layout = html.Div(
    id='entire-app-container',
    children = [
        build_banner(),
        dcc.Tabs(
            id="custom-tabs-container",
            value="shooting-tab",
            className="custom-tabs",
            children=[
                dcc.Tab(
                    id="Shooting-tab",
                    label="Shooting",
                    value="shooting-tab",
                    className="custom-tab",
                    selected_className="custom-tab-selected",
                ),
                dcc.Tab(
                    id="Movement-tab",
                    label="Movement",
                    value="movement-tab",
                    className="custom-tab",
                    selected_className="custom-tab-selected",
                ),
            ]
        ),
        html.Div(id='tab-content'),
    ]
)


### ======= ALL CALLBACKS ====== ####

# Return the content corresponding to the tab selected:
@app.callback(Output('tab-content', 'children'),
              Input('custom-tabs-container', 'value'))
def render_content(tab):
    # shooting tabs
    if (tab == 'shooting-tab'):
        return html.Div(
            id='tab-1-content',
            style={
                'margin-left' : 52,
            },
            children=[
                # div for left part of shooting tab
                html.Div(
                    id='tab-1-left-part',
                    className = 'six columns',
                    style={
                        'width':'30%',
                        'display':'inline-block'
                    },
                    children= [
                        html.Label('Select Team:',
                            style={
                                'textAlign': 'left',
                                'fontSize': 24,
                                'marginTop': 20,
                            }
                        ),

                        dcc.Dropdown(
                            id='team-dropdown-id',
                            options=team_dict,
                            value=['Chicago Bulls','Detroit Pistons',],
                            multi=True,
                            searchable=True,
                            search_value='',
                            placeholder='Select Teams:',
                            clearable=True,
                            className='team-select-box',
                        ),

                        html.Label('Select Players:',
                            style={
                                'textAlign': 'left',
                                'fontSize': 24,
                                'marginTop': 20
                            }
                        ),

                        dcc.Dropdown(
                            id='player-selection',
                            value=['Derrick Rose','Reggie Jackson'],
                            multi=True,
                            clearable=True,
                            searchable=True,
                            search_value='',
                            placeholder='Select Players:',
                            className='player-select-box',
                        ),

                        html.Label('Select Period:',
                            style={
                                'textAlign': 'left',
                                'font-size': 24,
                                'margin': 'auto',
                                'marginTop': 20
                            }
                        ),

                        html.Div(
                            dcc.Slider(
                                id='period-slider',
                                min=1,
                                max=5,
                                value=3,
                                marks={
                                    1:{'label':'1', 'style' : {'color': bball_colors['text']}},
                                    2:{'label':'2', 'style' : {'color': bball_colors['text']}},
                                    3:{'label':'3', 'style' : {'color': bball_colors['text']}},
                                    4:{'label':'4', 'style' : {'color': bball_colors['text']}},
                                    5:{'label':'All','style': {'color': bball_colors['text']}}
                                },
                            ),
                            className='period-select-box'
                        ),

                        html.Div(
                            id='team-output-container',
                            style={
                                'textAlign':'left',
                            }
                        ),

                        html.Div('_',
                            className='gap',
                            style={
                                'marginTop':300,
                                'color': bball_colors['page_background']
                            },
                            
                        )
                    ]
                ),
                html.Div(
                    id='tab-1-right-part',
                    style={
                        'width':'60%',
                        'display':'inline-block',
                        'marginLeft': 'auto',
                    },
                    children =[
                        dcc.Graph(
                            id='shot-graph',
                            style={
                                'height':750,
                                'width':800,
                                'float': 'right'
                            },
                            figure=fig
                        ),
                    ]
                )
            ]
        )
    # movement tab:
    elif (tab == 'movement-tab'):
        return html.Div(
            html.Label('Waiting for Movement Stuff...',
                style={
                    'textAlign': 'left',
                    'font-size': 24,
                    'padding': 20,
                }
            ),
        )



# == Shooting Callbacks == #

# Simple callback demo that diplays the period selected
@app.callback(
    Output('team-output-container', 'children'),
    [Input('period-slider', 'value')]
)
def update_output(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    Output('player-selection', 'options'),
    [Input('team-dropdown-id', 'value')]
)
def update_player_list(team_list):
    df = pd.DataFrame()
    for i in team_list:
        temp_df = sf[sf['TEAM_NAME'] == i]
        df = df.append(temp_df)

    unique_players = df['PLAYER_NAME'].unique()

    return [{'label': i, 'value': i} for i in unique_players]


# create shot graph from team and period selection
@app.callback(
    Output('shot-graph', 'figure'),
    [Input('player-selection', 'value'),
     Input('period-slider', 'value')]
)
def build_graph(team_list, period):
    df = pd.DataFrame()
    for i in team_list:
        temp_df = sf[sf['PLAYER_NAME'] == i]
        df = df.append(temp_df)
    if (period != 5):
        df = df[df['PERIOD'] == period]

    # make figure
    fig = go.Figure(data=go.Scatter(
                        x=df['LOC_X'],
                        y=df['LOC_Y'],
                        mode='markers',
                        hovertext=df['PLAYER_NAME']
                    )
     )

    fig.update_xaxes(range=[-300,300],showgrid=False, zeroline=False)
    fig.update_yaxes(range=[-100,500],showgrid=False, zeroline=False)

    fig.update_layout(
        plot_bgcolor = bball_colors['content_background'],
        paper_bgcolor = bball_colors['content_background'],
        font_color = bball_colors['text']
    )

    # Incorporate Image
    # img = Image.open('Basketball_Halfcourt3.png')

    fig.add_layout_image(
        dict(
            # source=img,
            source='https://raw.githubusercontent.com/matthewmechtly/CS519_Vis_Ballers/main/Basketball_Halfcourt3.png',
            xref="x",
            yref="y",
            x=-250,
            y=422.5,
            sizex=500,
            sizey=470,
            sizing="stretch",
            opacity=1.0,
            layer="below")
    )


    return fig

# Run's program with "hot-reloading" (i.e. when changes are made, app restarts)
if __name__ == '__main__':
    app.run_server(debug=True)
