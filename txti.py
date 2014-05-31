from flask import Flask, request
import twilio.twiml

from parser import parse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    from_number = request.values.get('From', None)
    body = request.values.get('Body', None)
    resp = twilio.twiml.Response()
    resp.message(body)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)