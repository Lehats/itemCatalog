#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from sqlalchemy import create_engine, asc, exists, desc
from sqlalchemy.orm import sessionmaker
from setupDb import Base, Parts, Categories, Users
from flask import session as login_session
import random, string, json, requests, httplib2
from google.oauth2 import id_token
from google.auth.transport import requests

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)

#### DATABASE connection ######****************
# Connect to db and create db engine
engine = create_engine('sqlite:///parts.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBsession()
    

#########************ Authentification pages *****************#####################

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    session.close()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    #return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Login Page with from for log in and sign up
@app.route('/existingUser', methods = ['GET', 'POST'])
def logIn():
    session.close()
    if request.args.get('state') != login_session.get('state'):
        return "invalid state parameter"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session.query(Users).filter_by(username = username).first()
        if user and user.verify_password(password):
            login_session['username'] = username
            session.close()
            return redirect(url_for('getMainPage'))
        else:
            session.close()
            return redirect(url_for('showLogin'))

    return render_template('login.html')

@app.route('/googleConnect', methods = ['POST'])
def googelConnect():
    session.close()
    # checks for state parameter
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # get the token from the onSignIn of the html file
    token = request.data

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "117697598600-cqmrdclt6di094ff3s6j5moj0sq38d4h.apps.googleusercontent.com")
        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
    except ValueError:
        # Invalid token
        pass
    url = ('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s' % token)
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    # result includes the following.
    '''
    {
    // These six fields are included in all Google ID Tokens.
    "iss": "https://accounts.google.com",
    "sub": "110169484474386276334",
    "azp": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
    "aud": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
    "iat": "1433978353",
    "exp": "1433981953",

    // These seven fields are only included when the user has granted the "profile" and
    // "email" OAuth scopes to the application.
    "email": "testuser@gmail.com",
    "email_verified": "true",
    "name" : "Test User",
    "picture": "https://lh4.googleusercontent.com/-kYgzyAWpZzJ/ABCDEFGHI/AAAJKLMNOP/tIXL9Ir44LE/s99-c/photo.jpg",
    "given_name": "Test",
    "family_name": "User",
    "locale": "en"
    }
    '''
    # check if user exists
    username = result['name']
    username = username.replace(" ","")
    user = session.query(Users).filter_by(username=username).first()
    # if not..
    if not user:
        userToAdd = Users(username=username)
        userToAdd.hashThePassword(result['name'])
        session.add(userToAdd)
        session.commit()
        login_session['username'] = username
        print "neuuser"
        session.close()
        return "bla" 
    # if so..
    else:
        login_session['username'] = username
        print "existuser"
        session.close()
        return "bla"  
    
# create new user
@app.route('/newUser', methods=['POST','GET'])
def createUser():
    session.close()
    if request.args.get('state') != login_session.get('state'):
        session.close()
        return "invalid state parameter"
    if ( request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        user = session.query(Users).filter_by(username = username).first()
        session.close()
        if user: 
            return redirect(url_for('showLogin')) 
        else:
            addUser = Users(username = username)
            addUser.hashThePassword(password)
            session.add(addUser)
            session.commit()
            session.close()
            login_session['username'] = username 
    return redirect(url_for('getMainPage'))

# log out
@app.route('/logout')
def logOut():
    session.close()
    del login_session['username']
    return redirect(url_for('getMainPage'))


#########**************** Resource pages ***********************#########

# Main page --  shows all categories and recently added items
@app.route('/')
def getMainPage():
    session.close()
    latestParts = session.query(Parts).order_by(Parts.id.desc()).limit(10)
    categories = session.query(Categories).group_by(Categories.name)
    if 'username' not in login_session:
        return render_template('main.html', categories = categories, latestParts = latestParts)
    return render_template('mainPrivate.html', categories = categories, latestParts = latestParts, user = login_session['username'] )
    

# new part page --shows form to set up a new part
@app.route('/newpart', methods=['GET', 'POST'])
def createNewPart():
    session.close()
    categories = session.query(Categories).group_by(Categories.name)
    user = login_session['username']
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        partName = request.form['partName']
        partDescription = request.form['partDescription']
        partCategoryName = request.form['partCategory']
        partCategory = session.query(Categories).filter_by(name=partCategoryName).first()
        partCreator = session.query(Users).filter_by(username = user).first()
        partToAdd = Parts(name=partName, description = partDescription, category_id = partCategory.id, user_id = partCreator.id)
        session.add(partToAdd)
        session.commit()
        return redirect(url_for('getMainPage'))
    return render_template('newPart.html', categories = categories, user = user )

# category page --  shows all parts of the specific category
@app.route('/<int:category_id>')
def getCategory(category_id):
    session.close()
    categories = session.query(Categories).group_by(Categories.name)
    requestedCategory = session.query(Categories).filter_by(id=category_id).first()
    partsOfrequestedCategory = session.query(Parts).filter_by(category_id = requestedCategory.id)
    if 'username' not in login_session:
        return render_template('category.html',categories = categories, category = requestedCategory, parts=partsOfrequestedCategory)
    return render_template('categoryPrivate.html',categories = categories, category = requestedCategory, parts=partsOfrequestedCategory,user = login_session['username'])

# part page --shows all info of the specific part
@app.route('/<int:category_id>/<int:part_id>')
def getPart(category_id, part_id):
    session.close()
    requestedPart = session.query(Parts).filter_by(id=part_id).first()  
    if 'username' in login_session:
        user = login_session['username']
        return render_template('partPrivate.html', part = requestedPart, user = user)  
    return render_template('part.html', part = requestedPart)

# part edit page --shows form to edit a part
@app.route('/<int:category_id>/<int:part_id>/edit', methods=['GET', 'POST'] )
def editPart(category_id, part_id):
    session.close()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    partToedit = session.query(Parts).filter_by(id=part_id).first()
    user = session.query(Users).filter_by(id=partToedit.user_id).first()
    if user.username != login_session.get('username'):
        return redirect(url_for('getPart', category_id = category_id, part_id = part_id))
    if (request.method == "POST"):
        partName = request.form['partName']
        partDescription = request.form['partDescription']
        partCategory = request.form['partCategory']
        partToedit.name = partName
        partToedit.description = partDescription
        categoryOfPart = session.query(Categories).filter_by(name=partCategory).first()
        partToedit.category_id = categoryOfPart.id
        session.commit()
        return redirect(url_for('getPart',category_id = partToedit.category_id, part_id = part_id ))
    categories = session.query(Categories).group_by(Categories.name)
    return render_template('editPart.html', categories = categories, part = partToedit, user = user.username)

# part delete page --shows form to delete a part
@app.route('/<int:category_id>/<int:part_id>/delete', methods=['GET','POST'] )
def deletePart(category_id,part_id):
    session.close()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    partToDelete = session.query(Parts).filter_by(id=part_id).first()
    user = session.query(Users).filter_by(id=partToDelete.user_id).first()
    if user.username != login_session.get('username'):
        return redirect(url_for('getPart', category_id = category_id, part_id = part_id))
    if request.method == 'POST':
        session.delete(partToDelete)
        session.commit()
        return redirect(url_for('getCategory', category_id = category_id))
    return render_template('deletePart.html', part = partToDelete, user = login_session['username'])

# json data
@app.route('/JSON')
def getJSON():
    parts = session.query(Parts).all()
    return jsonify(Parts=[r.serialize for r in parts])

if (__name__ == '__main__'):
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)