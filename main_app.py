import os
from flask import *
import requests

app = Flask(__name__)
app.secret_key= os.urandom(123)



@app.route("/",methods=["GET","POST"])
def loginpage():
    error=""
    if request.method=="POST":
        session['user'] = request.form["loginid"]
        pswrd = request.form["password"]
        verify= requests.get('https://api.github.com/user', auth=(session['user'],pswrd))
        if(verify.status_code==200):
            return redirect(url_for("analysepage"))
        else:
            error="Invalid Credentials"
            return render_template("login.html",error=error)
    return render_template("login.html",error=error)

@app.route("/analysepage")
def analysepage():
    count=1
    namelist=[]
    forklist=[]
    watcherlist=[]
    starlist=[]
    sizelist=[]
    if "user" in session:
        user= session['user']
        x1= requests.get('https://api.github.com/users/'+session['user'])
        y1= x1.json()
        n = y1["name"]
        img = y1["avatar_url"]
        bio= y1["bio"]
        x2= requests.get('https://api.github.com/users/'+session['user']+'/followers')
        y2= x2.json()
        z2= len(y2)
        x3 = requests.get('https://api.github.com/users/' + session['user'] + '/following')
        y3 = x3.json()
        z3 = len(y3)
        info= requests.get('https://api.github.com/users/'+session['user']+'/repos')
        info1= info.json()
        for i in info1:
            count=count+1
            namelist.append(i["name"])
            forklist.append(i["forks"])
            watcherlist.append(i["watchers"])
            starlist.append(i["stargazers_count"])
            sizelist.append(i["size"])
        return render_template("analyse.html",n=n,z2=z2,z3=z3,namelist=namelist,forklist=forklist,watcherlist=watcherlist,
                               starlist=starlist,sizelist=sizelist,count=count,img=img,bio=bio)
    else:
        return redirect(url_for("loginpage"))

@app.route("/graph")
def graph():
    if "user" in session:
        namelist=[]
        watcherlist=[]
        info = requests.get('https://api.github.com/users/' + session['user'] + '/repos')
        info1 = info.json()
        for i in info1:
            namelist.append(i["name"])
            watcherlist.append(i["watchers"])
        return render_template("graph.html",namelist=namelist,watcherlist=watcherlist)
    else:
        return redirect(url_for("loginpage"))

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user",None)
        return redirect(url_for("loginpage"))
    else:
        return "<p>You are already logged out</p>"

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")

if __name__=="__main__":
    app.run(debug=True)