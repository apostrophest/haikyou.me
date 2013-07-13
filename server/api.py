from datetime import datetime
import json

from flask import Flask
from flask.ext.restful import Resource, reqparse, Api, fields, marshal_with
from flask.ext.restful import abort, marshal
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/haikyou'
db = SQLAlchemy(app)
api = Api(app)

import models

###############################
### Resources
###

###############################
## The User Resource

user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True)
user_parser.add_argument('nickname', type=str, required=True)
user_parser.add_argument('description', type=str)

user_fields = {
    'id': fields.Integer,
    'date': fields.DateTime,
    'last_updated': fields.DateTime,
    'email': fields.String,
    'nickname': fields.String,
    'description': fields.String 
}

# this is a helper function that will abort 400 if this email exists already
def abort_on_duplicate_user_email(email):
    user = models.User.query.filter(models.User.email == email).first()
    if user is not None:
        abort(400, message='A user with this email already exists')

# likewise for nicknames
def abort_on_duplicate_user_nickname(nickname):
    user = models.User.query.filter(models.User.nickname == nickname).first()
    if user is not None:
        abort(400, message='A user with this nickname already exists')

class User(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = models.User.query.get(user_id)
        if user is None:
            abort(404, message='User does not exist')

        return user

    @marshal_with(user_fields)
    def put(self, user_id):
        args = user_parser.parse_args()

        email = args['email']
        nickname = args['nickname']
        description = args['description']

        # find the user, if it exists
        user = models.User.query.get(user_id)
        if user is None:
            # create a new user, but first make sure no duplicates
            abort_on_duplicate_user_email(email)
            abort_on_duplicate_user_nickname(nickname)

            user = models.User(
                    email=email, 
                    nickname=nickname,
                    description=description)

            db.session.add(user)
        else:
            # update the user, but first make sure no duplicates
            # however in this case, we only check if the nick/email has changed
            if nickname != user.nickname:
                abort_on_duplicate_user_nickname(nickname)
            
            if email != user.email:
                abort_on_duplicate_user_nickname(email)
            
            user.email = email
            user.nickname = nickname
            user.description = description
            user.last_updated = datetime.utcnow()

        db.session.commit()

        return user, 201

class UserList(Resource):
    def get(self):
        users = models.User.query.all()

        return { 
            'users': [ marshal(user, user_fields) for user in users ]
        }

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()

        email = args['email']
        nickname = args['nickname']
        description = args['description']

        # check to see if a user with this email or nickname exists already
        abort_on_duplicate_user_email(email)
        abort_on_duplicate_user_nickname(nickname)

        # create the new user
        user = models.User(
                email=email,
                nickname=nickname,
                description=description)

        db.session.add(user)
        db.session.commit()

        return user, 201

#############################
## The Haiku Resource

haiku_parser = reqparse.RequestParser()
haiku_parser.add_argument('user_id', type=int, required=True)
haiku_parser.add_argument('title', type=str, required=True)
haiku_parser.add_argument('first_line', type=str, required=True)
haiku_parser.add_argument('second_line', type=str, required=True)
haiku_parser.add_argument('third_line', type=str, required=True)

haiku_fields = {
    'id': fields.Integer,
    'date': fields.DateTime,
    'user_id': fields.Integer,
    'title': fields.String,
    'first_line': fields.String,
    'second_line': fields.String,
    'third_line': fields.String
}

class Haiku(Resource):
    @marshal_with(haiku_fields)
    def get(self, haiku_id):
        haiku = models.Haiku.query.get(haiku_id)
        if haiku is None:
            abort(404, message='Haiku not found')

        return haiku

    @marshal_with(haiku_fields)
    def put(self):
        pass

class HaikuList(Resource):
    def get(self):
        haikus = models.Haiku.query.all()

        return {
            'haikus': [ marshal(haiku, haiku_fields) for haiku in haikus ]
        }

    def post(self):
        args = haiku_parser.parse_args()

        user_id = args['user_id']
        title = args['title']
        first_line = args['first_line']
        second_line = args['second_line']
        third_line = args['third_line']

        # make sure a user with this user_id exists
        user = models.User.query.get(user_id)
        if user is None:
            return { 
                'status': 400,
                'message': 'Invalid user'
            }

        # otherwise create the new haiku and add it
        haiku = models.Haiku(
                user_id=user_id,
                title=title,
                first_line=first_line,
                second_line=second_line,
                third_line=third_line)

        db.session.add(haiku)
        db.session.commit()

        # return the id of the new haiku if successful
        return { 'id': haiku.id }


## The Actual API endpoints
api.add_resource(User, '/users/<int:user_id>/')
api.add_resource(UserList, '/users/')
api.add_resource(HaikuList, '/haikus/')
api.add_resource(Haiku, '/haikus/<int:haiku_id>/')

if __name__ == '__main__':
    app.run(debug=True)
