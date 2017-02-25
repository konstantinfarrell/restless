from flask import Flask
from flask_restful import Api
from restless.users import UsersMeta, UsersMetaId
from restless.settings import Base, engine


Base.metadata.create_all(engine)

app = Flask(__name__)
api = Api(app)

api.add_resource(UsersMeta, '/users')
api.add_resource(UsersMetaId, '/users/<uuid:id>')


if __name__ == '__main__':
    app.run()
