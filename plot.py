import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import pandas as pd
from datetime import datetime

import numpy as np

init_notebook_mode()

df = pd.read_csv('ETH/USD1m.csv')


trace1 = go.Candlestick(x=df['x'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])



Trend = df[~np.isnan(df['zigzag'])]




trace5 = go.Scatter(
    x=Trend['x'],
    y=Trend['zigzag'],
    mode='lines',
    name = 'zigzagC', # Style name/legend entry with html tags
)
trace6 = go.Scatter(
    x=Trend['x'],
    y=Trend['zdn'],
    mode='markers',
    name = 'Untested Level', # Style name/legend entry with html tags
)

trace7 = go.Scatter(
    x=Trend['x'],
    y=Trend['zup'],
    mode='lines',
    name = 'Untested Levels', # Style name/legend entry with html tags
)

data = ([trace1, trace5, trace6, trace7])


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