import json
from flask import make_response
from flask_restful import Resource, reqparse
from sqlalchemy import create_engine


dbtype = "mysql+pymysql"
dbuser = "root"
dbpass = ""
dbhost = "localhost"
dbname = "restless"

dbstring = "{dbtype}://{user}:{dbpass}@{host}/{name}".format(dbtype=dbtype,
                                                             user=dbuser,
                                                             dbpass=dbpass,
                                                             host=dbhost,
                                                             name=dbname)
e = create_engine(dbstring)


class Restless(Resource):
    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()
        self.conn = e.connect()
        super(Restless, self).__init__(*args, **kwargs)

    def body(self, args):
        for arg in args:
            self.parser.add_argument(arg)
        return self.parser.parse_args()

    def output_json(self, data, code, headers=None):
        if not headers:
            headers = {
                'Content-Type': 'application/json'
            }
        resp = make_response(json.dumps(data), code)
        resp.headers.extend(headers or {})
        return resp
