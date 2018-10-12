#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, asc, exists, desc
from sqlalchemy.orm import sessionmaker
from setupDb import Base, Parts, Categories, Users
from flask import session as login_session
import random, string


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
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    #return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Login Page with from for log in and sign up
@app.route('/existingUser', methods = ['GET', 'POST'])
def logIn():
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
            return render_template('login.html')

    return render_template('login.html')

# create new user
@app.route('/newUser', methods=['POST','GET'])
def createUser():
    if request.args.get('state') != login_session.get('state'):
        return "invalid state parameter"
    if ( request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        user = session.query(Users).filter_by(username = username).first()
        session.close()
        if user: 
            #session.close()
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
    del login_session['username']  
    return redirect(url_for('getMainPage'))


#########**************** Resource pages ***********************#########

# Main page --  shows all categories and recently added items
@app.route('/')
def getMainPage():
    latestParts = session.query(Parts).order_by(Parts.id.desc()).limit(10)
    categories = session.query(Categories).group_by(Categories.name)
    session.close()
    if 'username' in login_session:
        username = login_session['username']
        return render_template('mainPrivate.html', categories = categories, latestParts = latestParts, user = username )    
    return render_template('main.html', categories = categories, latestParts = latestParts)

# new part page --shows form to set up a new part
@app.route('/newpart')
def createNewPart():
    return render_template('newPart.html')

# category page --  shows all parts of the specific category
@app.route('/<int:category_id>')
def getCategory(category_id):
    return render_template('category.html')

# part page --shows all info of the specific part
@app.route('/<int:category_id>/<int:part_id>')
def getPart(category_id, part_id):
    return render_template('part.html')

# part edit page --shows form to edit a part
@app.route('/<int:category_id>/<int:part_id>/edit')
def editPart(category_id, part_id):
    return render_template('editPart.html')

# part delete page --shows form to delete a part
@app.route('/<int:category_id>/<int:part_id>/delete')
def deletePart(category_id,part_id):
    return render_template('deletePart.html')


if (__name__ == '__main__'):
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)