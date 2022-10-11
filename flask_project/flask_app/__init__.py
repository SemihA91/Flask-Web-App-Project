from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dash_app2 import create_dash_application
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
mail = Mail()


def create_app(test=False):

    """
    Creates the app and configures basic parameters. Manages some imports,
    blueprints and database.


    Parameters
    ----------
        No Parameters

    Returns
    -------
    app : Flask variable
        The configures flask app

    """

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'EDbzVfAz6kSB5Up9OHOflQ'

    if test:
        # Database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    else:
        # Database for deployment
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///intergeo.db'

    app.config['IMAGE_UPLOADS'] = 'static/images'
    app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'internationalgeographic14@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Internationalgeographic69'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    mail.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it
        # in the query for the user
        return User.query.get(int(user_id))

    with app.app_context():

        # blueprint for auth routes in our app
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth parts of app
        from .main_routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .blog_routes import blog as blog_blueprint
        app.register_blueprint(blog_blueprint)

        db.create_all()
        app = create_dash_application(app)

    return app
