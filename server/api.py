from flask import Flask
from flask.ext.restful import Resource, reqparse, Api
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/haikyou'
db = SQLAlchemy(app)
api = Api(app)

import models

class User(Resource):
    def get(self, nickname):
        user = models.User.query.filter(
                models.User.nickname == nickname).first()
        if user is None:
            return { 'status': 404, 'message': 'User does not exist' }

        return {
            'id': user.id,
            'nickname': user.nickname,
            'description': user.description
        }

new_user_parser = reqparse.RequestParser()
new_user_parser.add_argument('email', type=str)
new_user_parser.add_argument('nickname', type=str)
new_user_parser.add_argument('description', type=str)

class UserList(Resource):
    def get(self):
        users = models.User.query.all()

        return {
            'users': [
                { 'id': user.id, 'nickname': user.nickname }
                for user in users
            ]
        }

    def post(self):
        args = new_user_parser.parse_args()

        email = args['email']
        nickname = args['nickname']
        description = args['description']

        # check to see if a user with this email or nickname exists already
        user = models.User.query.filter(
                models.User.nickname == nickname).first()
        if user is not None:
            return { 
                'status': 400, 
                'message': 'A user with this nickname already exists' 
            }

        user = models.User.query.filter(
                models.User.email == email).first()
        if user is not None:
            return { 
                'status': 400,
                'message': 'A user with this email already exists' 
            }

        # create the new user
        user = models.User(
                email=email,
                nickname=nickname,
                description=description)

        db.session.add(user)
        db.session.commit()

        # if successful, we return back the new user's id
        return { 'id': user.id }

## The Actual API endpoints
api.add_resource(User, '/users/<string:nickname>/')
api.add_resource(UserList, '/users/')

if __name__ == '__main__':
    app.run(debug=True)
