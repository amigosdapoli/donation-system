from selenium import webdriver
import unittest

class NewDonorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')

    def tearDown(self):
        self.browser.quit()

    def test_form_url(self):
        # Donor has heard about the opportunity to donate to the organization and enters the website
        self.browser.get('http://localhost:8000/doar/donation_form')

        # She notices the page title and header mention to-do lists
        self.assertIn('Amigos da Poli', self.browser.title) 
 
if __name__ == '__main__':
    unittest.main(warnings='ignore')
