from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.proj
users = db.users
posts = db.posts
messages = db.messages

##### USER #####
def add_user( username, password, name, bio ):
    user = {
        'username' : username,
        'password' : password,
        'name' : name,
        'bio' : bio,
        'rating' : 4,
        'ratings' : 2,
        'profilepicture' : "http://cliparts.co/cliparts/qTB/6x8/qTB6x8zT5.svg"
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


def get_rating(username):
    user = users.find_one({'username':username})
    if user == None:
        return "User not found"
    rating = user['rating']
    return rating

def get_profilepicture(username):
    user = users.find_one({'username':username})
    if user == None:
        return "User not found"
    profilepicture = user['profilepicture']
    return profilepicture


def update_name(username, new_name):
    user = users.find_one({'username':username})
    uname = user['username']
    #name = user['name']
    password = user['password']
    bio = user['bio']
    rating = user['rating']
    ratings = user['ratings']
    profilepicture = user['profilepicture']
    db.users.update( {'username': username}, {
        'username': username,
        'name' : new_name,
        'password' : password,
        'bio' : bio,
        'rating' : rating,
        'ratings' : ratings,
        'profilepicture' : profilepicture} )
    return


def update_password(username, new_pass):
    user = users.find_one({'username':username})
    uname = user['username']
    name = user['name']
    #password = user['password']
    bio = user['bio']
    rating = user['rating']
    ratings = user['ratings']
    profilepicture = user['profilepicture']
    db.users.update( {'username': username}, {
        'username': username,
        'name' : name,
        'password' : new_pass,
        'bio' : bio,
        'rating' : rating,
        'ratings' : ratings,
        'profilepicture' : profilepicture} )
    return

def update_bio(username, new_bio):
    user = users.find_one({'username':username})
    uname = user['username']
    name = user['name']
    password = user['password']
    #bio = user['bio']
    rating = user['rating']
    ratings = user['ratings']
    profilepicture = user['profilepicture']
    db.users.update( {'username': username}, {
        'username': username,
        'name' : name,
        'password': password,
        'bio' : new_bio,
        'rating' : rating,
        'ratings' : ratings,
        'profilepicture' : profilepicture} )
    return

def update_profilepicture(username, new_profilepicture):
    user = users.find_one({'username':username})
    uname = user['username']
    name = user['name']
    password = user['password']
    bio = user['bio']
    rating = user['rating']
    ratings = user['ratings']
    #profilepicture = user['profilepicture']
    db.users.update( {'username': username}, {
        'username': username,
        'name' : name,
        'password': password,
        'bio' : bio,
        'rating' : rating,
        'ratings' : ratings,
        'profilepicture' : new_profilepicture} )
    return

def rate(username, new_rating):
    user = users.find_one({'username':username})
    
    uname = user['username']
    name = user['name']
    password = user['password']
    bio = user['bio']
    rating = user['rating']
    ratings = user['ratings']
    print ratings + 1
    
    '''if rating == 0: #never been rated before
        db.users.update( {'username': username}, {
            'username': username,
            'name' : name,
            'password': password,
            'bio' : bio,
            'rating' : new_rating,
            'ratings' : ratings + 1} )
        return'''

    total = rating * ratings
    print total
    total = total + new_rating
    print total
    new_num = ratings + 1
    print new_num
    av = total/new_num
    print av
    '''db.users.update( {'username': username}, {
        'username': username,
        'name' : name,
        'password': password,
        'bio' : bio
        'rating' : new_rating} )'''
    return

##### ^^^^^ USER ^^^^^ #####

##### POSTS #####
def add_post(username, title, content, start_price, time_start, time_ends, tags):
    tgs = tags.lower()
    tgs_array = tgs.split(",")
    post = {
        'username' : username,
        'title': title,
        'content' : content,
        'tags': tgs,
        #price attribute will keep changing based on what the highest bid is
        'price' : start_price,
        'highest_bidder' : None, #this will be someones username
        'time_start' : time_start,
        'time_ends' : time_ends,
        'tags_array':tgs_array
    }
    #print post
    return posts.insert(post)

def get_posts(username):
    counter = 0
    for post in posts.find({'username':username}):
        counter = counter + 1
        username = post['username']
        title = post['title']
        content = post['content']
        time_start = post['time_start']
        time_ends = post['time_ends']
        tags = post['tags']
        price = post['price']
    post_string = "username: " + username + "\n" + "title: " + title + "\n" + "content: " + content + "\n" + "start time: " + time_start + "\n" + "end time: " + time_ends + "\n" + "price: " + price + "\n" + "tags: " + tags
    return post_string

def bid(bidder_uname, poster_uname, post_title, new_price):
    post = posts.find_one({'username':poster_uname, 'title':post_title})
    
    username = post['username']
    title = post['title']
    content = post['content']
    time_start = post['time_start']
    time_ends = post['time_ends']
    tags = post['tags_string']
    price = post['price']

    if new_price <= price:
        return "new price must be higher than old price"
    
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

def get_following_posts(username):
    ##finds all of the posts that a user is associated with and prints them
    bidded_posts = posts.find({'highest_bidder':username})
    print bidded_posts
    return bidded_posts

##### ^^^^^ POSTS ^^^^^ #####

##### MESSAGING #####
def add_conversation(person1, person2, messages): #wasn't quite sure what fields we want/need
    conversation = {
        'person1' : person1,
        'person2' : person2,
        'messages' : messages,
        }
    return db.messages.insert(conversation)

def add_message(person1, person2, new_message):
    conversation = messages.find_one({'person1': person1, 'person2': person2})
    if conversation == None:
        #checks to see if the names are in a different order
        conversation = messages.find_one({'person1': person2, 'person2': person1})
    if conversation == None:
        return "users not found"
    print conversation
    p1 = conversation['person1']
    p2 = conversation['person2']
    mess = conversation['messages']
    print mess
    #mess = mess.insert(0, new_message) #adds to the front of the list
    db.messages.update( {'person1':p1, 'person2':p2}, {
        'person1':p1,
        'person2': p2,
        'messages': mess } )
    return

def get_messages(person1, person2):
    conversation = messages.find_one({'person1':person1, 'person2':person2})
    print 1
    print conversation
    
    if conversation == None:
        conversation = messages.find_one({'person1':person2, 'person2':person1})
    if conversation == None:
         return "users not found"

    print 2
    print conversation
    mess = conversation['messages']
    return mess

##### ^^^^^ MESSAGING ^^^^^ #####

##### TESTING #####

get_following_posts("claire")

#the way the function calls work
#def add_user(username,password,name, bio)
#def add_post(username, title, content, start_price, time_start, time_ends, tags)
#def bid(bidder_uname, poster_uname, post_title, new_price)
#def add_conversation(person1, person2, messages)
#def add_message(person1, person2, new_message)
#def update_name(username, new_name)
#db.users.remove()
#db.posts.remove()
#print db.users
#print db.posts
#db.messages.remove()
