import urllib2
import json


def get_json_data(url):
    f = urllib2.urlopen(url)
    json_string = f.read()
    f.close()
    return json.loads(json_string)

def get_xml_data(url):
    pass


if __name__ == '__main__':
    print get_json_data('https://api-ssl.bitly.com/v3/shorten?access_token=b64903c3af1d8efeab2b5b076dead34367ea2aa6&longUrl=http://www.unhaltable.com')
