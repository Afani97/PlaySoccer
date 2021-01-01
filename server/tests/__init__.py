from flask import json, appcontext_pushed, g, current_app, request, session, jsonify
from app import create_app, db
from config import TestConfig, AppiumTestConfig
from app.models import Sport, User
import time
from contextlib import contextmanager


class TestBase:
    def setup_class(self):
        self.app = create_app(TestConfig)
        app = self.app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        soccer = Sport("soccer")
        soccer.save_to_db()

    def teardown_class(self):
        db.drop_all()
        self.app_context.pop()

    def get_login(self):
        email = 'test' + str(time.time()) + '@test.com'
        self.client.post("/api/auth/register", json={
            'email': email, 'password': 'apple',
            'name': 'Test' + str(time.time()), 'zip': '01606'
        })
        return email

    def get_user(self, email):
        user = getattr(g, 'user', None)
        if user is None:
            if email:
                user = User.query.filter_by(email=email).first()
            g.user = user
        return user

    @contextmanager
    def user_set(self, app, user):
        def handler(sender, **kwargs):
            g.user = user

        with appcontext_pushed.connected_to(handler, app):
            yield

