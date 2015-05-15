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
    if user == None:
        return "Username does not exist"
    elif user['password'] != passw:
        return "Password and username do not match"
    return "match"

def add_post(username, title, content, price):
    user = users.find_one({'username': username})
    print user
    if user == None:
        return "Unable to post"
    post = {
        'title': title,
        'content': content,
        'price': price,
    }
    user['post'] = post
    print "post"
    print user['post']
    print "user"
    print user
    return "done"

def get_posts(username):
    user = users.find_one({'username':username})
    #post = user.find_one({
    if user == None:
        return "whoops"
    print 'user'
    print user
    return

def add_message(username, otheruser, content):
    user = users.find_one({'username': username})
    ouser = users.find_one({'username':otheruser})
    if user == None or ouser == None:
        return "unable to message"
    message = {
        'otheruser': otheruser,
        'content': content,
    }
    user['message'] = message


add_post('rebecca','test1','test1','test1')
print get_posts('rebecca')
