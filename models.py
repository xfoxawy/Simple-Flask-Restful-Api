from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from helpers import generate_unique_account_id
from custom_exceptions import AlreadyExists

db = SQLAlchemy()

#map models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime())
    achievements = db.relationship("Achievements")
    statistics = db.relationship("Statistics")

    def __init__(self, username, email):
        self.account_id = generate_unique_account_id()
        self.username = username
        self.email = email
        self.created_at = datetime.now()
        self.username_exists()
        self.email_exists()

    def __repr__(self):
        return '<User %s>' % self.account_id

    def columns_to_dict(self):
        x = {}
        for key in self.__mapper__.c.keys():
            if key != 'id':
                x[key] = getattr(self, key)
        return x

    def update(self, dic):
        unique = ["email", "username"]
        for key in dic:
            if key in self.__mapper__.c.keys():
                if key != 'id' and key != 'account_id':
                    if key in unique:
                        self.attribute_exists(**dic)
                    setattr(self, key, dic[key])

    def username_exists(self):
        if self.query.filter_by(username=self.username).first():
            raise AlreadyExists("username already exits")

    def email_exists(self):
        if self.query.filter_by(email=self.email).first():
            raise AlreadyExists("email already exists")

    def attribute_exists(self, **attribute):
        if self.query.filter_by(**attribute).first():
            raise AlreadyExists(attribute.keys()[0] + " already exists")


class Achievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    achievment = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)

    def __init__(self, user_id, achievement):
        self.user_id = user_id
        self.achievment = achievement
        self.created_at = datetime.now()

    def __repr__(self):
        return '<Achievement %s>' % self.achievment

    def columns_to_dict(self):
        x = {}
        for key in self.__mapper__.c.keys():
            if key != 'id' and key != 'user_id':
                x[key] = getattr(self, key)
        return x


class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    score = db.Column(db.Integer)
    level = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

    def __init__(self, user_id, wins, losses, score, level):
        self.user_id = user_id
        self.wins = wins
        self.losses = losses
        self.score = score
        self.level = level
        self.created_at = datetime.now()

    def __repr__(self):
        return '<Statistics for %s>' % self.wins

    def columns_to_dict(self):
        x = {}
        for key in self.__mapper__.c.keys():
            if key != 'id' and key != 'user_id':
                x[key] = getattr(self, key)
        return x
