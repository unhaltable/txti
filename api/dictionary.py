import urllib2
import json

api_call = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{0}?key=9baecd26-8583-4b74-9922-ce2a1170df9d"

def query(word):
    f = urllib2.urlopen(api_call.format(word))
    json_string = f.read()
    f.close()
    return json.loads(json_string)

def defineWord(word):
    parsed_json = query(word)
    print "lol"

if __name__ == "__main__":
    defineWord("league")