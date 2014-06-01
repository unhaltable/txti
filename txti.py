from urllib import quote_plus

from flask import Flask, request, redirect
import os
import pymongo
from initializer import get_parser
import twilio.twiml
import loginsys
import api.dbhelper as dbhelper


mongoport = 27017
mongoaddr = "localhost"

app = Flask(__name__)

# Direct logs to stdout
if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('txti')


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
        response.set_cookie("txtisessionkey", value=n[1], expires=n[2])
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
    if not 'txtisessionkey' in request.cookies.keys():
        return app.make_response(redirect("/login")) 
    else:
        client = pymongo.MongoClient(mongoaddr, mongoport)
        user = loginsys.is_key_valid(client, request.cookies["txtisessionkey"])
        client.disconnect()
        print request.cookies["txtisessionkey"]
        if user:
            #TODO serve the dashboard
            return serve_dashboard()
        else:
            response = app.make_response(redirect("/login?msg=login+expired"))
            response.set_cookie("txtisessionkey", value="", expires=0)
            return response

def serve_dashboard():
    base_string = serve_static("dashboard/index.html")
    return base_string

@app.route('/api', methods=['GET', 'POST'])
def txti():
    # Get parameters from request
    from_number = request.values.get('From', None)
    body = request.values.get('Body', '')

    # Log request
    app.logger.info('Received SMS:\n'
                    '{}'.format(body))

    # Create the response string by parsing the query, calling relevant APIs, and returning a string
    parser = get_parser()
    response = None
    try:
        response = parser.parse(body) # or 'Invalid command'
    except Exception as e:
        print e
        response = 'Invalid command'

    # Log response
    app.logger.info('Sending response:\n'
                    '{}'.format(response))

    # Create the response to be sent back to the user
    resp = twilio.twiml.Response()
    resp.message(str(response))
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)