from flask import Flask, flash,  render_template, request, redirect, url_for, session, escape

import mongo

app = Flask(__name__)
app.secret_key = 'secret'

@app.route("/", methods=['GET','POST'])
@app.route("/index", methods=['GET','POST'])
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        message = ""
        if request.method=="GET":
            return render_template("index.html", message=message)
        else:
            if request.form['b']=="Log In":
                username = request.form["logusername"]
                password = request.form["logpassword"]
                confirmation = mongo.authenticate(username,password)
                if confirmation != "match":
                    message = confirmation
                    return render_template("index.html", message=message)
                if confirmation == "match":
                    session['username'] = username
                    return redirect(url_for('home'))
            if request.form['b']=="Sign Up":
                username = request.form["signusername"]
                password = request.form["signpassword"]
                password2 = request.form["signpassword2"]
                name = request.form["name"]
                if mongo.user_exists(username) == "exists":
                    message = "Someone already has this username. Please use a different one." 
                    return render_template("index.html", message=message)
                else:
                    if password == password2:
                        mongo.add_user(username,password,name)
                        message = "Registration Sucessful! Log In to get started." 
                        return render_template("index.html", message=message)
                    else:
                        message = "Please make sure your passwords match"
                        return render_template("index.html", message=message)
            if request.form['b']=="Cancel":
                return render_template("index.html", message=message)




@app.route("/signup",methods=['GET','POST'])
def signup():
    message = ""
    if request.method=="GET":
        return render_template("signup.html", message=message)
    else:
        return render_template("signup.html", message=message)

@app.route("/home",methods=['GET','POST'])
def home():
    if 'username' in session:
        message = ""
        if request.method=="GET":
            return render_template('home.html', message=message)
        else:
            print "logout"
            if request.form['b']=="Logout":
                print "logout"
                return redirect(url_for('logout'))
            if request.form['b']=="Submit":
                pass
    else:
        return redirect(url_for('index'))


@app.route("/profile",methods=['GET','POST'])
def profile():
    if 'username' in session:
        if request.method=="GET":
            return render_template('profile.html')
        else:
            return render_template('profile.html')
    else:
        return redirect(url_for('index'))

@app.route("/market",methods=['GET','POST'])
def market():
    if 'username' in session:
        if request.method=="GET":
            return render_template('market.html')
        else:
            return render_template('market.html')
    else:
        return redirect(url_for('index'))


@app.route("/myitems",methods=['GET','POST'])
def myitems():
    if 'username' in session:
        if request.method=="GET":
            return render_template('myitems.html')
        else:
            return render_template('myitems.html')

@app.route("/myactivity",methods=['GET','POST'])
def myactivity():
    if 'username' in session:
        if request.method=="GET":
            return render_template('myactivity.html')
        else:
            return render_template('myactivity.html')
    else:
        return redirect(url_for('index'))

@app.route("/messages",methods=['GET','POST'])
def messages():
    if 'username' in session:
        if request.method=="GET":
            return render_template('messages.html')
        else:
            return render_template('messages.html')
    else:
        return redirect(url_for('index'))

    
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

if __name__=="__main__":
    app.debug=True
    app.run()
