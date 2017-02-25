import json
from datetime import datetime
from flask import make_response
from flask_restful import Resource, reqparse
from sqlalchemy import create_engine
from restless.settings import engine



class Restless(Resource):
    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()
        self.conn = engine.connect()
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

    @staticmethod
    def merge_results(data_, results):
        count = 0
        data = {}
        data.update(data_)
        for key in data.keys():
            data[key] = str(results[count])
            count += 1
        return data

    def timestamp(self):
        return str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
