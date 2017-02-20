import json
from uuid import uuid4
from flask import make_response
from flask_restful import Resource, reqparse
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from restless import Restless

class UsersMetaBase(Restless):
    def __init__(self, *args, **kwargs):
        super(UsersMetaBase, self).__init__(*args, **kwargs)
        self.data = {
            'first_name': None,
            'last_name': None,
            'username': None,
            'email': None,
            'uuid': None,
            'created': None,
            'modified': None
        }


class UsersMeta(UsersMetaBase):

    def get(self):
        q = self.conn.execute("SELECT * FROM User")
        results = [i[1:] for i in q.cursor.fetchall()]
        results = [self.merge_results(self.data, result) for result in results]
        return self.output_json({ "data": results }, code=200)

    def post(self):
        body = self.body(list(self.data.keys()))
        body['uuid'] = str(uuid4())
        timestamp = self.timestamp()
        body['created'] = timestamp
        body['modified'] = timestamp

        for key, value in body.items():
            if not value:
                return self.output_json(data={}, code=400)

        sql = 'INSERT INTO User (first_name, last_name, username, email, uuid, created, modified) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        try:
            q = self.conn.execute(sql, [body.values()])
            return self.output_json({ "data": body }, code=200)
        except IntegrityError as e:
            return self.output_json({}, code=400)


class UsersMetaId(UsersMetaBase):

    def get(self, id):
        q = self.conn.execute("SELECT * FROM User WHERE uuid = %s", [str(id)])
        try:
            results = [*q.cursor.fetchall()[0]][1:]
        except IndexError as e:
            return self.output_json({}, code=404)

        results = self.merge_results(self.data, results)
        return self.output_json({ "data": results }, code=200)

    def patch(self, id):
        body = self.body(list(self.data.keys()))
        body.pop('uuid')
        body.pop('created')
        body['modified'] = self.timestamp()

        sql_values = list(body.values())
        sql_values.append(str(id))
        sql = 'UPDATE User SET first_name=%s, last_name=%s, username=%s, email=%s, modified=%s WHERE uuid=%s'
        self.conn.execute(sql, sql_values)

        try:
            q = self.conn.execute("SELECT * FROM User WHERE uuid = %s", [str(id)])
            results = [*q.cursor.fetchall()[0]][1:]
        except IndexError as e:
            return self.output_json({}, code=404)

        results = self.merge_results(self.data, results)
        return self.output_json({ "data": results }, code=200)


    def delete(self, id):
        try:
            sql = 'DELETE FROM User WHERE uuid = %s'
            q = self.conn.execute(sql, [str(id)])
            return self.output_json({}, code=200)
        except IntegrityError as e:
            return self.output_json({}, code=404)
