from api import db
from passlib.apps import custom_app_context as pwd_context


class UserModel(db.Model):
   __tablename__= 'users'
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(32), unique=True)
   password_hash = db.Column(db.String(128))

   def __init__(self, username, password):
       self.username = username
       self.hash_password(password)

   def hash_password(self, password):
       self.password_hash = pwd_context.encrypt(password)

   def verify_password(self, password):
       return pwd_context.verify(password, self.password_hash)
