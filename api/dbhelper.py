import pymongo

"""
Assumed that on the same machine, a mongodb server is running on
the same machine, port listed below
pymongo 2.7.1
"""
mongoport = 27017
mongoaddr = "localhost"

"""
Databases:

txti.users {
    usernname,
    password_enc,
    phone_number,
    apis{
        fakeapi: <reference to entry on txti_api_fakeapi>
    }
}

txti.api_fakeapi {
    user: <reference to user in txti_users,
    fakeapi_username
    password_enc
}

"""

class db_session():

    def __init__(self):
        self.mongoclient = pymongo.MongoClient(mongoaddr, mongoport)

    #############
    #   Users   #
    #############

    def uid_by_number(self, phone_number):
        db = self.mongoclient.txti
        usr = db.users.find_one({"phone_numbers": phone_number});
        if usr == None:
            raise Exception("No Phone with that number")

        return usr[u'_id']

    def uid_by_name(self, username):
        db = self.mongoclient.txti
        return db.users.find({"username": username})[u'_id']

    
    """
    register a new user, and return a reference to that username (the _id field)
    """
    def register_user(self, username, password_enc, phone_numbers, email):
        db = self.mongoclient.txti

        #check if a user with that phone number or username exists
        if( 
            any(
                [ db.users.find({"phone_numbers": n}).count()>0
                    for n in phone_numbers])):
            raise Exception("one of those numbers is in use")
        elif(db.users.find({"username": username}).count()>0):
            raise Exception("username in use")

        client = {
            "username" : username,
            "password_enc" : password_enc,
            "phone_numbers" : phone_numbers,
            "email": email,
            "apis": {}
        }

        return db.users.insert(client)




    ##################
    #   API Logins   #
    ##################

    """
    register a new login for a given user, using the _id field

    will overwrite existing api logins.
    loginf is a dict of relevant login information
    """
    def register_api_login(self, _id, api_name, loginf):
        db = self.mongoclient.txti
        client = db.users.find_one({"_id": _id});
    
        api_collection = db["api_"+api_name]
        api_collection.remove({"_user":_id})

        api_id = api_collection.insert(
            joindict({"_user": _id}, loginf)
        )

        oldapis = client[u'apis']
        db.users.update({'_id':_id}, {"$set": 
            {
                "apis."+api_name: api_id
            }
        })



    def loginid_from_number(self, phone_number, api_name):
        db = self.mongoclient.txti
        user = db.users.find_one({"phone_numbers": phone_number})

        if not api_name in user[u'apis'].keys():
            raise Exception("no login registered for that user")

        return user[u'apis'][api_name]

    def loginid_from_uid(self, _id, api_name):
        db = self.mongoclient.txti
        user = db.users.find_one({"_id": _id})

        if not api_name in user[u'apis'].keys():
            raise Exception("no login registered for that user")

        return user[u'apis'][api_name]

    def login_from_number(self, phone_number, api_name):
        return self.mongoclient.txti["api_"+api_name].find_one({"_id":
            self.loginid_from_number(phone_number, api_name)
            })

    def login_from_uid(self, _id, api_name):
        return self.mongoclient.txti["api_"+api_name].find_one({"_id":
            self.loginid_from_uid(_id, api_name)
            })

    #################
    #  Etc Helpers  #
    #################

    def close(self):
        self.mongoclient.disconnect()

#helper method for me
def joindict(*dicts):
    return dict(reduce(lambda a,b: a+b, [d.items() for d in dicts]))    

if __name__ == "__main__":
    session = db_session()
    try:
        uid = session.register_user(
            "cooluser!!",
            "this is the encoded password",
            ["2153611301236"],
            "fake@email.ru"
        )
    except (Exception) as ex:
        uid = session.uid_by_number("2153611306")


    session.register_api_login(uid, "fakeapi",
        {
            "fakeapi_username": "AdjectiveObject",
            "password_enc": "password"
        })

    print(session.login_from_number("2153611306", "fakeapi"))
    print(session.login_from_uid(uid, "fakeapi"))

    session.close()