# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 16:38:17 2018

@author: Madhav Narendran
"""

import numpy as np

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.widgets import GraphWidget

def gen_z(res,home,away):
    
    if home == 'All':
        resFilt = res
    else:
        resFilt = res[res.homeTeam == home]
        
    if away == 'All':
        resFilt = resFilt
    else:
        resFilt = resFilt[resFilt.awayTeam == away]
    
    hSet = range(0,max(resFilt.homeScore)+1)
    rSet = range(0,max(resFilt.roadScore)+1)
    
    z = np.zeros((len(rSet),len(hSet)))
    t = []

    c = resFilt.groupby(['roadScore','homeScore']).gamesPlayed.count()

    for j, r in enumerate(sorted(rSet, reverse = False)):
        for i,h in enumerate(sorted(hSet, reverse = False)):
            try:
                z[j][i] = int(c[j][i])
            except:
                pass
            hov = ("Home: "+str(i)+
                   "<br>Away: "+str(j)+
                   "<br>Count: "+str(int(z[j][i])))
            t.append(hov)

    t = [t[i:i+len(hSet)] for i in range(0, len(t), len(hSet))]
    
    return(z,t, hSet, rSet, resFilt)

def plotly_heatmap(res, homeTeam='All', awayTeam='All'):
    
    z,t,hSet,rSet,res = gen_z(res, homeTeam, awayTeam)
    
    data = [{
            'z': z,
            'type': 'heatmap',
            'colorscale': [
                [0, 'rgb(255, 255, 255)'],
                [0.0001, 'rgb(230,250,255)'],
                [0.01, 'rgb(150,200,255)'],
                [0.5, 'rgb(150,0,75)'],
                [0.8, 'rgb(120,0,75)'],
                [1., 'rgb(50, 0, 0)']],
            'colorbar': {
                'tick0': 0,
                'tickmode': 'array',
                'tickvals': [0, 500, 1000, 1500, 2000, 2500, 3000, 3500]},
            'hoverinfo':'text',
            'showscale': False,
            'text': t,
                            },
            go.Histogram(y = res.roadScore,
                         xaxis = 'x2',
                         marker = dict(color = 'rgba(0,0,1,.1)'),
                         hoverinfo = 'text', 
                         text = list(res.groupby('roadScore').gamesPlayed.count())), 
            go.Histogram(x = res.homeScore,
                         yaxis = 'y2',
                         marker = dict(color = 'rgba(0,0,1,.1)'),
                         hoverinfo = 'text', 
                         text = list(res.groupby('homeScore').gamesPlayed.count())),
            
            ]
            
    
    axesColor = 'rgb(200,200,200)'

    layout = go.Layout(
        titlefont = dict(size = 50, 
                         color = axesColor),
        xaxis = dict(#ticks = list(hSet),
                     domain = [0,.8], 
                     nticks=len(hSet)+1,
                     fixedrange = True,
                     side = 'top',
                     ticklen = 0,
                     tickfont = dict(color = axesColor, size = 15),
                     title='',
                     titlefont=dict(size=18,color=axesColor)),
        yaxis = dict(#ticks= list(rSet),
                     domain = [0.2,1],
                     autorange = 'reversed', 
                     fixedrange = True,
                     nticks=len(rSet)+1,
                     ticklen = 0,
                     tickfont = dict(color = axesColor, size = 15)),
        xaxis2 = dict(zeroline = False,
                      domain = [0.8,1],
                      fixedrange = True,
                      scaleratio = 10,
                      showgrid = False,
                      tickfont = dict(color = axesColor, size = 8),
                      showticklabels=False),
        yaxis2 = dict(zeroline = False,
                      domain = [0,.2],
                      autorange = 'reversed', 
                      fixedrange = True,
                      scaleratio = 10,
                      showgrid = False,
                      tickfont = dict(color = axesColor, size = 8),
                      showticklabels=False),
        annotations = [dict(x=0, y=1.11, xref = 'paper', yref = 'paper',
                            showarrow = False,
                            text = '<b>home<b>', 
                            font = dict(size=25, color = axesColor)),
                       dict(x=-0.1, y=1, xref = 'paper', yref = 'paper',
                            showarrow = False,
                            text = '<b>away<b>',
                            textangle = -90,
                            font = dict(size=25, color = axesColor))],
        showlegend = False,
        hovermode = 'closest',
#         autosize = True,
        height = 550,
        width = 600,
        margin = dict(r=0, b=0),
        )
    


    fig = go.Figure(data = data, layout = layout)
    
    return fig