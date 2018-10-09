#!/usr/bin/env python3
from flask import Flask, render_template
from sqlalchemy import create_engine, asc, exists, desc
from sqlalchemy.orm import sessionmaker
from setupDb import Base, Parts


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



# Main page --  shows all categories and recently added items
@app.route('/')
def getMainPage():
    latestParts = session.query(Parts).order_by(Parts.id.desc()).limit(2)
    parts = session.query(Parts).group_by(Parts.category)
    session.close()
    return render_template('main.html', parts = parts, latestParts = latestParts)

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
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)