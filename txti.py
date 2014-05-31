from api.weather import weather_current
from flask import Flask, request
import twilio.twiml

import parser

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
def txti():
    # Get parameters from request
    from_number = request.values.get('From', None)
    body = request.values.get('Body', None)

    # Create the response string by parsing the query, calling relevant APIs, and returning a string
    response = get_response(body)

    # Create the response to be sent back to the user
    resp = twilio.twiml.Response()
    resp.message(response)
    return str(resp)


def get_response(query):
    f = parser.Formula("bustime", "Next bus for {{route}} at {{intersection}}", get_bus_prediction)
    p = parser.Parser()
    p.addFormula(f)
    return p.parse("Next bus for 116 at Coronation and Lawrence")

    # TODO: change this
    return weather_current('Canada', 'Toronto')


def get_bus_prediction(params):
    return 'Next bus for'


if __name__ == '__main__':
    app.run(debug=True)