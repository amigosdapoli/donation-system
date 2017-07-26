from selenium import webdriver
import unittest

class NewDonorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_donation_form_and_execute_donation(self):
        # Donor has heard about the opportunity to donate to the organization and enters the website
        self.browser.get('http://localhost:8000/')

        # She notices the page title and header mention to-do lists
        self.assertIn('Doação', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text  
        self.assertIn('Doação', header_text) 

        # Donor types donation info
        # She is invited to enter a to-do item straight away
        selectbox = self.browser.find_element_by_id('donation_type')  
        #self.assertEqual(
        #    inputbox.get_attribute('placeholder'),
        #    'Enter a to-do item'
        #)

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        # inputbox.send_keys('Buy peacock feathers') 
 
if __name__ == '__main__':
    unittest.main(warnings='ignore')
