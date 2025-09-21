from flask import Flask, url_for, get_flashed_messages, flash, redirect, render_template, request, session, abort, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user_model import Base, User
from bs4 import BeautifulSoup
import os
import pandas as pd
from matching import availability_match_ordered
from typing import Dict, List, Tuple

app = Flask(__name__)
app.secret_key = os.urandom(24)

engine = create_engine("sqlite:///users.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
web_session = Session()


@app.route("/")
def default():
    print("bruh")
    return redirect(url_for("login_controller"))


@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    # first check if the user has been logged in from previous visit to this site
    # if so, go to his/her profile page
    # if not, check if the incoming request is via GET request; show the login page
    # if  session.get("username")==True:
    # print("bruh")
    if request.method == "GET":
        print("Login route: GET request: displaying the login page...")
        return render_template("login.html")

    # if the incoming request is via POST request, process the login input
    elif request.method == "POST":
        if request.form.get('action') == 'New Account':
            return redirect(url_for("create_new_account"))
        # checking if the user is in the usersdatabase
        user = web_session.query(User).filter_by(
            Username=request.form["user"]).first()
        if user is not None:
            print("Login route: POST request: User is in the user database")
            # checking if the right password has been entered
            password = web_session.query(User).filter_by(
                Password=request.form["pass"]).first()
            if password is not None:
                print(
                    "Login route: POST request: password matches: adding user in session object")
                # user has successfully logged in, so save his/her info in the session
                # session["Username"] = request.form["user"]
                # redirect the user to his/her profile page
                print(
                    "Login route: POST Request: redirecting to the user profile page...")
                session['Username']=request.form["user"]
                return redirect(url_for("profile", username=request.form["user"]))
            else:
                # wrong password
                # print("Login route: POST Request: wrong password: aborting process...")
                error_message="Wrong password"
                #return redirect(url_for("login_controller"))
                return render_template("login.html",error_message=error_message)
                # abort(401)
        else:
            # wrong username
            # print("Login route: POST request: user is not registered in the database: Aborting process...")
            error_message="Wrong username"
           # return redirect(url_for("login_controller"))
            return render_template("login.html", error_message=error_message)


@app.route("/newaccount/", methods=["GET", "POST"])
def create_new_account():

    if request.method == 'GET':
        return render_template('new_account.html')
    elif request.method == 'POST':
        # return request.form.get("the_Name")
        testUser = web_session.query(User).filter_by(
            Username=request.form["user"]).first()
        if testUser is not None:
            flash('Username is taken')
            return render_template('new_account.html')
        session['Username']=request.form["user"]
        new_User = User(
            Name=request.form["the_Name"], Username=request.form["user"], Password=request.form["pass"])
        try:
            web_session.add(new_User)
            web_session.commit()
            return redirect(url_for("login_controller"))
        except:
            return 'Issue adding task'


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):

    #print("profile method reached")

    if request.method=="GET":
        return render_template("profile.html",username=username)
    elif request.method=="POST": 
        data = request.get_json()  # Get JSON data from the request
        received_value = data.get('value')
    
        # Perform some processing with the received_value

        processed_message = f"Received value: {received_value} at the backend!"
    
        currUser=web_session.query(User).filter_by(Username=username).first()
        currUser.Schedule=received_value
        web_session.commit()
        return jsonify(message=processed_message)  
                
        """rendered_html=render_template("profile.html")
        soup = BeautifulSoup(rendered_html, 'html.parser')
        strArr=[]
        white_Elements=soup.find_all(class_='scheduler-hour')
        currRow=0
        currCol=0
        for element in white_Elements:
            strArr[element.attrs['data-row']].insert(element.attrs['data-col'],0)

        green_Elements=soup.find_all(class_='scheduler-hour scheduler active')
        for element in green_Elements:
            strArr[element.attrs['data-row']].insert(element.attrs['data-col'],1)
        
        # Flatten the 2D array and convert elements to strings
        flattened_and_stringified = [str(item) for sublist in strArr for item in sublist]
        print("bruh", flattened_and_stringified)
        # Join the string elements without any separator
        result_string = "".join(flattened_and_stringified)
        print(result_string)
        currUser=session.query(User).filter_by(
            Username=username).first()
        #currUser.Schedule=result_string

        #Test for editing user field-passed
        #currUser.Schedule="1"
        currUser.Schedule=len(white_Elements)

        session.add(currUser)
        session.commit()
       #data=request.get_json()
        #js_value=data['key_from_js']
        #currUser.Schedule
        #return jsonify(js_value)
        
        serialize=0

        #Get serialized schedule"""
        return render_template("profile.html",username=username)

    # if username has not been specified when calling this function
    if not username:
        # if no profile specified, either:
        # * direct logged in users to their profile
        # * direct unlogged in users to the login page
        if "username" in web_session:
            print(
                "Profile route: user logged in session already: redirecting to profile/username...")
            return redirect(url_for("profile", username=session["Username"]))
        else:
            print(
                "Profile route: user is not in session object: redirect to login page...")
            return redirect(url_for("login_controller"))
    #elif session.query(User).filter_by(Username=username).first() is not None:
        if session.get("Username") == username:
            return render_template("profile.html")
        else:
            print("Profile route: username has been specified in database, but not specified in session object: rendering otherProfile page...")
            return render_template("profile.html")
        # return render_template("profile.html", username = username)
        # if specified, check to handle users looking up their own profile
