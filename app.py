from flask import (Flask, render_template, 
                    request, redirect, url_for)
from bson import ObjectId
from pymongo import MongoClient
import os

app = Flask(__name__)

# template title and heading
title = "TO-DO App"
heading = "A Generic TO-DO reminder!"

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
    a3 = "active"
    return render_template('index.html', a3=a3,
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

    return redirect(redir)

@app.route("/action", methods=['POST'])
def action():
    """Adding a Task"""
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    todos.insert_one({
                "name" : name,
                "desc" : desc,
                "date" : date,
                "pr" : pr,
                "done" : "no"})
    
    return redirect("/list")

@app.route("/remove")
def remove():
    """Deleting a Task"""
    key = request.values.get("_id")
    todos.remove({"_id" : ObjectId(key)})

    return redirect("/")

@app.route("/update")
def update():
    id = request.values.get("_id")
    task = todos.find({"_id" : ObjectId(id)})
    
    return render_template('update.html',
                            tasks=task,
                            h=heading,
                            t=title)

@app.route("/action2", methods=['POST'])
def action2():
    """Updating a Task with various references"""
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    _id = request.values.get("_id")
    todos.update(
        {"_id" : ObjectId(_id)},
        {'$set': {
                    "name":name,
                    "desc":desc,
                    "date":date,
                    "pr":pr
                  }
        }
    )

    return redirect("/")

@app.route("/search", methods=['GET'])
def search():
    """Searching a Task with a reference"""

    key = request.values.get("key")
    refer = request.values.get("refer")
    if key=="_id":
        todos_l = todos.find(
            {refer : ObjectId(key)})
    else:
        todos_l = todos.find({refer: key})

    return render_template("searchlist.html",
                            todos=todos_l,
                            t=title,
                            h=heading)

if __name__ == "__main__":

    app.run()