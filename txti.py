from flask import Flask
import twilio.twiml

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)