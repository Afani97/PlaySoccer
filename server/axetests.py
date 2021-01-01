from time import sleep, time
import os

from flask import request, session, g, jsonify
from selenium import webdriver
from axe_selenium_python import Axe

from app import create_app, db
from app.models import Sport, User
from tests import AppiumTestConfig

import multiprocessing as mp


class TestAxe:
    def setup_class(self):
        self.app = create_app(AppiumTestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = db
        self.db.create_all()
        soccer = Sport("soccer")
        soccer.save_to_db()
        self.server = mp.Process(target=self.app.run)  # terminate 'kill `lsof -i :5000`'
        self.server.start()
        self.driver = webdriver.Firefox(executable_path='/Users/aristotelfani/Downloads/geckodriver')
        self.driver.get('http://localhost:8080')
        self.axe = Axe(self.driver)

    def teardown_class(self):
        db.drop_all()
        os.remove('a11y.json')
        self.app_context.pop()
        self.server.terminate()
        self.driver.close()

    def setup_method(self, method):
        open('a11y.json', 'w').close()

    def axe_test(self, context=None):
        self.axe.inject()
        if context:
            results = self.axe.run(context=context)
            self.axe.write_results(results, 'a11y.json')
            assert len(results["violations"]) == 0, self.axe.report(results["violations"])
        else:
            results = self.axe.run()
            self.axe.write_results(results, 'a11y.json')
            assert len(results["violations"]) == 0, self.axe.report(results["violations"])

    def login(self, email):
        sleep(1)
        el = self.driver.find_element_by_id('login-email')
        el.send_keys(email)

        el = self.driver.find_element_by_id('login-password')
        el.send_keys('apple')

        el = self.driver.find_element_by_id('login-btn')
        el.click()
        sleep(1)

    def register(self, email=None):
        sleep(2)
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


class TestAxeLogin(TestAxe):
    def test_login(self):
        self.axe_test()

    def test_register(self):
        sleep(2)

        el = self.driver.find_element_by_id('register-btn')
        el.click()
        sleep(1)

        self.axe_test()

    def test_home(self):
        self.register()

        self.axe_test()

    def test_profile(self):
        el = self.driver.find_element_by_id('open-left-panel')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_id('profile')
        el.click()
        sleep(1)

        self.axe_test({
            "include": [["#profile-page"]],
            "exclude": [["#home-page"]]
        })

        el = self.driver.find_element_by_class_name('popup-close')
        el.click()
        sleep(1)

    def test_new_event(self):
        el = self.driver.find_element_by_id('new-event')
        el.click()
        sleep(2)

        self.axe_test({
            "include": [["#new-event-page"]],
            "exclude": [["#home-page"]]
        })

    def test_view_event(self):
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

        el = self.driver.find_element_by_class_name('item-title-row')
        el.click()

        self.axe_test({
            "include": [["#view-event-page"]],
            "exclude": [["#home-page"]]
        })

        el = self.driver.find_element_by_class_name('popup-close')
        el.click()
        sleep(1)

    def test_view_my_events(self):
        el = self.driver.find_element_by_id('open-left-panel')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_id('my-events')
        el.click()
        sleep(1)

        el = self.driver.find_element_by_link_text("Soccer")
        el.click()
        sleep(1)

        self.axe_test({
            "include": [["#my-events-page"]],
            "exclude": [["#home-page", "#view-event-page"]]
        })

        el = self.driver.find_element_by_class_name('close-view-event')
        el.click()
        sleep(1)

    def test_edit_my_event(self):
        el = self.driver.find_element_by_class_name('edit-btn')
        el.click()
        sleep(1)

        self.axe_test({
            "include": [["#edit-event-page"]],
            "exclude": [["#home-page", "#my-events-page"]]
        })

        el = self.driver.find_element_by_class_name('close-edit-page')
        el.click()
        sleep(1)







