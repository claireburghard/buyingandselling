from flask import Flask, flash,  render_template, request, redirect, url_for, session, escape

import mongo

app = Flask(__name__)
app.secret_key = 'secret'


@app.route("/", methods=['GET','POST'])
@app.route("/index", methods=['GET','POST'])
def index():
    message = ""
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return render_template("index.html", message=message)


@app.route("/login", methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        message = ""
        if request.method=="GET":
            return render_template("login.html", message = message)
        else:
            if request.form['b']=="Log In":
                username = request.form["logusername"]
                password = request.form["logpassword"]
                confirmation = mongo.authenticate(username,password)
                if confirmation != "match":
                    message = confirmation
                    return render_template("login.html", message = message)
                if confirmation == "match":
                    session['username'] = username
                    return redirect(url_for('home'))
            if request.form['b']=="Cancel":
                return redirect(url_for('index'))

@app.route("/register",methods=['GET','POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        message = ""
        if request.method=="GET":
            return render_template("register.html", message = message)
        else:
            if request.form['b']=="Register":
                username = request.form["regusername"]
                password = request.form["regpassword"]
                password2 = request.form["regpassword2"]
                if mongo.user_exists(username) == "exists":
                    message = "Someone already has this username. Please use a different one."
                    return render_template("register.html", message = message)
                else:
                    if password == password2:
                        mongo.add_user(username, password)
                        session['username']=username
                        return  redirect(url_for('signup'))
                    else:
                        message = "Please make sure your passwords match."
                        return render_template("register.html", message = message)
            if request.form['b']=="Cancel":
                return redirect(url_for('index'))

@app.route("/home",methods=['GET','POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        message = ""
        name = session['username']
        if request.method=="GET":
            return render_template('home.html', message = message, name = name)
        else:
            if request.form['b']=="Logout":
                return redirect(url_for('logout'))


@app.route("/signup", methods=['GET','POST'])
def signup():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        if request.method=="GET":
            username = session['username']
            return render_template('signup.html',username=username)
        else:
            if request.form['b']=="Submit":
                username = session['username']
                if request.form['name']!="":
                    name = request.form['name']
                else:
                    name = mongo.get_name(username)
                if request.form['picture']!="":
                    picture = request.form['picture']
                else:
                    picture = mongo.get_profilepicture(username)
                if request.form['bio']!="":
                    bio = request.form['bio']
                else:
                    bio = mongo.get_bio(username)
                if request.form['contactinfo']!="":
                    contactinfo = request.form['contactinfo']
                else:
                    contactinfo = mongo.get_contactinfo(username)
                pword = mongo.get_password(username)
                mongo.update_profile(username,name,picture,pword,newbio,contactinfo)
                return redirect(url_for('home'))


@app.route("/profile/<user>",methods=['GET','POST'])
def profile(user):
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        if request.method=="GET":
            name = mongo.get_name(user)
            #password = mongo.get_password(username)
            bio = mongo.get_bio(user)
            profilepicture = mongo.get_profilepicture(user)
            contactinfo = mongo.get_contactinfo(user)
            return render_template('profile.html',
                                   username = user,
                                   name = name,
                                   bio=bio,
                                   profilepicture=profilepicture,
                                   contactinfo=contactinfo)
        else:
            if request.form['b']=="Edit Profile":
                return redirect(url_for('editprofile'))
            if request.form['b']=="Logout":
                return redirect(url_for('logout'))

@app.route("/editprofile",methods=['GET','POST'])
def editprofile():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        if request.method=="GET":
            username = session['username']
            name = mongo.get_name(username)
            password = mongo.get_password(username)
            bio = mongo.get_bio(username)
            profilepicture = mongo.get_profilepicture(username)
            return render_template('editprofile.html',
                                   username=username,
                                   name=name,
                                   password=password,
                                   profilepicture=profilepicture,
                                   bio=bio)
        else:
            if request.form['b']=="Submit":
                username = session['username']
                if request.form['newname']!="":
                    newname = request.form['newname']
                else:
                    newname = mongo.get_name(username)
                if request.form['newpicture']!="":
                    newpicture = request.form['newpicture']
                else:
                    newpicture = mongo.get_profilepicture(username)
                if request.form['newpassword']!="":
                    newpassword = request.form['newpassword']
                else:
                    newpassword = mongo.get_password(username)
                if request.form['newbio']!="":
                    newbio = request.form['newbio']
                else:
                    newbio = mongo.get_bio(username)
                if request.form['newcontactinfo']!="":
                    newcontactinfo = request.form['newcontactinfo']
                else:
                    newcontactinfo = mongo.get_contactinfo(username)
                mongo.update_profile(username,newname,newpicture,
                                     newpassword,newbio,newcontactinfo)
                return redirect(url_for('profile'))
                

@app.route("/market",methods=['GET','POST'])
def market():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
       if request.method=="GET":
           return render_template('market.html', posts = mongo.get_all_posts())
       else:
           if request.form['b']=="Logout":
               return redirect(url_for('logout'))

@app.route("/viewpost/<postid>",methods=['GET','POST'])
def viewpost(postid):
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        message = ""
        post = mongo.find_post(postid)[0]
        if request.method=="GET":
            return render_template('viewpost.html',message = message, post = post)
        else:
            if request.form['b']=="Logout":
               return redirect(url_for('logout'))
            if request.form['b']=="Submit":
                post = mongo.find_post(postid)[0]
                new_bid = request.form['bid']
                user = session['username']
                if float(new_bid) == 0.0:
                    return render_template('viewpost.html',message = "Please input an actual number", post=post)
                elif float(new_bid) < float(post['price']):
                    return render_template('viewpost.html',message = "Your bid must be higher than previous bid",post=post)
                else:
                    mongo.bid(new_bid,user,postid)
                    return redirect(url_for('viewpost',postid=postid))

@app.route("/myitems",methods=['GET','POST'])
def myitems():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        message = ""
        if request.method=="GET":
            return render_template('myitems.html',message=message, myitems = mongo.get_posts( session["username"] ))
        else:
            if request.form['b']=="Logout":
                return redirect(url_for('logout'))



@app.route("/newpost",methods=['GET','POST'])
def newpost():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        message = ""
        if request.method=="GET":
            return render_template('newpost.html', message = message)
        else:
            if request.form['b']=="Logout":
                return redirect(url_for('logout'))
            if request.form['b']=="Submit":
                user = session['username']
                title = request.form['title']
                content = request.form['content']
                picture = request.form ['picture']
                start_price = request.form['start_price']
                time_start = request.form['time_start']
                time_ends = request.form['time_ends']
                tags = request.form['tags']
                if (title == "" or content == "" or picture=="" or start_price == "" or 
                    time_start == "" or time_ends == "" or tags == ""):
                    return render_template("newpost.html", message = "Please fill in all fields correctly.")
                mongo.add_post(user, title, content, picture, start_price, time_start, time_ends, tags)
                posts = mongo.get_posts(user)
                return redirect(url_for('myitems'))


@app.route("/messages",methods=['GET','POST'])
def messages():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        msgs = mongo.get_conversations(session['username'])
        if request.method=="GET":
            return render_template('messages.html',currentuser=session['username'], messages = msgs)
        else:
            if request.form['b']=="Logout":
                return redirect(url_for('logout'))

@app.route("/viewmessage/<otheruser>", methods=['GET','POST'])
def viewmessage(otheruser):
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        if request.method=="GET":
            return render_template('viewmessage.html',
                                   otheruser=otheruser,
                                   currentuser=session['username'],
                                   messlog=mongo.get_messages(session['username'],otheruser))
        else:
            if request.form['b']=="Logout":
                return redirect(url_for('logout'))
            if request.form['b']=="Submit":
                response = request.form['response']
                record = {'user':session['username'],'mess':response}
                if response == "":
                    render_template('viewmessage.html',
                                   otheruser=otheruser,
                                   currentuser=session['username'],
                                   messlog=mongo.get_messages(session['username'],otheruser))
                mongo.add_message(session['username'],otheruser,record)
                return redirect(url_for('viewmessage', otheruser=otheruser))
                

@app.route("/newmessage",methods=['GET','POST'])
def newmessage():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        message = ""
        if request.method=="GET":
            return render_template('newmessage.html', message = message)
        else:
            if request.form['b']=="Logout":
                return redirect(url_for('logout'))
            if request.form['b']=="Submit":
                user = session['username']
                op = request.form['op']
                content = request.form['content']
                if (op == "" or content == ""):
                    return render_template("newmessage.html", message = "Please fill in all fields correctly.")
                elif mongo.user_exists(op) == "does not exist":
                     return render_template("newmessage.html", message = "That user does not exist.")
                else:
                    message_list=[]
                    message_list.append({'user':session['username'],'mess':content})
                    mongo.add_conversation(user, op, message_list)
                    return redirect(url_for('viewmessage', otheruser=op))
        
    
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

if __name__=="__main__":
    app.debug=True
    app.run()
