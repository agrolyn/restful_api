from datetime import timedelta
import os
from flask import Flask
from itsdangerous import URLSafeTimedSerializer
from controllers import articles_controller, recipes_controller, auth_controller, profile_controller, community_controller
# from controllers import detection_controller
from models.models import db
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager, jwt_required
from flask_mail import Mail

app = Flask(__name__)

# Secret key for session management and jwt
app.config["SECRET_KEY"] = os.urandom(24)
app.config["JWT_SECRET_KEY"] = os.urandom(32)  # JWT secret key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

# Database configuration
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOSTNAME = os.getenv('DB_HOSTNAME')
DB_NAME = os.getenv('DB_NAME')
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

app.config["MAIL_SERVER"] = 'mail.agrolyn.online'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')
app.config["MAIL_DEFAULT_SENDER"] = ('AGROLYN', "admin@agrolyn.online")

# Database init
db.init_app(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Configure Flask Migration
migrate = Migrate(app, db)

# Configure JWT
jwt = JWTManager(app)

# Configure Email
mail = Mail(app)

# Configure Swagger
swagger = Swagger(app, template_file='api_docs.yml')

@app.route("/", methods=["GET"])
def index():
    return "<div style='display: flex; justify-content: center; align-items: center; width: 100%; min-height: 100vh; font-size: 1.5rem; font-weight: semibold;'>AGROLYN RESTFUL API</div>"

######################################################################
###################### Users Auth Endpoint ###########################
######################################################################

@app.route('/register', methods=['POST'])
def register():
    return auth_controller.register_acc(s, mail)

@app.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    return auth_controller.confirm_email_acc(token, s)

@app.route('/login', methods=['POST'])
def login():
    return auth_controller.login_acc()

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    return auth_controller.forgot_pwd(s, mail)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    return auth_controller.reset_pwd(token, s)

@app.route('/logout', methods=['POST'])
def logout():
    return auth_controller.logout_acc()

@app.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)  # Memastikan hanya refresh token yang bisa mengakses route ini
def refresh_access_token():
    return auth_controller.refresh_token()

######################################################################
######################## Articles Endpoint ###########################
######################################################################

@app.route("/articles/", methods=["GET"])
@jwt_required()
def all_articles():
    return articles_controller.get_all_articles()

@app.route("/articles/<int:id>/", methods=["GET"])
@jwt_required()
def detail_article(id):
    return articles_controller.get_detail_articles(id)

######################################################################
######################## Recipes Endpoint ############################
######################################################################

@app.route("/recipes/", methods=["GET"])
@jwt_required()
def all_recipes():
    return recipes_controller.get_all_recipes()

@app.route("/recipes/<int:id>/", methods=["GET"])
@jwt_required()
def detail_recipe(id):
    return recipes_controller.get_detail_recipes(id)

######################################################################
######################## Profile Endpoint ############################
######################################################################

@app.route("/edit-profile", methods=["PUT"])
@jwt_required()
def edit_profile():
    return profile_controller.edit_profile()

######################################################################
####################### Community Endpoint ###########################
######################################################################

@app.route("/community/questions", methods=["GET"])
def get_all_question():
    return community_controller.get_all_question()

# @app.route("/questions/<int:id>/", methods=["GET"])
# @jwt_required()
# def get_detail_question(id):
#     return community_controller.get_detail_question(id)

# @app.route('/disccus/<int:questions_id>', methods=['GET'])
# @jwt_required()
# def get_disccus_route(questions_id):
#     return community_controller.get_disccus_by_question(questions_id)

######################################################################
#################### AI Prediction Endpoint ##########################
######################################################################

# @app.route('/predict', methods=['POST'])
# def predict():
#     return detection_controller.predict()

if __name__ == "__main__":
    app.run(debug=True)
