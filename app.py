from flask import (Flask, render_template, 
                    request, redirect, url_for)
from bson import ObjectId
from pymongo import MongoClient
import os