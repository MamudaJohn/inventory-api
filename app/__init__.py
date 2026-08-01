import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, current_user
from dotenv import load_dotenv
import uuid


app = Flask(__name__)


load_dotenv()

# CONFIGURATIONS 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("POSTGRESS_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  ## Flask-Security-Too configuration
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT")
app.config['SECURITY_PASSWORD_HASH'] = "bcrypt"
app.config['SECURITY_REGISTERABLE'] = True
# app.config['SECURITY_RECOVERABLE'] = ""
# app.config['SECURITY_CONFIRMABLE'] = ""
app.config['SECURITY_CHANGEABLE'] = True
# app.config['SECURITY_SEND_REGISTER_EMAIL'] = ""



# INITIALISED SQLALCHEMY
db = SQLAlchemy(app)

from .models.user import User
from .models.role import Role

# INITIALISE MIGRATE
migrate = Migrate(app, db)

# Flask Security initialisation
user_datastore = SQLAlchemyUserDatastore(db, user_model=User, role_model=Role)
security = Security(app, user_datastore)

from .routes import bp as rolesBlueprint

app.register_blueprint(rolesBlueprint)


@app.route("/")
def Welcome():
    user = User(
        username = "John Mamuda",
        email = "mamuda@gmail.com",
        password = "123456789",
        fs_uniquifier=str(uuid.uuid4().hex)
    )
    user.add_role_by_name("Super Admin")
    db.session.add(user)
    db.session.commit()


    result = User.query.all()
    result = [sult.to_dict() for sult in result]
    # print(result)


    rolelist = Role.query.all()
    resul = [sult.to_dict() for sult in rolelist]
    # print(resul)
    # print(resul)
    db.session.commit()
    return f"<h1>Welcome</h1><br/><h3>HELLO WORLD!!</h3><br/>{result}<br/>{resul}"