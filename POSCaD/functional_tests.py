from selenium import webdriver
import unittest

class NewDonorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_form_url(self):
        # just checks if the url is correct
        self.broswer.get('http://localhost:8000/doar')

if __name__== '__main__:':
    unittest.main(warnings='ignore')
