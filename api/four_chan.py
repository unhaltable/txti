import urllib2
import json
import re

boards = ['a', 'b', 'c', 'd', 'e', 'f', 'gif', 'h', 'hr', 'k', 'm', 'o', 'p', 'r', 's', 't', 'v', 'g', 'vg', 'vr', 'w',
          'wg', 'i', 'ic', 'r9k', 's4s', 'cm', 'hm', 'lgbt', 'y', '3', 'adv', 'an', 'asp', 'biz', 'cgl', 'ck', 'co',
          'diy', 'fa', 'fit', 'gd', 'hc', 'int', 'jp', 'lit', 'mlp', 'mu', 'n', 'out', 'po', 'pol', 'sci', 'soc', 'sp',
          'tg', 'toy', 'trv', 'tv', 'vp', 'wsg', 'x']

api_call = "http://a.4cdn.org/{}/1.json"

def query(board):
    f = urllib2.urlopen(api_call.format(board))
    json_string = f.read()
    f.close()
    return json.loads(json_string)

def removeTags(WORD):
    return re.sub("<(.)*>", '', WORD)

def four_chan(l):
    s = l[0]
    if s in boards:
        json_thingy = query(s)
        return removeTags(json_thingy['threads'][0]['posts'][0]['com'])
    else:
        return "Not a board"



if __name__ == "__main__":
    print four_chan("b")