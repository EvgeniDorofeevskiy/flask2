from api import db


class AuthorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32), server_default='ivanov', default= 'petrov')
    quotes = db.relationship(
        'QuoteModel', backref='author', lazy='dynamic', cascade='all, delete')

    def __init__(self, name, surname= 'petrov'):
        self.name = name
        self.surname = surname


