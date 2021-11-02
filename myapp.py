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
import pandas as pd

app = dash.Dash(__name__)#,
                # suppress_callback_exceptions=True)

### Real df (Saved to disk right now) ###
sf = pd.read_csv('shots_fixed.csv')
# sf = pd.read_csv('https://raw.githubusercontent.com/sealneaward/nba-movement-data/master/data/shots/shots_fixed.csv')

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
    
fig = px.scatter(sf,
                 x="LOC_X", 
                 y="LOC_Y",
                 color="SHOT_MADE_FLAG",
                 hover_name="PLAYER_NAME")



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
                    style={
                        'width':'30%',
                        'display':'inline-block'
                    },
                    children= [
                        html.Label('Select Team:',
                            style={
                                'textAlign': 'left',
                                'font-size': 24,
                                'margin-top': 20,
                            }
                        ),

                        dcc.Dropdown(
                            id='team-dropdown-id',
                            options=[
                                {'label': 'Atlanta Hawks', 'value': 'Atlanta Hawks'},
                                {'label': 'Boston Celtics', 'value': 'Boston Celtics'},
                                {'label': 'Brooklyn Nets', 'value': 'Brooklyn Nets'},
                                {'label': 'Charlotte Hornets', 'value': 'Charlotte Hornets'},
                                {'label': 'Chicago Bulls', 'value': 'Chicago Bulls'},
                                {'label': 'Cleveland Cavaliers', 'value': 'Cleveland Cavaliers'},
                                {'label': 'Dallas Mavericks', 'value': 'Dallas Mavericks'},
                                {'label': 'Denver Nuggets', 'value': 'Denver Nuggets'},
                                {'label': 'Detroit Pistons', 'value': 'Detroit Pistons'},
                                {'label': 'Golden State Warriors', 'value': 'Golden State Warriors'},
                                {'label': 'Houston Rockets', 'value': 'Houston Rockets'},
                                {'label': 'Indiana Pacers', 'value': 'Indiana Pacers'},
                                {'label': 'Los Angeles Clippers', 'value': 'LA Clippers'},
                                {'label': 'Los Angeles Lakers', 'value': 'Los Angeles Lakers'},
                                {'label': 'Memphis Grizzlies', 'value': 'Memphis Grizzlies'},
                                {'label': 'Miami Heat', 'value': 'Miami Heat'},
                                {'label': 'Milwaukee Bucks', 'value': 'Milwaukee Bucks'},
                                {'label': 'Minnesota Timberwolves', 'value': 'Minnesota Timberwolves'},
                                {'label': 'New Orleans Pelicans', 'value': 'New Orleans Pelicans'},
                                {'label': 'New York Knicks', 'value': 'New York Knicks'},
                                {'label': 'Oklahoma City Thunder', 'value': 'Oklahoma City Thunder'},
                                {'label': 'Orlando Magic', 'value': 'Orlando Magic'},
                                {'label': 'Philadelphia 76ers', 'value': 'Philadelphia 76ers'},
                                {'label': 'Phoenix Suns', 'value': 'Phoenix Suns'},
                                {'label': 'Portland Trail Blazers', 'value': 'Portland Trail Blazers'},
                                {'label': 'Sacramento Kings', 'value': 'Sacramento Kings'},
                                {'label': 'San Antonio Spurs', 'value': 'San Antonio Spurs'},
                                {'label': 'Toronto Raptors', 'value': 'Toronto Raptors'},
                                {'label': 'Utah Jazz', 'value': 'Utah Jazz'},
                                {'label': 'Washington Wizards', 'value': 'Washington Wizards'}
                            ],
                            value=['Chicago Bulls',
                                    'Detroit Pistons',
                            ],
                            multi=True,
                            searchable=True,
                            search_value='',
                            placeholder='Select Teams:',
                            clearable=True,
                            className='team-select-box',
                        ),

                        html.Label('Select Period:',
                            style={
                                'textAlign': 'left',
                                'font-size': 24,
                                'margin': 'auto'
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
                                'marginTop':500,
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
                                'height':800,
                                'width':900,
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
@app.callback(
    Output('team-output-container', 'children'),
    [Input('period-slider', 'value')]
)
def update_output(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    Output('shot-graph', 'figure'),
    [Input('team-dropdown-id', 'value'),
     Input('period-slider', 'value')]
)
def build_graph(team_list, period):
    df = pd.DataFrame()
    for i in team_list:
        temp_df = sf[sf['TEAM_NAME'] == i]
        df = df.append(temp_df)
    if (period != 5):
        df = df[df['PERIOD'] == period]
    fig = px.scatter(df,
                    x='LOC_X',
                    y='LOC_Y',
                    color="SHOT_MADE_FLAG",
                    hover_name='PLAYER_NAME')
    fig.update_layout(
        plot_bgcolor = bball_colors['content_background'],
        paper_bgcolor = bball_colors['content_background'],
        font_color = bball_colors['text']
    )
    return fig

# Run's program with "hot-reloading" (i.e. when changes are made, app restarts)
if __name__ == '__main__':
    app.run_server(debug=True)
