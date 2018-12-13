from flask import (Flask, render_template, 
                    request, redirect, url_for)
from bson import ObjectId
from pymongo import MongoClient
import os

app = Flask(__name__)

# template title and heading
title = "TODO app"
heading = "A Generic TODO reminder!"

# connecting to MongoDB and selecting database
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb

# selecting collection name
todos = db.todo

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/list")
def lists():
    """Displays all to-do lists"""
    todos_l = todos.find()
    a1 = "active"
    return render_template('index.html', a1=a1,
                            todos=todos_l,
                            t=title, h=heading)

@app.route("/")
@app.route("/uncompleted")
def tasks():
    # Display uncompleted tasks
    todos_l = todos.find({"done" : "no"})
    a2 = "active"
    return render_template('index.html', a2=a2,
                            todos=todos_l,
                            t=title, h=heading)

@app.route("/completed")
def completed():
    """Displays all completed to-do lists"""
    todos_l = todos.find({'done':'yes'})
    a1 = "active"
    return render_template('index.html', a1=a1,
                        todos=todos_l, t=title, h=heading)

@app.route("/done")
def done():
    """Displays the DONE or NOT-DONE icon"""
    id = request.values.get("_id")
    task = todos.find({"_id":ObjectId(id)})
    if(task[0]["done"]=="yes"):
        todos.update({"_id":ObjectId(id)},
                     {"$set": {"done":"no"}})
    else:
        todos.update({"_id":ObjectId(id)},
                     {"$set": {"done":"yes"}})
    
    redir = redirect_url()

    return redirect_url
    
