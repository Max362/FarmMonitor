# Importing packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#Defining our database
db = SQLAlchemy()
DB_NAME = "database.db"

#Initialising the Flask App
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #Initialising our database
    db.init_app(app)

    from .views import views
    from .auth import auth

    #Registering our blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #The models need to run befor we create the database
    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    #If user is not logged in flask will redirect us to login page
    login_manager.login_view = 'auth.login'
    #We telling login manager which app we are using
    login_manager.init_app(app)

    #This will tell Flask how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

#Creating a database if not already exists
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
