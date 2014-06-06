import requests
from xml.etree import ElementTree


def get_json_data(url, verify=True):
    response = requests.get(url, verify)
    return response.json()

def get_xml_data(url, verify=True):
    response = requests.get(url, verify)
    tree = ElementTree.fromstring(response.content)
    return tree


if __name__ == '__main__':
    print get_json_data('https://api-ssl.bitly.com/v3/shorten?access_token=b64903c3af1d8efeab2b5b076dead34367ea2aa6&longUrl=http://www.unhaltable.com')
