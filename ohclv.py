import ccxt
import pandas as pd
import numpy as np
import time
import os
import errno
import math
from TA import zigzag

# DATOS

def is_numeric(obj):
    attrs = ['__add__', '__sub__', '__mul__', '__truediv__', '__pow__']
    return all(hasattr(obj, attr) for attr in attrs)

def ohcl(moneda = 'ETH/USD', exchange = ccxt.bitmex, tf = '1m'):
    df = pd.DataFrame()



    pd.set_option('expand_frame_repr', False)
    limit = 500

    current_time =int(time.time()//60 * 60 * 1000)
    print(current_time)


    if tf == ('1m'):
        since_times = current_time - limit *1000 *60
        datas = exchange().fetch_ohlcv(symbol=moneda, timeframe = tf, limit=limit, since=since_times)
        df = pd.DataFrame(datas)
        i = 1
        while i < 5:
            since_time = current_time - limit*i *1000 *60
            df = df.append(exchange().fetch_ohlcv(symbol=moneda, timeframe = tf, limit=limit, since=since_time))
            i +=1
            print(df)
            time.sleep(0.5)
    
    if tf == ('1h'):

        since_times = current_time - limit *1000 *60 *60
        datas = exchange().fetch_ohlcv(symbol=moneda, timeframe = tf, limit=limit, since=since_times)
        df = pd.DataFrame(datas)
        i = 1
        while i < 5:
            since_time = current_time - limit*i *1000 *60 *60
            df = df.append(exchange().fetch_ohlcv(symbol=moneda, timeframe = tf, limit=limit, since=since_time))
            i +=1
            print(df)
            time.sleep(0.5)


    if tf == ('1d'):
        since_times = current_time - limit *1000 *60 *60 *24
        datas = exchange().fetch_ohlcv(symbol=moneda, timeframe = tf, limit=limit, since=since_times)
        df = pd.DataFrame(datas)
        i = 1
        while i < 5:
            since_time = current_time - limit*i *1000 *60 *60 *24
            df = df.append(exchange().fetch_ohlcv(symbol=moneda, timeframe = tf, limit=limit, since=since_time))
            i +=1
            print(df)
            time.sleep(0.5)


    df = df.rename(columns={0: 'x',1: 'open',2:'high',3:'low',4:'close',5:'volume'})

    df['x'] = pd.to_datetime(df['x'], unit='ms')

    if not os.path.isfile(moneda + tf + '.csv'):
        try:
            os.makedirs(os.path.dirname(moneda + tf + '.csv'))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise 

        with open(moneda + tf + '.csv', "w") as f:
            f.write("0")

    csv = pd.read_csv(moneda + tf + '.csv',  index_col=False)

    df = pd.concat([df, csv], ignore_index=True)

    df = df.drop_duplicates(subset=['x'], keep='last')

    df.to_csv((moneda + tf + '.csv') , index=False)

    #Clean data

    clean = pd.read_csv(moneda + tf + '.csv',  index_col=False)
    clean = clean.drop_duplicates(subset=['x'], keep='last')
    clean.sort_values(by=['x'])
    clean.to_csv((moneda + tf + '.csv') , index=False) 

    print(clean)

    df2 = pd.read_csv(moneda + tf + '.csv',  index_col=False)
    #ZigZag
    zz = zigzag(df2, pct=1)
    df2['zigzag'] = zz
    df2.to_csv((moneda + tf + '.csv') , index=False)

    csvdos = pd.read_csv(moneda + tf + '.csv',  index_col=False)
    print(csvdos)

    #ZigZag
    df3 = csvdos[~np.isnan(csvdos['zigzag'])][['x','open','high','low','close','volume', 'zigzag']]
    df3['zup']=0
    df3['zdn']=0
    df3.to_csv((moneda + tf + 'ZigZag.csv') , index=False)

    df4 = pd.read_csv(moneda + tf + 'ZigZag.csv',  index_col=False)
    print(df4)


    def zup (x):

        if df4['zigzag'][x] > df4['zigzag'][x-1]:
            df4['zup'][x] = df4['zigzag'][x]

    for x in range(1,len(df4['zigzag'])):
        zup(x)

    def zdn (x):
    
        if df4['zigzag'][x] < df4['zigzag'][x-1]:
            df4['zdn'][x] = df4['zigzag'][x]

    for x in range(1,len(df4['zigzag'])):
        zdn(x)
    
    df4.to_csv((moneda + tf + 'ZigZag.csv') , index=False)
    df5 = pd.read_csv(moneda + tf + 'ZigZag.csv',  index_col=False)

    df6 = pd.concat([csvdos, df5])
    df6.sort_values(by=['x'])
    df6 = df6.drop_duplicates(subset=['x'], keep='last')
    df6.sort_values(by=['x'])
    df6.to_csv((moneda + tf + '.csv') , index='x')

    df7 = pd.read_csv(moneda + tf + '.csv',  index_col=False)
    df7.sort_values(by=['x'])
    df7 = df6.drop_duplicates(subset=['x'], keep='last')
    df7.to_csv((moneda + tf + '.csv') , index='x')

    print(df7)

ohcl()