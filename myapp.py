# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
# from dash import dcc
# from dash import html
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

### Toy dataset and Graph for Demo Purposes ###
# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

### Real df (Saved to disk right now) ###
# sf = pd.read_csv('shots_fixed.csv')
sf = pd.read_csv('https://raw.githubusercontent.com/sealneaward/nba-movement-data/master/data/shots/shots_fixed.csv')

### Data Manipulation for Display ###


### Create Graph ##
fig = px.scatter(sf,
                 x="LOC_X", 
                 y="LOC_Y",
                 color="SHOT_MADE_FLAG",
                 hover_name="PLAYER_NAME")


### CONFIGURATION INPUTS ###
colors = {
    'background': '#3E464F',
    'text': '#77b0b1'
}


### APP LAYOUT FORMATTING ###
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


### APP LAYOUT PORTION ###
app.layout = html.Div(
    style={'backgroundColor': colors['background'],
           'padding':10, 
           'display': 1,
           'flex-direction': 'row',
           'color':'#77b0b1',
           'margin':'auto',
           'width': "75%"
    }, 
    children = [

        html.H1(
            children='BLAH Dash',
            style={
                'textAlign': 'center',
                # 'color':colors['text']
            }
        ),

        html.Label('Select Team:',
            style={
                'textAlign': 'left',
                'font-size': 24,
                'padding': 20}
        ),

        dcc.Dropdown(
            id='team_dropdown_id',
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
                    # 'Detroit Pistons',
                    # 'New York Knicks',
                    # 'Boston Celtics'
            ],
            multi=True,
            searchable=True,
            search_value='',
            placeholder='Select Teams:',
            clearable=True,
            className='team_select_box_css',
        ),

        html.Label('Select Period:',
            style={
                'textAlign': 'left',
                'font-size': 24,
                'padding': 20
            }
        ),

        html.Div(
            dcc.Slider(
                id='period_slider',
                min=1,
                max=5,
                value=3,
                marks={
                    1:{'label':'1', 'style': {'color': '#77b0b1'}},
                    2:{'label':'2', 'style': {'color': '#77b0b1'}},
                    3:{'label':'3', 'style': {'color': '#77b0b1'}},
                    4:{'label':'4', 'style': {'color': '#77b0b1'}},
                    5:{'label':'All', 'style': {'color': '#77b0b1'}}
                },
            ),
            className='period_select_box_css'
        ),

        html.Div(
            id='slider-output-container',
            style={
                'textAlign':'left',
            }
        ),

        html.Div(
            'Dash: A web application framework for your data.,',
            style={
                'textAlign':'right',
            }
        ),

        dcc.Graph(
            id='shot_graph',
            style={
                'height':500,
                'width':900
            },
            figure=fig
        ),


        html.Div(
            id='team-output-container',
            style={
                'textAlign':'left',
            }
        ),

    ]
    # className='three columns',
)

### Callbacks ###
@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('period_slider', 'value')]
)
def update_output(value):
    return 'You have selected "{}"'.format(value)



# ### TEST ###
# @app.callback(
#     dash.dependencies.Output('team-output-container', 'children'),
#     [dash.dependencies.Input('team_dropdown_id', 'value')]
# )
# def update_output(value):
#     return 'You have selected "{}"'.format(value)




@app.callback(
    dash.dependencies.Output('shot_graph', 'figure'),
    [dash.dependencies.Input('team_dropdown_id', 'value'),
     dash.dependencies.Input('period_slider', 'value')]
)
def build_graph(team_list, period):

    df = pd.DataFrame()

    for i in team_list:
        temp_df = sf[sf['TEAM_NAME'] == i]
        df = df.append(temp_df)

    if (period != 5):
        df = df[df['PERIOD'] == period]

    # sf_filtered = sf[sf['TEAM_NAME'] == team[0]]
    fig = px.scatter(df,
                    x='LOC_X',
                    y='LOC_Y',
                    color="SHOT_MADE_FLAG",
                    hover_name='PLAYER_NAME')

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    return fig

# Run's program with "hot-reloading"
# (i.e. when changes are made to code, app auto restarts)
if __name__ == '__main__':
    app.run_server(debug=True)
