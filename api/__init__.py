import gc
from config import Config
from flask import Flask , g, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
basic_auth = HTTPBasicAuth() #← Старый меняем
token_auth = HTTPTokenAuth('Bearer') #← Новый добавляем
multi_auth = MultiAuth(basic_auth, token_auth) #← Объединяем




@basic_auth.verify_password
def verify_password(username, password):
   from api.models.user import UserModel
   user = UserModel.query.filter_by(username = username).first()
   if not user or not user.verify_password(password):
       return False
#    g.user = user
   return user


@token_auth.verify_token
def verify_token(token):
   from api.models.user import UserModel
   user = UserModel.verify_auth_token(token)
   print(f"{user=}")
   return user

