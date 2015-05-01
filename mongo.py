from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.proj
users = db.users

def add_user(username,password,name):
    user = {
        'username' : username,
        'password' : password,
        'name' : name,
    }
    return users.insert(user)

def user_exists(username):
    user = users.find_one({'username': username})
    if user == None:
        return "does not exist"
    else:
        return "exists"

def authenticate( username, passw ):
    user = users.find_one({'username': username})
    if user  == None:
        return "Username does not exist"
    elif user['password'] != passw:
        return "Password and username do not match"
    return "match"



