from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.proj
users = db.users
posts = db.posts
messages = db.messages

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
        #price attribute will keep changing based on what the highest bid is
        'price' : start_price,
        'highest_bidder': None, #this will be someones username
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

def bid(bidder_uname, poster_uname, post_title, new_price):
    post = posts.find_one({'username':poster_uname, 'title':post_title})
    
    username = post['username']
    title = post['title']
    content = post['content']
    time_start = post['time_start']
    time_ends = post['time_ends']
    tags = post['tags']
    
    db.posts.update({'username':username, 'title':title},
                    {'username': username,
                     'title': title,
                     'content': content,
                     'price': new_price,
                     'highest_bidder': bidder_uname,
                     'time_start': time_start,
                     'time_ends': time_ends,
                     'tags':tags,
                     })

    return 
##### ^^^^^ POSTS ^^^^^ #####

##### MESSAGING #####
def add_conversation(person1, person2, messages): #wasn't quite sure what fields we want/need
    conversation = {
        'person1' : person1,
        'person2' : person2,
        'messages' : messages,
        }
    return messages.insert(conversation)

def add_message(person1, person2, new_message):
    conversation = messages.find_one({'person1': person1, 'person2': person2})
    p1 = conversation['person1']
    p2 = conversation['person2']
    messages = conversation['messages']
    messages = messages.insert(0, new_message) #adds to the front of the list
    db.messages.update( {
        'person1':p1,
        'person2': p2,
        'messages': messages } )
    return

##### ^^^^^ MESSAGING ^^^^^ #####

##### TESTING #####

#the way the function calls work
#def add_user(username,password,name, bio)
#def add_post(username, title, content, start_price, time_start, time_ends, tags)
#def bid(bidder_uname, poster_uname, post_title, new_price)

print "1"
#add_user('rebecca','rebecca','rebecca','my life')
#add_post('rebecca','testing','testing','$$','early','late')
#update_name('rebecca','rebecca')
#print get_name('rebecca')
print
print
print "2"
#add_post('rebecca','title','content','$','soon','not soon','tags and stuff')
#bid('other_person','rebecca','title','$$')
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
