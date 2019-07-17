from ohcl import ohcl
import ccxt

ohcl(moneda = 'BTC/USD', exchange = ccxt.bitmex, tf = '1h')
