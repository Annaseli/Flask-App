from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f9ac5193def46b21bcbf5ed7cd295aef'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# Flask-Login an extension that handles user session management
login_manager = LoginManager(app)
# when the user is not logged in and tries to access the account page it redirects to the login_view function
login_manager.login_view = 'login'
# when the user is not logged in and tries to access the account page it gets a message that bootstrap will categorize
# as "info" for style
login_manager.login_message_category = 'info'

from flaskblog import routes
