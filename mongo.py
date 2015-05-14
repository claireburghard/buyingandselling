from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.proj
users = db.users

def add_user(username,password,name):
    user = {
        'username' : username,
        'password' : password,
        'name' : name,
        'posts': {},
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
   # print user
    if user == None:
        return "Unable to post"
    post = {
        'title': title,
        'content': content,
        'price': price,
    }
    name = user['name']
    password = user['password']
    username = user['username']
    posts = user['posts']
    #print "HERE"
    #print posts
    print post
    #db.users.update( {'username':username}, {'name':name, 'password':password, 'username':username, 'posts':post} )
    print user['posts']
    db.users.user.posts.insert([posts, post])
    print "HERE"
    print user['posts']
    return

def get_posts(username):
    user = users.find_one({'username':username})
    if user == None:
        return "User not found"
    post = user['posts']
    if post == None:
        return "No posts"
    return post

def get_name(username):
    user = users.find_one({'username':username})
    if user == None:
        return "User not found"
    name = user['name']
    return name


#add_user('testuname','testpass','testname')
#print get_posts('testuname')
print add_post('testuname','testtitle','testcontent','testprice')
print add_post('testuname','test2','test2','test2')
