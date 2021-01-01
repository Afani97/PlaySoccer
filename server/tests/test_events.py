from flask import json, current_app, g
from tests import TestBase
import time
import uuid


class TestEvents(TestBase):
    def test_get_events(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            events_request = self.client.get("/api/events/list?page=1")
            events_data = json.loads(events_request.get_data(as_text=True))
            assert "Successfully retrieved events" == events_data["msg"]

    def test_get_events_failed(self):
        self.client.get("/api/auth/logout")
        with self.user_set(current_app, None):
            event = self.client.get("/api/events/list?page=1")
            events_data = json.loads(event.get_data(as_text=True))
            assert "User not authorized" == events_data["msg"]

    def test_create_new_event(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            post_data = {
                "title": "Soccer 3v3",
                "where": "123 Main St. ",
                "when": int(time.time()),
                "max_players": "5",
                "additional_info": "Bring a soccer net"
            }
            events_request = self.client.post("/api/events/new_event",
                                              json=post_data)
            events_data = json.loads(events_request.get_data(as_text=True))
            assert "Successfully saved new event" == events_data["msg"]

    def test_create_new_event_failed(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            post_data = {
                "where": "123 Main St. ",
                "when": int(time.time()),
                "max_players": "5",
                "additional_info": "Bring a soccer net"
            }
            events_request = self.client.post("/api/events/new_event",
                                              json=post_data)
            assert events_request.status_code == 400

    def test_get_event_details(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            post_data = {
                "title": "Soccer 3v3",
                "where": "123 Main St. ",
                "when": int(time.time()),
                "max_players": "5",
                "additional_info": "Bring a soccer net"
            }
            events_request = self.client.post("/api/events/new_event",
                                              json=post_data)
            events_data = json.loads(events_request.get_data(as_text=True))
            event_id = events_data["event"]["id"]
            events_request = self.client.get("/api/events/" + event_id)
            events_data = json.loads(events_request.get_data(as_text=True))
            assert "Successfully retrieved event" == events_data["msg"]

    def test_get_event_details_failed(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            events_request = self.client.get("/api/events/" + str(uuid.uuid4()))
            events_data = json.loads(events_request.get_data(as_text=True))
            assert "Error retrieving event details" == events_data["msg"]

    def test_join_event(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            post_data = {
                "title": "Soccer 3v3",
                "where": "123 Main St. ",
                "when": int(time.time()),
                "max_players": "5",
                "additional_info": "Bring a soccer net"
            }
            events_request = self.client.post("/api/events/new_event",
                                              json=post_data)
            events_data = json.loads(events_request.get_data(as_text=True))
            event_id = events_data["event"]["id"]
            self.client.post("/api/auth/register", json={
                'email': 'test' + str(time.time()) + '@test.com', 'password': 'apple',
                'name': 'Test' + str(time.time()), 'zip': '01606'
            })
            put_data = {
                "event_id": event_id
            }
            events_request = self.client.put("/api/events/join_event",
                                             json=put_data)
            events_data = json.loads(events_request.get_data(as_text=True))
            assert "Successfully added to event" == events_data["msg"]

    def test_join_event_failed(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            events_request = self.client.put("/api/events/join_event",
                                             json={"event_id": 1})
            assert events_request.status_code == 400

    def test_edit_event(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            post_data = {
                "title": "Soccer 3v3",
                "where": "12 Main St. ",
                "when": int(time.time()),
                "max_players": "0",
                "additional_info": ""
            }
            events_request = self.client.post("/api/events/new_event",
                                              json=post_data)
            events_data = json.loads(events_request.get_data(as_text=True))
            event_id = events_data["event"]["id"]
            put_data = {
                "title": "Soccer",
                "where": "123 Main St. ",
                "when": int(time.time()),
                "max_players": "5",
                "additional_info": "Bring a soccer net"
            }
            events_request = self.client.put("/api/events/" + event_id + "/edit",
                                             json=put_data)
            events_data = json.loads(events_request.get_data(as_text=True))
            assert "Successfully updated event" == events_data["msg"]

    def test_edit_event_failed(self):
        email = self.get_login()
        with self.user_set(current_app, self.get_user(email)):
            put_data = {
                "title": "Soccer 3v3",
                "where": "123 Main St. ",
                "when": int(time.time()),
                "max_players": "5",
                "additional_info": "Bring a soccer net"
            }
            events_request = self.client.put("/api/events/" + str(uuid.uuid4()) + "/edit",
                                             json=put_data)
            assert events_request.status_code == 401
