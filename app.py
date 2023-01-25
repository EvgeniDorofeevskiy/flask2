from api import app
from api.handlers import author
from api.handlers import quote
from api.handlers import user
from api.handlers import token
from config import Config


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
