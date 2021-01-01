import time

from tests import TestBase
from flask import json, current_app


class TestAuth(TestBase):
    def test_login(self):
        self.client.post("/api/auth/register", json={
            'email': 'ari@test.com', 'password': 'apple',
            'name': 'Test' + str(time.time()), 'zip': '01606'
        })
        response = self.client.post("/api/auth/login", json={
            'email': 'ari@test.com', 'password': 'apple'
        })
        data = json.loads(response.get_data(as_text=True))
        assert "Login successful" == data["msg"]

    def test_login_failed(self):
        self.client.post("/api/auth/register", json={
            'email': 'ari@test.com', 'password': 'apple',
            'name': 'Test' + str(time.time()), 'zip': '01606'
        })
        response = self.client.post("/api/auth/login", json={
            'email': 'ari@test.com', 'password': 'Apple'
        })
        data = json.loads(response.get_data(as_text=True))
        assert "Bad email or password" == data["msg"]

    def test_register(self):
        response = self.client.post("/api/auth/register", json={
            'email': 'test' + str(time.time()) + '@test.com', 'password': 'apple',
            'name': 'Test' + str(time.time()), 'zip': '01606'
        })
        data = json.loads(response.get_data(as_text=True))
        assert "Register successful" == data["msg"]

    def test_register_failed(self):
        response = self.client.post("/api/auth/register", json={
            'email': 'ari@test.com', 'password': 'apple',
            'name': 'Test' + str(time.time()), 'zip': '01606'
        })
        data = json.loads(response.get_data(as_text=True))
        assert "Account already created" == data["msg"]

    def test_update_email(self):
        email = 'test' + str(time.time()) + '@test.com'
        self.client.post("/api/auth/register", json={
            'email': email, 'password': 'apple',
            'name': 'Test' + str(time.time()), 'zip': '01606'
        })
        put_data = {
            "email": "ari" + str(time.time()) + "@test.com"
        }
        with self.user_set(current_app, self.get_user(email)):
            profile_request = self.client.put("/api/auth/update_email",
                                              json=put_data)
            profile_data = json.loads(profile_request.get_data(as_text=True))
            assert "Email update successful" == profile_data["msg"]

    def test_update_email_failed(self):
        email = 'text' + str(time.time()) + '@test.com'
        self.client.post("/api/auth/register", json={
            'email': email, 'password': 'apple',
            'name': 'Test' + str(time.time()), 'zip': '01606'
        })
        put_data = {
            "email": email
        }
        with self.user_set(current_app, self.get_user(email)):
            profile_request = self.client.put("/api/auth/update_email",
                                              json=put_data)
            assert profile_request.status_code == 400

    def test_update_password(self):
        email = 'test' + str(time.time()) + '@test.com'
        self.client.post("/api/auth/register", json={
            'email': email, 'password': 'apple',
            'name': 'Test' + str(time.time()), 'zip': '01606'
        })
        put_data = {
            "current_password": "apple",
            "new_password": "banana"
        }
        with self.user_set(current_app, self.get_user(email)):
            profile_request = self.client.put("/api/auth/update_password",
                                              json=put_data)
            profile_data = json.loads(profile_request.get_data(as_text=True))
            assert "Password update successful" == profile_data["msg"]

    def test_update_password_failed(self):
        email = 'text' + str(time.time()) + '@test.com'
        self.client.post("/api/auth/register", json={
            'email': email, 'password': 'apple',
            'name': 'Test' + str(time.time()), 'zip': '01606'
        })
        put_data = {
            "current_password": "apple",
            "new_password": "apple"
        }
        with self.user_set(current_app, self.get_user(email)):
            profile_request = self.client.put("/api/auth/update_password",
                                              json=put_data)
            assert profile_request.status_code == 400