@app.route('/get_serial')
def get_serial():
    currUser=web_session.query(User).filter_by(Username=session["Username"]).first()
    currSerial={"Schedule": currUser.Schedule}
    return jsonify(currSerial)
@app.route('/process_value', methods=['GET','POST'])
def process_value():
        skills= pd.read_csv('static/csv/hobbies.csv')
        top10skills=skills["HOBBIES"].head(10)
        top10skillscommaseparated=",".join(top10skills.astype(str))
        currUser=web_session.query(User).filter_by(Username=session["Username"]).first()

        if request.method=='GET':
            profile_data={'Possible_Skills': top10skillscommaseparated,'Schedule': currUser.Schedule, 'MySkills': currUser.MySkills, 'MyNeededSkills': currUser.NeededSkills}
            return jsonify(profile_data)
        else:
            data = request.get_json()  # Get JSON data from the request
            schedule = data.get('schedule')
            mySkills=data.get('mySkills')
            myNeededSkills=data.get('myNeededSkills')
    
            # Perform some processing with the received_value

            processed_message = f"Received values: {schedule} and {mySkills} and {myNeededSkills} recieved at the backend!"
        
            check=session["Username"]
            print("check= "+check)
            currUser=web_session.query(User).filter_by(Username=check).first()
            #if currUser is None:
                #currUser.Schedule="3"
            #else:
            currUser.Schedule=schedule
            currUser.MySkills=mySkills
            currUser.NeededSkills=myNeededSkills
            web_session.commit()

            availabilityDict: Dict[str,str]={}
            skillsDict: Dict[str, Dict[str, List[str]]]={}
            teachDict: Dict[str, List[str]]={}
            learnDict: Dict[str, List[str]]={}
            allUsers=web_session.query(User).all()
            for user in allUsers:
                availabilityDict[user.Username]=user.Schedule
                mySkillsArr=user.MySkills.split(",")
                mySkillsList=list(mySkillsArr)
                teachDict[user.Username]=mySkillsList
                neededSkillsArr=user.NeededSkills.split(",")
                neededSkillsList=list(neededSkillsArr)
                learnDict[user.Username]=neededSkillsList
                #skillsDict[user.Username]={teachDict,learnDict}
            matches=availability_match_ordered(availabilityDict,teachDict,learnDict,user.Username)
            #res = sorted(matches, key=lambda x: x[1],reverse=True)
            i=0
            matchInfo={}
            #for match in res:
                #currUserName=match[0]
                #currUser=web_session.query(User).filter_by(Username=currUserName).first()
                #currNameofUser=currUser.Name
                #combo=currNameofUser, currUser.MySkills,currUser.NeededSkills,match[1]
                #matchInfo[i]=combo
                #i=i+1
            session['matches']=matchInfo
            return jsonify({'Status':"success"})
            #return redirect(url_for("show_matches"), code=307)
@app.route('/show_matches')
def show_matches():
    return render_template("matches.html",matches=session['matches'])
if __name__ == "__main__":
    #app.run(debug=True)
    app.run(port=5000,debug=False)
