from app import db
from sqlalchemy_utils import UUIDType, EncryptedType, EmailType, PasswordType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from sqlalchemy import Integer, String, Text, DateTime, LargeBinary
import uuid
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))

SECRET_KEY = os.environ.get('SECRET_KEY')

events = db.Table('events',
                  db.Column('user_id', UUIDType(binary=False), db.ForeignKey('user.id'), primary_key=True),
                  db.Column('event_id', UUIDType(binary=False), db.ForeignKey('event.id'), primary_key=True)
                  )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(UUIDType(binary=False), primary_key=True)
    email = db.Column(EmailType, nullable=False)
    password = db.Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt']
    ), nullable=False)
    first_name = db.Column(EncryptedType(db.Unicode, SECRET_KEY, AesEngine, 'pkcs5'), nullable=False)
    last_name = db.Column(EncryptedType(db.Unicode, SECRET_KEY, AesEngine, 'pkcs5'), nullable=False)
    current_zip = db.Column(EncryptedType(db.Unicode, SECRET_KEY, AesEngine, 'pkcs5'), nullable=False)
    current_job = db.Column(EncryptedType(db.Unicode, SECRET_KEY, AesEngine, 'pkcs5'), nullable=True)
    about_me = db.Column(EncryptedType(db.Unicode, SECRET_KEY, AesEngine, 'pkcs5'), nullable=True)
    events = db.relationship('Event', secondary=events, lazy='subquery', backref=db.backref('users', lazy=True))
    image = db.Column(LargeBinary, nullable=True)

    def __init__(self, email, password, first_name, last_name, current_zip):
        self.id = uuid.uuid4()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.current_zip = current_zip

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {"id": self.id,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "current_zip": self.current_zip,
                "current_job": self.current_job,
                "about_me": self.about_me}

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(UUIDType(binary=False), primary_key=True)
    title = db.Column(String(256), nullable=False)
    location = db.Column(String(256), nullable=False)
    description = db.Column(Text, nullable=True)
    timestamp = db.Column(DateTime, index=True, nullable=False)
    created_by_user_id = db.Column(UUIDType(binary=False), db.ForeignKey('user.id'), nullable=False)
    sports_id = db.Column(UUIDType(binary=False), db.ForeignKey('sport.id'), nullable=False)
    member_limit_count = db.Column(Integer, nullable=True)

    def __init__(self, title, location, timestamp, created_by_user_id, sports_id):
        self.id = uuid.uuid4()
        self.title = title
        self.location = location
        self.timestamp = timestamp
        self.created_by_user_id = created_by_user_id
        self.sports_id = sports_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        user = User.query.filter_by(id=self.created_by_user_id).first()
        users = []
        for u in self.users:
            users.append(u.to_json())
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "description": self.description,
            "timestamp": self.timestamp,
            "created_by": self.created_by_user_id,
            "created_by_user_name": user.first_name + " " + user.last_name,
            "created_by_user_company": user.current_job,
            "sports_id": self.sports_id,
            "current_members": users,
            "member_limit_count": self.member_limit_count
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Sport(db.Model):
    __tablename__ = 'sport'
    id = db.Column(UUIDType(binary=False), primary_key=True)
    title = db.Column(String(256), nullable=False)

    def __init__(self, title):
        self.id = uuid.uuid4()
        self.title = title

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
