#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, asc, exists, desc
from sqlalchemy.orm import sessionmaker
from setupDb import Base, Parts, Categories, Users
from flask import session as login_session
import random, string

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
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    session.close()
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

# create new user
@app.route('/newUser', methods=['POST','GET'])
def createUser():
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
    users = session.query(Users).all()
    if 'username' not in login_session:
        return render_template('main.html', categories = categories, latestParts = latestParts, users = users)
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


if (__name__ == '__main__'):
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)