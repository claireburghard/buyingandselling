import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('localhost', 27017)
db = client.proj
users = db.users
posts = db.posts
messages = db.messages

##### USER #####
def add_user(username, password):
    user = {
        'username' : username,
        'password' : password,
        'name' : "",
        'bio' : "",
        'contactinfo' : "",
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

def get_contactinfo(username):
    user = users.find_one({'username':username})
    if user == None:
        return "User not found"
    contactinfo = user['contactinfo']
    return contactinfo

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


def update_profile(username, new_name, newpicture, newpassword,newbio,newcontactinfo):
    user = users.find_one({'username':username})
    rating = user['rating']
    ratings = user['ratings']
    db.users.update( {'username': username}, {
        'username': username,
        'name' : new_name,
        'password' : newpassword,
        'bio' : newbio,
        'rating' : rating,
        'ratings' : ratings,
        'profilepicture' : newpicture,
        'contactinfo': newcontactinfo} )
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
def add_post(username, title, content, picture, start_price, time_start, time_ends, tags):
    tgs = tags.lower()
    tgs_array = tgs.split(",")
    post = {
        'username' : username,
        'title': title,
        'content' : content,
        'picture':picture,
        'tags': tgs,
        #price attribute will keep changing based on what the highest bid is
        'price' : start_price,
        'highest_bidder' : None, #this will be someones username
        'time_start' : time_start,
        'time_ends' : time_ends,
        'tags_array':tgs_array
    }
    return posts.insert(post)

def get_posts(username):
    posts_list = []
    posts_data = posts.find({'username':username})
    if posts_data == None:
        return []
    else:
        for post in posts_data:
            temp_post = []
            temp_post.append(post['_id'])
            temp_post.append(post['username'])
            temp_post.append(post['title'])
            temp_post.append(post['picture'])
            temp_post.append(post['time_start'])
            temp_post.append(post['time_ends'])
            temp_post.append(post['price'])
            temp_post.append(post['tags'])
            posts_list.append(temp_post)
        return posts_list

def find_post(post_id):
    data = []
    post_data = list(posts.find({'_id':ObjectId(post_id)}))
    if post_data == None:
        return []
    else:
        return post_data

def get_all_posts():
    posts_list = []
    posts_data = posts.find()
    if posts_data == None:
        return []
    else:
        for post in posts_data:
            temp_post = []
            temp_post.append(post['_id'])
            temp_post.append(post['username'])
            temp_post.append(post['title'])
            temp_post.append(post['picture'])
            temp_post.append(post['time_start'])
            temp_post.append(post['time_ends'])
            temp_post.append(post['price'])
            temp_post.append(post['tags'])
            posts_list.append(temp_post)
        return posts_list

def bid(bid, bidder, post_id):
    post = posts.find_one({'_id':ObjectId(post_id)})
    username = post['username']
    title = post['title']
    content = post['content']
    picture = post['picture']
    time_start = post['time_start']
    time_ends = post['time_ends']
    tags = post['tags']
    tags_array = post['tags_array']
    db.posts.update({'username':username,'title':title},
                    {'username': username,
                     'title': title,
                     'content': content,
                     'price': bid,
                     'picture':picture,
                     'highest_bidder': bidder,
                     'time_start': time_start,
                     'time_ends': time_ends,
                     'tags':tags,
                     'tags_array':tags_array
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
    p1 = conversation['person1']
    p2 = conversation['person2']
    mess = conversation['messages']
    new_mess = [new_message] + mess
    db.messages.update( {'person1':p1, 'person2':p2}, {
        'person1':p1,
        'person2': p2,
        'messages': new_mess } )
    return

def get_messages(curruser,op):
    messages_list=[]
    conversation = messages.find_one({'person1': curruser, 'person2': op})
    if conversation == None:
        conversation = messages.find_one({'person1': op, 'person2': curruser})
    messages_list = conversation['messages']
    return messages_list


def get_conversations(username):
    messages_list=[]
    for message in messages.find({'person1':username}):
        temp_message = []
        temp_message.append(message['person1'])
        temp_message.append(message['person2'])
        temp_message.append(message['messages'])
        messages_list.append(temp_message)
    for message in messages.find({'person2':username}):
        temp_message = []
        temp_message.append(message['person1'])
        temp_message.append(message['person2'])
        temp_message.append(message['messages'])
        messages_list.append(temp_message)
    return messages_list

##### ^^^^^ MESSAGING ^^^^^ #####

##### TESTING #####

#the way the function calls work
#def add_user(username,password,name, bio)
#def add_post(username, title, content, start_price, time_start, time_ends, tags)
#def bid(bidder_uname, poster_uname, post_title, new_price)
#def add_conversation(person1, person2, messages)
#def add_message(person1, person2, new_message)
#def update_name(username, new_name)
#db.users.remove()
#db.posts.remove()
#db.messages.remove()
#print db.users
#print db.posts
