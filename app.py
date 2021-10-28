# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# Toy dataset
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# Toy Graph
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")


### APP LAYOUT PORTION ###
app.layout = html.Div(children=[
    html.H1(children='BLAAAAAHHH Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


# Run's program with "hot-reloading"
# (i.e. when changes are made to code, app auto restarts)
if __name__ == '__main__':
    app.run_server(debug=True)