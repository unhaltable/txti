import urllib2
import json

api_block = 'https://www.dogeapi.com/wow/v2/?a=get_current_block'
api_value = 'https://www.dogeapi.com/wow/v2/?a=get_current_price&convert_to=USD&amount_doge=1'
api_difficulty = 'https://www.dogeapi.com/wow/v2/?a=get_difficulty'

def query(url):
    f = urllib2.urlopen(url)
    json_string = f.read()
    f.close()
    return json.loads(json_string)

def get_doge_info(l):
	block = query(api_block)[u'data'][u'current_block']
	value = query(api_value)[u'data'][u'amount']
	difficulty = query(api_difficulty)[u'data'][u'difficulty']

	return "Current value of doge: %s cents USD\nCurrent block: %s\nCurrent mining difficulty rating: %s\n"%(value*100, block, difficulty)

if __name__ == "__main__":
	print get_doge_info([])