from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewDonorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_donation_form_and_execute_donation(self):
        # Donor has heard about the opportunity to donate to the organization and enters the website
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        #self.assertIn('Doação', self.browser.title)
        #header_text = self.browser.find_element_by_name('nav_bar_title').text
        #self.assertIn('Doação', header_text)

        # Donor types donation info
        # she identifies the dropdown box as to select which type of donation she wants to do
        select_elm = self.browser.find_element_by_id("id_is_recurring_field")
        for option in select_elm.find_elements_by_tag_name('option'):
            if option.text == 'Pontual':
                # She chooses the "Recorrente" type donation
                option.click()  # select() in earlier versions of webdriver
                break

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
        CPNJ_input_box.send_keys("37002113844")

        # Identifies the text box for her phone number...
        phone_input_box = self.browser.find_element_by_xpath("//label[contains(text(),'Telefone')]")

        # ... and inputs hers
        phone_input_box.send_keys("11998765432")

        # Identifies email text box
        email_input_box = self.browser.find_element_by_xpath("//label[contains(text(),'E-mail')]")

        # ...And inputs hers
        email_input_box.send_keys("maria.silva@gmail.com")

        # Inputs Payment details
        cc_name = self.browser.find_element_by_id("id_name_on_card")
        cc_name.send_keys("Fulano de Tal")
        cc_number = self.browser.find_element_by_id("id_card_number")
        cc_number.send_keys("4111111111111111")
        cc_expire_month = self.browser.find_element_by_id("id_expiry_date_month")
        cc_expire_month.send_keys("12")
        cc_expire_year = self.browser.find_element_by_id("id_expiry_date_year")
        cc_expire_year.send_keys("18")
        cc_cvv = self.browser.find_element_by_id("id_card_code")
        cc_cvv.send_keys("123")

        # Submit
        submit = self.browser.find_element_by_name("subbtn")
        submit.send_keys(Keys.ENTER)
        time.sleep(5)

        self.assertIn('bem sucedida', self.browser.page_source)





