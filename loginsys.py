import pymongo, uuid, time  

"""
Assumed that on the same machine, a mongodb server is running on
the same machine, port listed below
pymongo 2.7.1
"""
mongoport = 27017
mongoaddr = "localhost"


"""
client:mongoclient
key: the key to test

returns false if key is invalid
otherwise, returns the uid of the user who the key belongs to
"""
def is_key_valid(client, key):
    #check it's in the db
    if (client.keys.find({"uuid":key}).count() == 0):
        return False

    #check it's still valid
    keyobj = client.keys.find({"uuid":key})
    if (keyobj.expires < time.time()):
        return keyobj.userid
    else:
        client.keys.remove({"uuid":key})

"""
clinet: mongoclient
uid: user id
inserts a new key into key dict and returns it
"""
def make_key(client, uid):
    luuid = str(uuid.uuid4())
    while (client.txti.keys.find({"uuid":luuid}).count() > 0):
        luuid = str(uuid.uuid4())

    #expires in an hour
    client.txti.keys.insert({"userid":uid, "uuid" :luuid, "expires": time.time()+(60*60)})
    return luuid

"""
client: mongoclient
username: 
password_hash: lel like we even bother hashing
returns (successbool, key)
"""
def get_login_key(client, username, password_hash):
    user = client.txti.users.find_one({"username":username, "password_enc":password_hash})
    if user == None:
        return (False, None)
    else:
        return (True, make_key(client, user[u'_id']))