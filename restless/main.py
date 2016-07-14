from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine


dbtype = "postgresql"
dbuser = "postgres"
dbpass = "postgres"
dbhost = "localhost"
dbname = "restless"

dbstring = "{dbtype}://{user}:{dbpass}@{host}/{name}".format(dbtype=dbtype,
                                                             user=dbuser,
                                                             dbpass=dbpass,
                                                             host=dbhost,
                                                             name=dbname)
e = create_engine(dbstring)


class UsersMeta(Resource):

    def get(self):
        conn = e.connect()
        q = conn.execute("SELECT * FROM \"User\"")
        result = {'users': q.cursor.fetchall()}
        return result


class UsersMetaId(Resource):

    def get(self, id):
        conn = e.connect()
        q = conn.execute("SELECT * FROM \"User\" WHERE id = {}".format(id))
        result = {'user': i for i in q.cursor.fetchall()}
        return result
