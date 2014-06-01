import urllib2
import json

api_call = 'https://www.bitstamp.net/api/ticker/'

def query():
    f = urllib2.urlopen(api_call)
    json_string = f.read()
    f.close()
    return json.loads(json_string)

def get_btc_info(l):
    json = query()
    return 'Last price: {}. In last 24hr: price high: {}, price low: {}, volume: {}, volume weighted average price: {}'.format(json['last'], json['high'], 
                                                                                                                               json['low'], json['volume'], json['vwap'])


if __name__ == '__main__':
    print get_btc_info([])