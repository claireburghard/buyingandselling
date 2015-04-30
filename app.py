from flask import Flask, flash,  render_template, request, redirect, url_for, session, escape


app = Flask(__name__)
app.secret_key = 'secret'

@app.route("/", methods=['GET','POST'])
@app.route("/index", methods=['GET','POST'])
def index():
    message = ""
    if request.method=="GET":
        return render_template("index.html", message=message)
    else:
        return render_template("index.html", message=message)

@app.route("/signup",methods=['GET','POST'])
def signup():
    message = ""
    if request.method=="GET":
        return render_template("signup.html", message=message)
    else:
        return render_template("signup.html", message=message)
    
if __name__=="__main__":
    app.debug=True
    app.run()
