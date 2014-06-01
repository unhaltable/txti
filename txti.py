from urllib import quote_plus

from flask import Flask, request, redirect, render_template
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
    name = "login/register"
    if("txtisessionkey" in request.cookies.keys()):
        helper = dbhelper.db_session()
        userid = loginsys.is_key_valid(helper.mongoclient, request.cookies["txtisessionkey"])
        user = helper.user_from_uid(userid)
        helper.close()
        name = user["username"]
    return render_template("index.html", topright_text=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if("txtisessionkey" in request.cookies.keys()):
        helper = dbhelper.db_session()
        userid = loginsys.is_key_valid(helper.mongoclient, request.cookies["txtisessionkey"])
        if userid:
            return redirect("/dashboard")
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
                session.register_user(
                    request.form["username"],
                    request.form["password"],
                    [request.form["phone"]] ,
                    request.form["email"])
                session.close()
                return dologin(request.form)
            except(Exception) as e:
                msg = e.message
                session.close()
        else:
            msg="not all fields filled"
    response = app.make_response(redirect("/login?failure=register?msg=%s"%( quote_plus(msg)  )) )
    return response

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    client = pymongo.MongoClient(mongoaddr, mongoport)
    loginsys.kill_key(client , request.cookies['txtisessionkey'])
    client.disconnect()
    response = app.make_response(redirect("/") )
    response.set_cookie("txtisessionkey", value="", expires=0)
    return response

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    #chck cookie exists
    if not 'txtisessionkey' in request.cookies.keys():
        return app.make_response(redirect("/login")) 
    else:
        helper = dbhelper.db_session()
        userid = loginsys.is_key_valid(helper.mongoclient, request.cookies["txtisessionkey"])
        user = helper.user_from_uid(userid)
        helper.close()

        print request.cookies["txtisessionkey"]
        if user:
            return serve_dashboard(user)
        else:
            response = app.make_response(redirect("/login?msg=login+expired"))
            response.set_cookie("txtisessionkey", value="", expires=0)
            return response

all_apis=[
    {
        "api-id": "facebook",
        "api-name": "Facebook",
        "email": None,
        "password": None
    },
    {
        "api-id": "fakeapi1",
        "api-name": "Fake API 1",
        "username": None,
        "password": None
    },
    {
        "api-id": "fakeapi2",
        "api-name": "Fake API 2",
        "username": None,
        "password": None,
        "thirdfield": None
    }
]

def serve_dashboard(user):
    #formatted_phones = ["(%c%c%c) %c%c%c-%c%c%c%c" % tuple(map(ord, numb)) for numb in user["phone_numbers"]]
    base_string = render_template(
        "dashboard.html",
        username=user["username"],
        userapis=user["apis"].keys(),
        phonenumbers=user["phone_numbers"],
        allapis=all_apis)
    #TODO SERV
    return base_string

@app.route('/addapi', methods=['POST'])
def addapi():
    if("txtisessionkey" in request.cookies.keys()):
        helper = dbhelper.db_session()
        userid = loginsys.is_key_valid(helper.mongoclient, request.cookies["txtisessionkey"])
        if "api-id" in request.form.keys():
            proper_apis = filter(lambda x: x["api-id"] == request.form["api-id"], all_apis)
            if len(proper_apis)>0:
                proper_api = proper_apis[0]
                print construct_to_fit(proper_api, request.form)
                helper.register_api_login(userid, proper_api["api-id"], construct_to_fit(proper_api, request.form))
                helper.close();
                return "successfully registered!"
            print "shit"
            return "error finding app-id"
        print "shit!"
        return "api-id DNE tho."
    else:
        return "not logged in!"

def construct_to_fit(api, parts):
    new = {}
    for i in api.keys():
        if i!="api-name" and i!= "api-id":
            new[i]=(parts[i])
    return new

@app.route('/api', methods=['GET', 'POST'])
def txti():
    # Get parameters from request
    from_number = request.values.get('From', None)
    body = request.values.get('Body', '')

    # Log request
    app.logger.info('Received SMS:\n'
                    '{}'.format(body))

    # Create the response string by parsing the query, calling relevant APIs, and returning a string
    response = get_parser().parse(body)

    # Log response
    app.logger.info('Sending response:\n'
                    '{}'.format(response))

    # Create the response to be sent back to the user
    resp = twilio.twiml.Response()
    resp.message(response)
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)