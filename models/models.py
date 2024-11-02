from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()

class PlantTypes(db.Model):
    __tablename__ = 'plant_types'
    id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(255), nullable=False)

    # Relationship
    questions = relationship('Questions', backref='plant_types', lazy=True)
    disccus = relationship('Disccus', backref='plant_types', lazy=True)
    plant_dis = relationship('PlantDis', backref='plant_types', lazy=True)

    def __repr__(self):
        return f"PlantTypes('{self.plant_name}')"


class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), nullable=False)

    # Relationship
    users = relationship('Users', backref='roles', lazy=True)

    def __repr__(self):
        return f"Roles('{self.role_name}')"


class TrsStatus(db.Model):
    __tablename__ = 'trs_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=False)

    # Relationship
    transactions = relationship('Transactions', backref='trs_status', lazy=True)

    def __repr__(self):
        return f"TrsStatus('{self.status}')"


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    released_date = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'thumbnail': self.thumbnail,
            'description': self.description,
            'location': self.location,
            'released_date': self.released_date
        }

    def __repr__(self):
        return f"Articles('{self.title}', '{self.location}')"


class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    img_recipe = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'img_recipe': self.img_recipe,
            'ingredients': self.ingredients,
            'steps': self.steps,
        }

    def __repr__(self):
        return f"Recipes('{self.title}')"


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    phone_number = db.Column(db.String(255))
    img_profile = db.Column(db.String(255))
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    # Relationship
    products = relationship('Products', backref='users', lazy=True)
    questions = relationship('Questions', backref='users', lazy=True)
    disccus = relationship('Disccus', backref='users', lazy=True)
    orders = relationship('Orders', backref='users', lazy=True)
    reviews = relationship('Reviews', backref='users', lazy=True)
    transactions = relationship('Transactions', backref='users', lazy=True)

    def __repr__(self):
        return f"Users('{self.name}', '{self.email}')"


class ProductCategories(db.Model):
    __tablename__ = 'product_categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)

    # Relationship
    products = relationship('Products', backref='product_categories', lazy=True)

    def __repr__(self):
        return f"ProductCategories('{self.category_name}')"


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    desc_product = db.Column(db.Text, nullable=False)
    img_product = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, default=0, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    sold = db.Column(db.Integer, default=0, nullable=False)
    product_categories_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship
    orders = relationship('Orders', backref='products', lazy=True)
    reviews = relationship('Reviews', backref='products', lazy=True)

    def __repr__(self):
        return f"Products('{self.product_name}', '{self.price}')"


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    like_num = db.Column(db.Integer, default=0)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plant_types_id = db.Column(db.Integer, db.ForeignKey('plant_types.id'), nullable=False)

    # Relationship
    disccus = relationship('Disccus', backref='questions', lazy=True)

    def __repr__(self):
        return f"Questions('{self.question}')"


class Disccus(db.Model):
    __tablename__ = 'disccus'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text, nullable=False)
    questions_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    plant_types_id = db.Column(db.Integer, db.ForeignKey('plant_types.id'), nullable=False)
    like_num = db.Column(db.Integer, default=0, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Disccus('{self.answer}')"


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    price_order = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, default=0, nullable=False)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Orders('{self.price_order}', '{self.qty}')"


class PlantDis(db.Model):
    __tablename__ = 'plant_dis'
    id = db.Column(db.Integer, primary_key=True)
    dis_name = db.Column(db.String(255), nullable=False)
    dis_indo_name = db.Column(db.String(255), nullable=False)
    handling = db.Column(db.Text, nullable=False)
    plant_types_id = db.Column(db.Integer, db.ForeignKey('plant_types.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"PlantDis('{self.dis_name}')"


class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=0, nullable=False)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Reviews('{self.review}', '{self.rating}')"


class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime, nullable=False)
    transaction_amount = db.Column(db.Integer, default=0, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trs_status_id = db.Column(db.Integer, db.ForeignKey('trs_status.id'), nullable=False)

    def __repr__(self):
        return f"Transactions('{self.transaction_date}', '{self.transaction_amount}')"
