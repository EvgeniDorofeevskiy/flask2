from api import db, Config
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import URLSafeSerializer, BadSignature
# from itsdangerous import TimedSerializer as Serializer SignatureExpired



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

   def generate_auth_token(self):
       s = URLSafeSerializer(Config.SECRET_KEY)
       return s.dumps({'id': self.id})



   @staticmethod
   def verify_auth_token(token):
       s = URLSafeSerializer(Config.SECRET_KEY)
       try:
           data = s.loads(token)
       except BadSignature:
           return None  # invalid token
       user = UserModel.query.get(data['id'])
       return user


#    def generate_auth_token_exptime(self, expiration=600):
#         s = Serializer(Config.SEKRET_KEY, expires_in=expiration)
#         return s.dumps({'id': self.id})

#    @staticmethod
#    def verify_auth_token_exptime(token):
#        s = Serializer(Config.SECRET_KEY)
#        try:
#            data = s.loads(token)
#        except SignatureExpired:
#            return None  # invalid token
#        except BadSignature:
#            return None  # invalid token
#        user = UserModel.query.get(data['id'])
#        return user