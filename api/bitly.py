import urllib2
import json

api_call = 'https://api-ssl.bitly.com/v3/shorten?access_token=b64903c3af1d8efeab2b5b076dead34367ea2aa6&longUrl={}'

def query(url):
    f = urllib2.urlopen(api_call.format(url))
    json_string = f.read()
    f.close()
    return json.loads(json_string)

def shorten_url(l):
    json = query(l[0])
    return json['data']['url']


if __name__ == '__main__':
    print shorten_url(['http://www.unhaltable.com'])