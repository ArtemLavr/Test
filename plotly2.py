import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import pandas as pd
from datetime import datetime

import numpy as np

init_notebook_mode()

df = pd.read_csv("bitmex_data.csv")

trace1 = go.Candlestick(x=df['x'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])

df.loc[df.sup <= 0.000001, 'sup'] = 'Nul' 
df.loc[df.res <= 0.000001, 'res'] = 'Nul' 


trace2 = go.Scatter(
    x=df['x'],
    y=df['sup'],
    mode='markers',
    name = 'support', # Style name/legend entry with html tags
)

trace3 = go.Scatter(
    x=df['x'],
    y=df['res'],
    mode='markers',
    name = 'ressistance', # Style name/legend entry with html tags
)

Trend = df[~np.isnan(df['zigzag'])]


trace4 = go.Scatter(
    x=Trend['x'],
    y=Trend['zigzag'],
    mode='lines',
    name = 'zigzag', # Style name/legend entry with html tags
)

#trace5 = go.Scatter(
#    x=df['x'],
#    y=df['untested'],
#    mode='lines',
#    name = 'Untested Level', # Style name/legend entry with html tags
#)

#data = ([trace1, trace2, trace3, trace4, trace5])
data = ([trace1, trace2, trace3, trace4])

layout = go.Layout(
    xaxis = dict(
        rangeslider = dict(
            visible = False
        )
    )
)
    

fig = dict(data=data, layout=layout)

config={'showLink': True}
plot(fig, filename='simple_ohlc.html', config=config)