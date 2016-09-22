from ConfigParser import ConfigParser
from os import path
from flask import Flask, request
from models import db, User, Achievements, Statistics
from flask_jsonschema import JsonSchema, ValidationError
from flask_migrate import Migrate
from custom_exceptions import AlreadyExists
from helpers import respond
from simple_auth import requires_auth

config = ConfigParser()
config.read('db.conf')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://"+config.get('DB', 'user')+":"+config.get('DB', 'password')+"@"+config.get('DB', 'host')+"/"+config.get('DB', 'db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONSCHEMA_DIR'] = path.join(app.root_path, 'schemas')
jsonschema = JsonSchema(app)
db.init_app(app)
migrate = Migrate(app, db)


"""jsonschema error handler"""
@app.errorhandler(ValidationError)
def on_validation_error(e):
    return respond({'error': e.message}, 400)

#routes
api = '/api/v1'


@app.route(api+'/user', methods=['POST'])
@requires_auth
@jsonschema.validate('user', 'create')
def createUser():
    req = request.get_json()
    try:
        newuser = User(username=req['username'], email=req['email'])
        db.session.add(newuser)
        db.session.commit()
        return respond({'user': newuser.columns_to_dict()}, 201)
    except AlreadyExists as e:
        return respond({'error': e.message}, 400)


@app.route(api+'/user/<string:account_id>', methods=['GET'])
@requires_auth
def getUser(account_id):
    try:
        user = User.query.filter_by(account_id=account_id).first()
        response = respond({'user': user.columns_to_dict()}, 200)
    except:
        response = respond({'error': "user not found"}, 404)
    return response


@app.route(api+'/user/<string:account_id>', methods=['PUT'])
@requires_auth
@jsonschema.validate('user', 'update')
def updateUser(account_id):
    req = request.get_json()
    try:
        user = User.query.filter_by(account_id=account_id).first()
        user.update(req)
        db.session.commit()
        return respond({'user': user.columns_to_dict()}, 201)
    except AlreadyExists as e:
        return respond({"error": e.message}, 400)


@app.route(api+'/user/<string:account_id>/<string:info>', methods=['GET'])
@requires_auth
def getUserInfo(account_id, info):
    if info not in ['statistics', 'achievements']:
        return respond({"error": "invalid url"}, 404)
    else:
        if info == 'achievements':
            return getUserAchievements(account_id=account_id)
        elif info == 'statistics':
            return getUserStastistics(account_id=account_id)


def getUserAchievements(account_id):
    try:
        user = User.query.filter_by(account_id=account_id).options(db.load_only("id")).first()
        achievements = Achievements.query.filter_by(user_id=user.id).all()
        result = {}

        for index in range(len(achievements)):
   	        result[index] = achievements[index].columns_to_dict()
        return respond({'achievements': result}, 200)
    except:
        return respond({'error': "user not found"}, 404)


def getUserStastistics(account_id):
    try:
        user = User.query.filter_by(account_id=account_id).options(db.load_only("id")).first()
        statistics = Statistics.query.filter_by(user_id=user.id).order_by(Statistics.created_at.desc()).first()
        res = {"statistics": statistics.columns_to_dict()}
        return respond(res, 200)
    except:
        return respond({"error": "user not found"}, 404)


@app.route(api+'/user/<string:account_id>/achievements', methods=['POST'])
@requires_auth
@jsonschema.validate('achievements', 'create')
def updateUserAchievements(account_id):
    try:
        req = request.get_json()
        user = User.query.filter_by(account_id=account_id).options(db.load_only("id")).first()
        achiev = Achievements(user_id=user.id, achievement=req['achievement'])
        db.session.add(achiev)
        db.session.commit()
        resp = {"success": "achievement has been added successfully"}
        return respond(resp, 201)
    except:
        return respond({"error": "user not found"}, 404)


@app.route(api+'/user/<string:account_id>/statistics', methods=['POST'])
@requires_auth
@jsonschema.validate('statistics', 'create')
def updateUserStatistics(account_id):
    try:
        req = request.get_json()
        user = User.query.filter_by(account_id=account_id).options(db.load_only("id")).first()
        stats = Statistics(user_id=user.id, wins=req['wins'], losses=req['losses'], score=req['score'], level=req['level'])
        db.session.add(stats)
        db.session.commit()
        resp = {"success": "statistics has been added successfully"}
        return respond(resp, 201)
    except:
        return respond({"error": "user not found"}, 404)



if __name__ == '__main__':
    app.run(debug=True)
