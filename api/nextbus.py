import xml.etree.ElementTree as ET
import requests

nextbus_route_config = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ttc&r={}'

def get_bus_prediction(params):
    route_tag = params[0]
    direction = params[1]
    intersection = params[2]
    route_config = requests.get(nextbus_route_config.format(route_tag))

    tree = ET.fromstring(route_config.content)
    # TODO: parse xml tree

    return 'Next bus for {} {} at {}'.format(route_tag, direction, intersection)