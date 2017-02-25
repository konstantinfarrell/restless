import json
from uuid import uuid4
from flask import make_response
from flask_restful import Resource, reqparse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.exc import IntegrityError

from restless import Restless
from restless.settings import Base, session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    username = Column(String(100))
    email = Column(String(100))
    uuid = Column(String(64))
    created = Column(DateTime)
    modified = Column(DateTime)

    def json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'uuid': str(self.uuid),
            'created': str(self.created),
            'modified': str(self.modified)
        }


class UsersMetaBase(Restless):
    def __init__(self, *args, **kwargs):
        super(UsersMetaBase, self).__init__(*args, **kwargs)
        self.session = session

    def clean(self, data):
        data.pop('id', None)
        return data


class UsersMeta(UsersMetaBase):

    def get(self):
        users = self.session.query(User).all()
        results = [self.clean(i.json()) for i in users]
        return self.output_json({ "data": results }, code=200)

    def post(self):
        body = self.clean(self.body(list(User.__table__.columns.keys())))
        body['uuid'] = str(uuid4())
        timestamp = self.timestamp()
        body['created'] = timestamp
        body['modified'] = timestamp

        for key, value in body.items():
            if not value:
                return self.output_json(data={}, code=400)

        try:
            user = User(**body)
            self.session.add(user)
            self.session.commit()
            return self.output_json({ "data": body }, code=200)
        except IntegrityError as e:
            return self.output_json({}, code=400)


class UsersMetaId(UsersMetaBase):

    def get(self, id):
        user = self.session.query(User).filter_by(uuid=str(id)).all()
        results = [self.clean(i.json()) for i in user]
        return self.output_json({ "data": results }, code=200)

    def patch(self, id):
        body = self.body(list(User.__table__.columns.keys()))
        body.pop('uuid')
        body.pop('created')
        body['modified'] = self.timestamp()
        user = self.session.query(User).filter_by(uuid=str(id))
        results = user.first().json()
        body['id'] = results['id']
        user.update(body, synchronize_session='evaluate')
        self.session.commit()
        results = user.first().json()
        results.pop('id')
        return self.output_json({ "data": results }, code=200)


    def delete(self, id):
        try:
            self.session.query(User).filter_by(uuid=str(id)).delete(synchronize_session='evaluate')
            self.session.commit()
            return self.output_json({'data': []}, code=200)
        except IntegrityError as e:
            return self.output_json({}, code=404)
