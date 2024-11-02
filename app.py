from datetime import timedelta
from functools import wraps
import os
from flask import Flask, flash, redirect, session, url_for
from controllers import articles_controller
from controllers import recipes_controller
from models.models import db
from flask_migrate import Migrate

app = Flask(__name__)

# Configure database
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
hostname = os.getenv('DB_HOSTNAME')
database_name = os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{hostname}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Set a secret key for session management
app.secret_key = os.urandom(24)

db.init_app(app)  # Initialize the app with db

migrate = Migrate(app, db)

@app.route("/", methods=["GET"])
def index():
    return "REST API"

######################################################################
######################## Articles Endpoint ###########################
######################################################################

@app.route("/articles/", methods=["GET"])
def all_articles():
    return articles_controller.get_all_articles()

@app.route("/articles/<int:id>/", methods=["GET"])
def detail_article(id):
    return articles_controller.get_detail_articles(id)

######################################################################
######################## Recipes Endpoint ###########################
######################################################################

@app.route("/recipes/", methods=["GET"])
def all_recipes():
    return recipes_controller.get_all_recipes()

@app.route("/recipes/<int:id>/", methods=["GET"])
def detail_recipe(id):
    return recipes_controller.get_detail_recipes(id)