from api.weather import weather_current
from flask import Flask, request
import twilio.twiml

from parser import parse

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
    request_parts = parse(query)
    request_type = request_parts[0]

    # TODO: Instead of returning the raw query, call a function to get data corresponding to the request type
    return weather_current('Canada', 'Toronto')

if __name__ == '__main__':
    app.run(debug=True)