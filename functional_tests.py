from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
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
		header_text = self.browser.find_element_by_id('nav_bar_title').text  
		self.assertIn('Doação', header_text) 

        # Donor types donation info
		# she identifies the dropdown box as to select which type of donation she wants to do
		donation_type_dropdown_box = self.browser.find_element_by_xpath("//label[@for='donation_type'][contains(text(),'Tipo de doação')]")
        
		# She is invited to select the type of donation in a select box
		selectbox = self.browser.find_element_by_xpath("//select[@id='donation_type']")

		# She chooses the "Recorrente" type donation
		select = Select(self.browser.find_element_by_xpath("//select[@id='donation_type']"))
		select.select_by_visible_text("Recorrente")

		# She identifies the text box to input donation value
		donation_value_text_box_label = self.browser.find_element_by_xpath("//label[@for='donation_value'][contains(text(),'Valor da doação')]")
		
		# She sees a text box to input the donation value
		donation_input_box = self.browser.find_element_by_id('donation_value')
		donation_input_box.send_keys('50')

		# She starts filling in personal information
		# First, she identifies the boxes to write her name and surname...
		name_input_box_label = self.browser.find_element_by_xpath("//label[@for='donor_name'][contains(text(),'Nome')]")
		surname_input_box_label = self.browser.find_element_by_xpath("//label[@for='donor_surname'][contains(text(),'Sobrenome')]")

		# ...then, writes her name...		
		name_input_box = self.browser.find_element_by_id('donor_name')
		name_input_box.send_keys("Maria")
		
		# ...and surname.
		surname_input_box = self.browser.find_element_by_id('donor_surname')
		surname_input_box.send_keys("Silva")

		# Identifies the text box for her CNPJ...
		CPNJ_input_box_label = self.browser.find_element_by_xpath("//label[@for='donor_CNPJ'][contains(text(),'CNPJ')]")
		
		# ... and inputs her own 
		CPNJ_input_box = self.browser.find_element_by_xpath("//input[@type='text'][@id='donor_CNPJ']")
		CPNJ_input_box.send_keys("370.021.138-44") 

		# Identifies the text box for her phone number...
		phone_input_box_label = self.browser.find_element_by_xpath("//label[@for='donor_phone'][contains(text(),'Telefone')]")

		# ... and inputs hers
		phone_input_box = self.browser.find_element_by_xpath("//input[@type='text'][@id='donor_phone']")
		phone_input_box.send_keys("998765432")

		# Identifies email text box
		email_input_box_label = self.browser.find_element_by_xpath("//label[@for='donor_email'][contains(text(),'E-mail')]")
		
		# ...And inputs hers
		email_input_box = self.browser.find_element_by_xpath("//input[@type='text'][@id='donor_email']")
		email_input_box.send_keys("maria.silva@gmail.com")

		# Identifies Address text box
		address_input_box_label = self.browser.find_element_by_xpath("//label[@for='donor_address'][contains(text(),'Endereço')]")
	
		# ...and inputs hers
		address_input_box = self.browser.find_element_by_xpath("//input[@type='text'][@id='donor_address']")
		address_input_box.send_keys("Avenia Faria Lima")
 
if __name__ == '__main__':
    unittest.main(warnings='ignore')
