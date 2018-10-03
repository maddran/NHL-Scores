# -*- coding: utf-8 -*-
"""

"""

import pandas as pd


res = pd.read_csv("final_scores_for_plot.csv", index_col = 0)
res.head()

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Input, Output

from heat_map import plotly_heatmap

app = dash.Dash()


# Barebones layout
app.layout = html.Div([html.H1('NHL Final Scores'),
                       dcc.Graph(id='example-graph',
                                 figure = plotly_heatmap(res, 'CGY', 'EDM')),
                                 ])
            


if __name__ == '__main__':
    app.run_server(debug=False)