import urllib2
import xml.etree.ElementTree as ET


api_call = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{0}?key=9baecd26-8583-4b74-9922-ce2a1170df9d"

def query(word):
    f = urllib2.urlopen(api_call.format(word))
    xml_string = f.read()
    f.close()
    return ET.fromstring(xml_string)

def getDefinition(word):
    parsed_xml = query(word)
    entry = parsed_xml[0]
    for node in entry:
        if node.tag == 'def':
            for other_node in node:
                if other_node.tag == 'dt':
                    return other_node.text[1:]


if __name__ == "__main__":
    defineWord("league")