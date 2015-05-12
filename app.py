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
            return render_template("login.html", message=message)
        else:
            username = request.form["logusername"]
            password = request.form["logpassword"]
            confirmation = mongo.authenticate(username,password)
            if confirmation != "match":
                message = confirmation
                return render_template("login.html", message=message)
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
            return render_template("register.html", message=message)
        else:
            username = request.form["regusername"]
            password = request.form["regpassword"]
            password2 = request.form["regpassword2"]
            name = request.form["name"]
            if mongo.user_exists(username) == "exists":
                message = "Someone already has this username. Please use a different one."
                return render_template("register.html", message=message)
            else:
                if password == password2:
                    mongo.add_user(username,password,name)
                    message = "Registration sucessful! Log in to get started."
                    return  redirect(url_for('signup'))
                else:
                    message = "Please make sure your passwords match."
                    return render_template("register.html", message=message)


@app.route("/home",methods=['GET','POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        message = ""
        if request.method=="GET":
            return render_template('home.html', message=message)
        else:
            if request.form['b']=="Logout":
                print "logout"
                return redirect(url_for('logout'))
            if request.form['b']=="Submit":
                title = request.form['title']
                content = request.form['content']
                price = request.form['price']
                user = session['username']
                mongo.add_post(user, title, content, price)
                posts = mongo.get_posts(user)
                return render_template('home.html', message=posts)


@app.route("/signup", methods=['GET','POST'])
def signup():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        return render_template('signup.html')


@app.route("/profile",methods=['GET','POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        if request.method=="GET":
            return render_template('profile.html')
        else:
            if request.form['b']=="Logout":
                print "logout"
                return redirect(url_for('logout'))


@app.route("/market",methods=['GET','POST'])
def market():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        if request.method=="GET":
            return render_template('market.html')
        else:
            if request.form['b']=="Logout":
                print "logout"
                return redirect(url_for('logout'))


@app.route("/myitems",methods=['GET','POST'])
def myitems():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        if request.method=="GET":
            return render_template('myitems.html')
        else:
            if request.form['b']=="Logout":
                print "logout"
                return redirect(url_for('logout'))
    
    
@app.route("/myactivity",methods=['GET','POST'])
def myactivity():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        if request.method=="GET":
            return render_template('myactivity.html')
        else:
            if request.form['b']=="Logout":
                print "logout"
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
                print "logout"
                return redirect(url_for('logout'))


    
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

if __name__=="__main__":
    app.debug=True
    app.run()
