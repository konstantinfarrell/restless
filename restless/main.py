import json
from uuid import uuid4
from flask import make_response
from flask_restful import Resource, reqparse
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from restless import Restless




class UsersMeta(Restless):

    def get(self):
        q = self.conn.execute("SELECT * FROM User")
        result = {'users': q.cursor.fetchall()}
        return result

    def post(self):
        args = ['first_name', 'last_name', 'username', 'email']
        body = self.body(args)
        body['uuid'] = str(uuid4())
        for key, value in body.items():
            if not value:
                return self.output_json(data={}, code=400)

        sql = 'INSERT INTO User (first_name, last_name, username, email, uuid) VALUES (%s, %s, %s, %s, %s)'
        try:
            q = self.conn.execute(sql, [body.values()])
            return self.output_json(body, code=200)
        except IntegrityError as e:
            return self.output_json({}, code=400)


class UsersMetaId(Restless):

    def get(self, id):
        conn = e.connect()
        q = conn.execute("SELECT * FROM User WHERE uuid = %s", [id])
        result = {'user': i for i in q.cursor.fetchall()}
        return result
