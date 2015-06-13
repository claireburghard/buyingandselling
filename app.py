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
            username = request.form["logusername"]
            password = request.form["logpassword"]
            confirmation = mongo.authenticate(username,password)
            if confirmation != "match":
                message = confirmation
                return render_template("login.html", message = message)
            if confirmation == "match":
                session['username'] = username
                return redirect(url_for('home'))


@app.route("/register",methods=['GET','POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        message = ""
        if request.method=="GET":
            return render_template("register.html", message = message)
        else:
            username = request.form["regusername"]
            password = request.form["regpassword"]
            password2 = request.form["regpassword2"]
            bio = request.form['bio']
            name = request.form["name"]
            if mongo.user_exists(username) == "exists":
                message = "Someone already has this username. Please use a different one."
                return render_template("register.html", message = message)
            else:
                if password == password2:
                    mongo.add_user(username, password, name, bio)
                    message = "Registration sucessful! Log in to get started."
                    return  redirect(url_for('signup'))
                else:
                    message = "Please make sure your passwords match."
                    return render_template("register.html", message = message)


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
            return render_template('signup.html')


@app.route("/profile",methods=['GET','POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        name = session['username']
        if request.method=="GET":
            username = session['username']
            name = mongo.get_name(username)
            #password = mongo.get_password(username)
            bio = mongo.get_bio(username)
            profilepicture = mongo.get_profilepicture(username)
            return render_template('profile.html',
                                   username=username,
                                   name = name,
                                   bio=bio,
                                   profilepicture=profilepicture)
        else:
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
                newname = request.form['newname']
                newpicture = request.form['newpicture']
                newpassword = request.form['newpassword']
                newbio = request.form['newbio']
                mongo.update_name(username,newname)
                mongo.update_profilepicture(username,newpicture)
                mongo.update_password(username,newpassword)
                mongo.update_bio(username,newbio)
                return redirect(url_for('profile'))
                

@app.route("/market",methods=['GET','POST'])
def market():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
       if request.method=="GET":
           return render_template('market.html')
       else:
           if request.form['b']=="Logout":
               return redirect(url_for('logout'))

@app.route("/myitems",methods=['GET','POST'])
def myitems():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        message = ""
        if request.method=="GET":
            return render_template('myitems.html', message = message)
        else:
            if request.form['b']=="Logout":
                return redirect(url_for('logout'))
            if request.form['b']=="Submit":
                user = session['username']
                title = request.form['title']
                content = request.form['content']
                start_price = request.form['start_price']
                time_start = request.form['time_start']
                time_ends = request.form['time_ends']
                tags = request.form['tags']
                if (title == "" or content == "" or start_price == "" or 
                    time_start == "" or time_ends == "" or tags == ""):
                    return render_template("myitems.html", message = "Please fill in all fields correctly.")
                mongo.add_post(user, title, content, start_price, time_start, time_ends, tags)
                posts = mongo.get_posts(user)
                return render_template('myitems.html', message=posts)


@app.route("/myactivity",methods=['GET','POST'])
def myactivity():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        if request.method=="GET":
            return render_template('myactivity.html')
        else:
            if request.form['b']=="Logout":
                return redirect(url_for('logout'))


@app.route("/messages",methods=['GET','POST'])
def messages():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        if request.method=="GET":
            return render_template('messages.html')
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
                                   currentuser=session['username'])
        else:
            if request.form['b']=="Logout":
                return redirect(url_for('logout'))
        
    
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

if __name__=="__main__":
    app.debug=True
    app.run()
