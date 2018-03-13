from django.test import LiveServerTestCase, Client
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

class StatisticsTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        os.environ['RECAPTCHA_DISABLE'] = 'True'

    def tearDown(self):
        self.browser.quit()

    def _create_user(self):
        self.username = "test_admin"
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.user = user

    def test_admin_pages(self):
        self._create_user()
        client = Client()
        client.login(username=self.username, password=self.password)
        admin_pages = [
            "/admin/",
            # put all the admin pages for your models in here.
            "/admin/auth/",
            "/admin/auth/group/",
            "/admin/auth/group/add/",
            "/admin/auth/user/",
            "/admin/auth/user/add/",
            "/admin/password_change/",
            "/admin/dbwrapper/donation/",
            "/admin/dbwrapper/donor/",
        ]
        for page in admin_pages:
            resp = client.get(page)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'<!DOCTYPE html', resp.content)

