from flask import Flask
from flask_restful import Resource, Api
from restless.main import UsersMeta, UsersMetaId


app = Flask(__name__)
api = Api(app)

api.add_resource(UsersMeta, '/users')
api.add_resource(UsersMetaId, '/users/<int:id>')


if __name__ == '__main__':
    app.run()
