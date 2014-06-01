import urllib2
import json

api_call = 'https://www.bitstamp.net/api/ticker/'

def query():
    f = urllib2.urlopen(api_call)
    json_string = f.read()
    f.close()
    return json.loads(json_string)

def get_btc_last(l):
    json = query()
    return 'Last BTC price: ' + json['last']

def get_btc_high(l):
    json = query()
    return 'Last 24 hours price high: ' + json['high']

def get_btc_low(l):
    json = query()
    return 'Last 24 hours price low: ' + json['low']

def get_btc_volume(l):
    json = query()
    return 'Last 24 hours volume: ' + json['volume']

def get_btc_vwap(l):
    json = query()
    return 'Last 24 hours volume weighted average price: ' + json['vwap']


if __name__ == '__main__':
    print get_btc_last([])
    print get_btc_high([])
    print get_btc_low([])
    print get_btc_volume([])
    print get_btc_vwap([])