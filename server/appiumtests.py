from time import sleep, time

import requests
from flask import request, session, jsonify, g
from selenium import webdriver

from app import create_app, db
from app.models import Sport, User
from tests import AppiumTestConfig

from multiprocessing import Process


class TestAppium:
    def setup_class(self):
        self.app = create_app(AppiumTestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = db
        self.db.create_all()
        soccer = Sport("soccer")
        soccer.save_to_db()
        self.server = Process(target=self.app.run)  # terminate 'kill `lsof -i :5000`'
        self.server.start()
        self.driver = webdriver.Firefox(executable_path='/Users/aristotelfani/Downloads/geckodriver')
        self.driver.get('http://localhost:8080')

    def teardown_class(self):
        db.drop_all()
        self.app_context.pop()
        self.server.terminate()
        self.driver.close()

    def login(self, email):
        sleep(1)
        el = self.driver.find_element_by_id('login-email')
        el.send_keys(email)

        el = self.driver.find_element_by_id('login-password')
        el.send_keys('apple')

        el = self.driver.find_element_by_id('login-btn')
        el.click()
        sleep(2)

    def register(self, email=None):
        sleep(2)

        el = self.driver.find_element_by_id('register-btn')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_id('register-name')
        el.clear()
        el.send_keys('Ari' + str(time()))

        el = self.driver.find_element_by_id('register-zip')
        el.clear()
        el.send_keys('01606')

        el = self.driver.find_element_by_id('register-email')
        el.clear()
        if email is not None:
            el.send_keys(email)
        else:
            el.send_keys('test' + str(time()) + '@test.com')

        el = self.driver.find_element_by_id('register-password')
        el.clear()
        el.send_keys('apple')

        el = self.driver.find_element_by_id('register-confirm')
        el.clear()
        el.send_keys('apple')

        el = self.driver.find_element_by_id('register-button')
        el.click()
        sleep(1)

    def logout(self):
        el = self.driver.find_element_by_id('open-left-panel')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_id('logout-button')
        el.click()
        sleep(1)


class TestAppiumLogin(TestAppium):
    def test_login(self):
        email = 'test' + str(time()) + '@test.com'
        response = requests.post("http://127.0.0.1:5000/api/auth/register", json={
            'email': email, 'password': 'apple',
            'name': 'Test' + str(time()), 'zip': '01606'
        })
        assert "Register successful" == response.json()["msg"]

        self.login(email)

        el = self.driver.find_element_by_class_name('title-large-text')
        assert el.text == "Events"

        self.logout()

    def test_register(self):
        self.register()

        el = self.driver.find_element_by_class_name('title-large-text')
        assert el.text == "Events"

        self.logout()


class TestAppiumProfile(TestAppium):

    def test_update_profile(self):
        self.register()

        el = self.driver.find_element_by_id('open-left-panel')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_id('profile')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_id('first-name')
        el.clear()
        el.send_keys('Ari')

        el = self.driver.find_element_by_id('last-name')
        el.clear()
        el.send_keys('Fani')

        el = self.driver.find_element_by_id('current-job')
        el.clear()
        el.send_keys('Apple')

        el = self.driver.find_element_by_id('current-zip')
        el.clear()
        el.send_keys('01606')

        el = self.driver.find_element_by_id('about-me')
        el.clear()
        el.send_keys('Software Engineer')

        el = self.driver.find_element_by_partial_link_text('Save')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_class_name("toast-text")
        assert el.text == "Saved profile info"

    def test_update_password(self):
        el = self.driver.find_element_by_id('update-password-btn')
        el.click()

        el = self.driver.find_element_by_id('current-password')
        el.send_keys('apple')

        el = self.driver.find_element_by_id('new-password')
        el.send_keys('banana')

        el = self.driver.find_element_by_class_name('dialog-button-bold')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_class_name("toast-text")
        assert el.text == "Password update successful"

    def test_update_email(self):
        el = self.driver.find_element_by_id('update-email-btn')
        el.click()

        el = self.driver.find_element_by_id('update-email')
        el.send_keys('ari' + str(time()) + '@test.com')

        el = self.driver.find_element_by_class_name('dialog-button-bold')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_class_name("toast-text")
        assert el.text == "Email update successful"

        el = self.driver.find_element_by_class_name('popup-close')
        el.click()
        sleep(1)

        self.logout()


class TestAppiumEvents(TestAppium):

    def test_new_event(self):
        self.register()

        el = self.driver.find_element_by_id('new-event')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_id('ne-title')
        el.clear()
        el.send_keys("Soccer")

        el = self.driver.find_element_by_id('ne-address')
        el.clear()
        el.send_keys('123 Main St.')

        el = self.driver.find_element_by_id('ne-time')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_id('current-day')
        el.click()

        el = self.driver.find_element_by_class_name('calendar-close')
        el.click()

        el = self.driver.find_element_by_id('create-event-btn')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_class_name("toast-text")
        assert el.text == "Successfully saved new event"
        sleep(1)

    def test_view_event(self):
        el = self.driver.find_element_by_class_name('item-title-row')
        el.click()

        el = self.driver.find_element_by_id('event-title')
        assert el.text == "Soccer"

        el = self.driver.find_element_by_class_name('popup-close')
        el.click()
        sleep(1)

    def test_view_my_events(self):
        title = "Soccer"
        el = self.driver.find_element_by_id('open-left-panel')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_id('my-events')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_link_text(title)
        assert el.text == title
        el.click()
        sleep(1)

        el = self.driver.find_element_by_id('event-title')
        assert el.text == title

        el = self.driver.find_element_by_class_name('close-view-event')
        el.click()
        sleep(1)

    def test_edit_my_event(self):
        el = self.driver.find_element_by_class_name('edit-btn')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_id('ee-title')
        el.clear()
        el.send_keys("Soccer" + str(int(time())))

        el = self.driver.find_element_by_id('ee-address')
        el.clear()
        el.send_keys('124 Main St.')

        el = self.driver.find_element_by_id('edit-event-btn')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_class_name("toast-text")
        assert el.text == "Successfully updated event"
        sleep(1)

        el = self.driver.find_element_by_class_name('close-my-events')
        el.click()
        sleep(1)

        self.logout()
