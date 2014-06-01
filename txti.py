from api.nextbus import get_bus_prediction
from api.weather import weather_current
from flask import Flask, request, render_template, redirect, url_for
import pymongo
import twilio.twiml
import loginsys, dbhelper

import parser

app = Flask(__name__)

def serve_static(filename):
    f = open("./static/"+filename)
    n = f.readlines()
    f.close()
    print n
    return reduce(lambda a, b: a+"\n" + b, n)

@app.route('/', methods=['GET', 'POST'])
def index():
    return serve_static("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        return serve_static("login.html")
    else:
        return serve_static("login.html")

#login push
@app.route('/login-push', methods=["POST"])
def login_push():
    pass

#register push
@app.route('/register-push', methods=["POST"])
def register_push():
    pass


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    #chck cookie exists
    if not hasattr(request, 'txtisessionkey'):
        return app.make_response(redirect("/login")) 
    else:
        client = pymongo.MongoClient(mongoaddr, mongoport)
        user = login.is_key_valid(request.txtisessionkey)
        if user:
            #TODO serve the dashboard
            return "yay you're logged in"
        else:
            return app.make_response(redirect("/login"))

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
    f = parser.Formula("bustime", "Next bus for {{route}} {{direction}} at {{intersection}}", get_bus_prediction)
    p = parser.Parser()
    p.addFormula(f)
    return p.parse("Next bus for 116 North at Coronation and Lawrence")

    # TODO: change this
    return weather_current('Canada', 'Toronto')





if __name__ == '__main__':
    app.run(debug=True)