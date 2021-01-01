import time

from flask import json, current_app
from tests import TestBase


class TestProfile(TestBase):
    def test_get_profile_info(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            profile_request = self.client.get("/api/profile/")
            profile_data = json.loads(profile_request.get_data(as_text=True))
            assert "Successfully get profile" == profile_data["msg"]

    def test_get_profile_info_failed(self):
        self.client.get("/api/auth/logout")
        with self.user_set(current_app, None):
            profile_request = self.client.get("/api/profile/")
            profile_data = json.loads(profile_request.get_data(as_text=True))
            assert "User not authorized" == profile_data["msg"]

    def test_save_profile_info(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            put_data = {
                "first_name": "Ari",
                "last_name": "Fani",
                "current_job": "N/A",
                "current_zip": "00000",
                "about_me": "Something interesting"
            }
            profile_request = self.client.put("/api/profile/",
                                                         json=put_data)
            profile_data = json.loads(profile_request.get_data(as_text=True))
            assert "Successfully updated profile" == profile_data["msg"]

    def test_save_profile_info_failed(self):
        self.client.get("/api/auth/logout")
        with self.user_set(current_app, None):
            put_data = {
                "first_name": "Ari",
                "current_zip": "00000"
            }
            profile_request = self.client.put("/api/profile/", json=put_data)
            profile_data = json.loads(profile_request.get_data(as_text=True))
            assert "User not authorized" == profile_data["msg"]

    def test_save_profile_info_failed_no_json(self):
        self.client.get("/api/auth/logout")
        with self.user_set(current_app, None):
            profile_request = self.client.put("/api/profile/")
            assert profile_request.status_code == 401

    def test_get_my_events(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            post_data = {
                "title": "Soccer 3v3",
                "where": "123 Main St. ",
                "when": int(time.time()),
                "max_players": "5",
                "additional_info": "Bring a soccer net"
            }
            self.client.post("/api/events/new_event",
                                        json=post_data)
            events_request = self.client.get("/api/profile/events")
            events_data = json.loads(events_request.get_data(as_text=True))
            assert "Successfully retrieved user's events" == events_data["msg"]
            assert len(events_data["events"]) == 1

    def test_get_my_events_none(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            events_request = self.client.get("/api/profile/events")
            events_data = json.loads(events_request.get_data(as_text=True))
            assert len(events_data["events"]) == 0
