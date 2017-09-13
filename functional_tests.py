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
		header_text = self.browser.find_element_by_name('nav_bar_title').text  
		self.assertIn('Doação', header_text) 

        # Donor types donation info
		# she identifies the dropdown box as to select which type of donation she wants to do
		monthly_donation = self.browser.find_element_by_xpath("//label[contains(text(),'Mensal')]")
        
		# She chooses the "Recorrente" type donation
		monthly_donation.click()

		# She identifies the text box to input donation value
		donation_input_box = self.browser.find_element_by_xpath("//label[contains(text(),'Valor da doação')]")
		
		# She sees a text box to input the donation value
		donation_input_box.send_keys('50')

		# She starts filling in personal information
		# First, she identifies the boxes to write her name and surname...
		name_input_box = self.browser.find_element_by_xpath("//label[contains(text(),'Nome')]")
		surname_input_box = self.browser.find_element_by_xpath("//label[contains(text(),'Sobrenome')]")

		# ...then, writes her name...		
		name_input_box.send_keys("Maria")
		
		# ...and surname.
		surname_input_box.send_keys("Silva")

		# Identifies the text box for her CNPJ...
		CPNJ_input_box = self.browser.find_element_by_xpath("//label[contains(text(),'CPF')]")
		
		# ... and inputs her own 
		CPNJ_input_box.send_keys("370.021.138-44") 

		# Identifies the text box for her phone number...
		phone_input_box = self.browser.find_element_by_xpath("//label[contains(text(),'Telefone')]")

		# ... and inputs hers
		phone_input_box.send_keys("998765432")

		# Identifies email text box
		email_input_box = self.browser.find_element_by_xpath("//label[contains(text(),'E-mail')]")
		
		# ...And inputs hers
		email_input_box.send_keys("maria.silva@gmail.com")

		# Identifies Address text box
		address_input_box = self.browser.find_element_by_xpath("//label[contains(text(),'Endereço')]")
	
		# ...and inputs hers
		address_input_box.send_keys("Avenia Faria Lima")

		# Identifies dropdown box to select payment method
		payment_method_label = self.browser.find_element_by_xpath("//label[@for='payment_method'][contains(text(),'Forma de pagamento')]")
		payment_method_box = self.browser.find_element_by_xpath("//select[@name='payment_method']")
		
		# ...evaluates her options...
		payment_method_CC_option = self.browser.find_element_by_xpath("//option[@value='CC']")
		self.assertIn("Cartão de crédito", payment_method_CC_option.text)
		payment_method_BB_option = self.browser.find_element_by_xpath("//option[@value='BB']")
		self.assertIn("Boleto bancário", payment_method_BB_option.text)
 
if __name__ == '__main__':
    unittest.main(warnings='ignore')
