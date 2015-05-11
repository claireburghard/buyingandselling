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

def add_post(username, title, content, price):
    user = users.find_one({'username': username})
    if user == None:
        return "Unable to post"
    post = {
        'title': title,
        'content': content,
        'price': price,
    }
    user['post'] = post
    print user['post']
    return "done"
