from datetime import timedelta
import os
from flask import Flask
from itsdangerous import URLSafeTimedSerializer
from controllers import articles_controller, recipes_controller, auth_controller, profile_controller, community_controller, ecommerce_controller, videdu_controller, detection_controller, history_detection_controller
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

@app.route('/register/', methods=['POST'])
def register():
    return auth_controller.register_acc(s, mail)

@app.route('/confirm/<token>/', methods=['GET'])
def confirm_email(token):
    return auth_controller.confirm_email_acc(token, s)

@app.route('/login/', methods=['POST'])
def login():
    return auth_controller.login_acc()

@app.route('/forgot_password/', methods=['POST'])
def forgot_password():
    return auth_controller.forgot_pwd(s, mail)

@app.route('/reset_password/<token>/', methods=['GET', 'POST'])
def reset_password(token):
    return auth_controller.reset_pwd(token, s)

@app.route('/logout/', methods=['POST'])
@jwt_required()
def logout():
    return auth_controller.logout_acc()

@app.route('/refresh-token/', methods=['POST'])
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
##################### Video Education Endpoint #######################
######################################################################

@app.route("/video-education/", methods=["GET"])
@jwt_required()
def all_videdu():
    return videdu_controller.get_all_videdu()

@app.route("/video-education/<int:id>/", methods=["GET"])
@jwt_required()
def detail_videdu(id):
    return videdu_controller.get_detail_videdu(id)

######################################################################
######################## Profile Endpoint ############################
######################################################################

@app.route("/edit-profile/", methods=["PUT"])
@jwt_required()
def edit_profile():
    return profile_controller.edit_profile()

######################################################################
####################### Community Endpoint ###########################
######################################################################

@app.route("/community/questions/", methods=["GET"])
@jwt_required()
def get_all_question():
    return community_controller.get_all_question()

@app.route("/community/questions/<int:id>/", methods=["GET"])
@jwt_required()
def get_detail_question(id):
    return community_controller.get_detail_question(id)

# Filtering
@app.route("/community/questions/filters/<string:filter_name>/", methods=["GET"])
@jwt_required()
def get_filtered_question(filter_name):
    return community_controller.get_filtered_question(filter_name)

# Search Community Question
@app.route("/community/questions/search/", methods=["GET"])
@jwt_required()
def search_community_q():
    return community_controller.search_community_question()

# Like and Dislike Community Question
@app.route("/community/questions/<int:id>/like/", methods=["POST"])
@jwt_required()
def inc_like_question(id):
    return community_controller.inc_like_q(id)

@app.route("/community/questions/<int:id>/dislike/", methods=["POST"])
@jwt_required()
def dec_like_question(id):
    return community_controller.dec_like_q(id)

# Like and Dislike Community Answer
@app.route("/community/answer/<int:id>/like/", methods=["POST"])
@jwt_required()
def inc_like_answer(id):
    return community_controller.inc_like_ans(id)

@app.route("/community/answer/<int:id>/dislike/", methods=["POST"])
@jwt_required()
def dec_like_answer(id):
    return community_controller.dec_like_ans(id)

# CRUD Community Question
@app.route("/community/question/new/", methods=["POST"])
@jwt_required()
def new_question():
    return community_controller.new_q()

@app.route("/community/question/update/<int:question_id>/", methods=["PUT"])
@jwt_required()
def upd_question(question_id):
    return community_controller.update_q(question_id)

@app.route("/community/question/delete/<int:question_id>/", methods=["DELETE"])
@jwt_required()
def del_question(question_id):
    return community_controller.delete_q(question_id)

# CRUD Community Answer by Question Id
@app.route("/community/answer/new/<int:question_id>/", methods=["POST"])
@jwt_required()
def new_ans(question_id):
    return community_controller.new_ans(question_id)

@app.route("/community/answer/update/<int:answer_id>/", methods=["PUT"])
@jwt_required()
def upd_ans(answer_id):
    return community_controller.update_ans(answer_id)

@app.route("/community/answer/delete/<int:answer_id>/", methods=["DELETE"])
@jwt_required()
def del_ans(answer_id):
    return community_controller.delete_ans(answer_id)

######################################################################
####################### E-Commerce Endpoint ##########################
######################################################################

# Common GET Request E-Commerce
# Common User
@app.route("/ecommerce/products/", methods=["GET"])
@jwt_required()
def get_all_products():
    return ecommerce_controller.get_all_products()

@app.route("/ecommerce/products/filters/<int:product_categories_id>/", methods=["GET"])
@jwt_required()
def get_filtered_products(product_categories_id):
    return ecommerce_controller.get_filtered_products(product_categories_id)

@app.route("/ecommerce/products/search/", methods=["GET"])
@jwt_required()
def search_product():
    return ecommerce_controller.search_product()

# Farmer
@app.route("/ecommerce/products/me/", methods=["GET"])
@jwt_required()
def product_me():
    return ecommerce_controller.product_me()

# CRUD Functionality
@app.route("/ecommerce/products/new-product/", methods=["POST"])
@jwt_required()
def new_product():
    return ecommerce_controller.new_product()

@app.route("/ecommerce/products/update-product/<int:product_id>/", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    return ecommerce_controller.update_product(product_id)

@app.route("/ecommerce/products/delete-product/<int:product_id>/", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    return ecommerce_controller.delete_product(product_id)

#####################################################################
################### AI Prediction Endpoint ##########################
#####################################################################

@app.route('/corn-disease-predict/<string:disease>/', methods=['POST'])
@jwt_required()
def corn_disease_predict(disease):
    return detection_controller.disease_detection(disease, "corn")

@app.route('/rice-disease-predict/<string:disease>/', methods=['POST'])
@jwt_required()
def rice_disease_predict(disease):
    return detection_controller.disease_detection(disease, "rice")

@app.route('/history/detection-history/', methods=['GET'])
@jwt_required()
def history_detection():
    return history_detection_controller.get_all_history()

@app.route('/history/detection-history/<int:id_history>/', methods=['GET'])
@jwt_required()
def detail_history_detection(id_history):
    return history_detection_controller.get_detail_history(id_history)

@app.route('/history/detection-history/delete-history/<int:id_detection>/', methods=['DELETE'])
@jwt_required()
def delete_history_detection(id_detection):
    return history_detection_controller.delete_detection_by_id(id_detection)

@app.route('/history/detection-history/delete-all-history/', methods=['DELETE'])
@jwt_required()
def delete_all_history_detection():
    return history_detection_controller.delete_all_detections()

if __name__ == "__main__":
    app.run(debug=True)
