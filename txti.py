from api.nextbus import get_bus_prediction
from api.weather import weather_current
from flask import Flask, request, render_template, redirect, url_for
import pymongo
from initializer import getParser
import twilio.twiml
import loginsys
import api.dbhelper as dbhelper
import parser
from urllib import quote_plus

mongoport = 27017
mongoaddr = "localhost"

app = Flask(__name__)

def serve_static(filename):
    f = open("./static/"+filename)
    n = f.readlines()
    f.close()
    return reduce(lambda a, b: a+"\n" + b, n)

@app.route('/', methods=['GET', 'POST'])
def index():
    return serve_static("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return serve_static("login.html")

def dologin(form):
    conn = pymongo.MongoClient(mongoaddr, mongoport)
    print form["username"], form["password"]
    n = loginsys.get_login_key(conn, form["username"], form["password"])
    conn.disconnect()

    print n

    if n[0]:
        response = app.make_response(redirect("/dashboard") )
        response.set_cookie("txtisessionkey", value=n[1])
    else:
        response = app.make_response(redirect("/login?failure=login") )
    return response
    

#login push
@app.route('/login_push', methods=["POST"])
def login_push():
    if request.method == 'POST':
        return dologin(request.form)
    else:
        response = app.make_response(redirect("/login?failure=login") )
        return response

#register push
@app.route('/register_push', methods=["POST"])
def register_push():
    msg=""
    if request.method == 'POST':
        if all([ (x in request.form.keys()) for x in ["username","password","email","phone"] ] ):
            session = dbhelper.db_session()
            try:
                session.register_user(request.form["username"], request.form["password"], request.form["phone"], request.form["email"])
                session.close()
                return dologin(request.form)
            except(Exception) as e:
                msg = e.message
                session.close()
        else:
            msg="not all fields filled"
    response = app.make_response(redirect("/login?failure=register?msg=%s"%( quote_plus(msg)  )) )
    return response



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
    response = getParser.parse(body)

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