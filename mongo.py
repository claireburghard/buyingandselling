from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.proj
users = db.users
posts = db.posts

##### USER #####
def add_user(username,password,name, bio):
    user = {
        'username' : username,
        'password' : password,
        'name' : name,
        'bio' : bio,
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

def get_name(username):
    user = users.find_one({'username':username})
    if user == None:
        return "User not found"
    name = user['name']
    return name

def get_password(username):
    user = users.find_one({'username':username})
    if user == None:
        return "User not found"
    password = user['password']
    return password

def get_bio(username):
    user = users.find_one({'username':username})
    if user == None:
        return "User not found"
    bio = user['bio']
    return bio

def update_name(username, new_name):
    user = users.find_one({'username':username})
    uname = user['username']
    #name = user['name']
    password = user['password']
    bio = user['bio']
    db.users.update( {'username': username}, {'username': username, 'name':new_name, 'password': password, 'bio':bio} )
    return

def update_password(username, new_pass):
    user = users.find_one({'username':username})
    uname = user['username']
    name = user['name']
    #password = user['password']
    bio = user['bio']
    db.users.update( {'username': username}, {'username': username, 'name':new_name, 'password': new_pass, 'bio':bio} )
    return

def update_bio(username, new_bio):
    user = users.find_one({'username':username})
    uname = user['username']
    name = user['name']
    password = user['password']
    #bio = user['bio']
    db.users.update( {'username': username}, {'username': username, 'name':name, 'password': password, 'bio':new_bio} )
    return

##### ^^^^^ USER ^^^^^ #####

##### POSTS #####
def add_post(username, title, content, start_price, time_start, time_ends, tags):
    post = {
        'username' : username,
        'title': title,
        'content' : content,
        'price' : start_price,
        'time_start' : time_start,
        'time_ends' : time_ends,
        'tags' : tags,
    }
    #print post
    return posts.insert(post)

def get_posts(username):
    result = []
    counter = 0
    for post in  posts.find({'username':username}):
        counter = counter + 1
        result.append(post)
        #print counter
    return result

##### ^^^^^ POSTS ^^^^^ #####

print "1"
#add_user('rebecca','rebecca','rebecca','my life')
#add_post('rebecca','testing','testing','$$','early','late')
#update_name('rebecca','rebecca')
#print get_name('rebecca')
print
print
print "2"
#add_post('rebecca','test2','test2','$','soon','not soon')
print
print
print "3"
#print get_posts('rebecca')
print
print
print "4"
#print get_posts('lol')

#db.posts.remove()
#db.users.remove()
#print db.posts
