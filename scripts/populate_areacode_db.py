import pymongo, urllib2, re, json


srcurl = "http://www.bennetyee.org/ucsd-pages/area.html"

def parse_html_table(tablestr):
	depth = 0
	xcounter = 0
	buff = ""
	records = []
	for c in tablestr:
		if c == '<':
			depth+=1
			if buff != "":
				records.append(buff)
			buff = ""
		elif c == '>':
			depth-=1
		elif depth == 0:
			if(c != "\n"):
				buff += c
	return records

def parse_website(srcurl):
	print "downloading",srcurl
	response = urllib2.urlopen(srcurl)
	html = response.read()

	#print html

	print "finding table regex"

	pattern = re.compile("<table border=1.*?\\/table", flags=re.DOTALL)
	b = pattern.findall(html)
	
	print len(b)
	
	table = min(b, key=lambda a: len(a))

	print "table found %s chars"%(len(table))

	print "parsing table"

	return parse_html_table(table)

def list_to_dict(keys, lst):
	out=[]
	assmel = {}
	for k in range(len(lst)):
		if (lst[k] != None):
			assmel[keys[k%len(keys)]] = lst[k]
		else:
			assmel[keys[k%len(keys)]] = None
			
		if k%len(keys) == len(keys)-1:
			out.append(assmel.copy())
			assemel = {}

	return out

if __name__ == "__main__":
	b = parse_website(srcurl)
	a = list_to_dict(["code","state","timezone","desc"],b[6:])
	print json.dumps(a,indent=2)
