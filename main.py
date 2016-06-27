from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine

dbtype = "postgresql"
dbuser = "postgres"
dbpass = ""
dbhost = ""
dbname = "restless"

dbstring = "{dbtype}://{user}:{dbpass}@{host}/{name}".format(dbtype=dbtype,
                                                             user=dbuser,
                                                             dbpass=dbpass,
                                                             host=dbhost,
                                                             name=dbname)

e = create_engine(dbstring)


app = Flask(__name__)
api = Api(app)


class UsersMeta(Resource):

    def get(self):
        conn = e.connect()
        q = conn.execute("SELECT * FROM \"User\"")
        result = {'users': [i for i in q.cursor.fetchall()]}
        return result


class UsersMetaCount(Resource):

    def get(self, count):
        conn = e.connect()
        q = conn.execute("SELECT * FROM \"User\" LIMIT {}".format(count))
        result = {'users': [i for i in q.cursor.fetchall()]}
        return result

api.add_resource(UsersMeta, '/users')
api.add_resource(UsersMetaCount, '/users/<int:count>')

if __name__ == '__main__':
    app.run()
