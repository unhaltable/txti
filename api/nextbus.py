import urllib2
import xml.etree.ElementTree as ET

nextbus_route_config = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ttc&r={}'
nextbus_stop_config = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictionsForMultiStops&a=ttc&stops={}%7C{}'


def parse_xml(file, tag_name, attr1, attr2):
    f = urllib2.urlopen(file)
    xml_string = f.read()
    f.close()
    return ET.fromstring(xml_string)


def get_stop(stops, intersection):
    entry = stops[0]
    for node in entry:
        if node.tag == 'stop':
            title = node.attrib['title'].split(' At ')
            if intersection[1:] == title[:-1] or intersection == title:
                return node.attrib['tag']
    return -1


def get_bus_prediction(l):
    params = l[0].split(' ')
    params.remove('at')
    params[2:] = [' '.join(params[2:])]

    route_tag = params[0]     # 506
    direction = params[1]     # West
    intersection = params[2]  # "College St and St George St"

    stops = parse_xml(nextbus_route_config.format(route_tag), 'stop', 'tag', 'title')
    stop_id = get_stop(stops, intersection.split(' and '))

    if stop_id == -1:
        return 'Could not find stop'

    predictions = parse_xml(nextbus_stop_config.format(route_tag, stop_id), 'prediction', 'seconds', 'minutes')
    try:
        first_prediction = list(predictions)[0][0][0].attrib
        minutes = first_prediction['minutes']
        seconds = first_prediction['seconds']
        actual_seconds = int((int(seconds)/60.0) % 1 * 60)
        if actual_seconds < 10: actual_seconds = '0' + str(actual_seconds)

        return 'Next bus for {} {} at {} is coming in {}m and {}s.'.format(route_tag, direction, intersection, minutes, actual_seconds)
    except:
        return 'No predictions available'


if __name__ == '__main__':
    print get_bus_prediction(['310 North at Bathurst St and Dewlane Dr'])
    print get_bus_prediction(['506 West at College St and St George St'])