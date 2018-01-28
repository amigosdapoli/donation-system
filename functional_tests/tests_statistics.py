from django.test import LiveServerTestCase
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

    def test_userc_can_follow_statistics(self):
        # Donor has there is a campaign and wants to follow progress
        self.browser.get(self.live_server_url + "/statistics")

        self.assertIn('Resultados consolidados', self.browser.page_source)

