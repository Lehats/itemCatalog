#!/usr/bin/env python3
from flask import Flask, render_template


app = Flask(__name__)

# Main page --  shows all categories and recently added items
@app.route('/')
def getMainPage():
    return render_template('main.html')

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