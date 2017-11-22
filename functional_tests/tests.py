from django.test import LiveServerTestCase, Client
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
import time
import os

MAX_WAIT = 10


class NewDonorTest(LiveServerTestCase):
    def setUp(self):
        options = Options()
        #options.add_argument('-headless')
        self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', firefox_options=options)
        os.environ['RECAPTCHA_DISABLE'] = 'True'

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()  
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def fill_in_donation_fields_right(self):
        # She identifies the text box to input donation value
        donation_input_box = self.browser.find_element_by_id("id_donation_value")

        # She sees a text box to input the donation value
        donation_input_box.send_keys('50')

    def fill_in_personal_fields_right(self):
        # She starts filling in personal information
        # First, she identifies the boxes to write then she fill them in...

        # Identifies the text box for her phone number...
        name_input_box = self.browser.find_element_by_id("id_name")
        surname_input_box = self.browser.find_element_by_id("id_surname")
        CPNJ_input_box = self.browser.find_element_by_id("id_tax_id_no_pk_validation")
        phone_input_box = self.browser.find_element_by_id("id_phone_number")
        email_input_box = self.browser.find_element_by_id("id_email")

        # ...And inputs hers
        name_input_box.send_keys("Maria")
        surname_input_box.send_keys("Silva")
        CPNJ_input_box.send_keys("128.164.150-23")
        phone_input_box.send_keys("11998765432")
        email_input_box.send_keys("teste@gmail.com")

    def fill_in_cc_fields(self, credit_card_number):
        # Inputs Payment details
        cc_name = self.browser.find_element_by_id("id_name_on_card")
        cc_name.send_keys("Fulano de Tal")
        cc_number = self.browser.find_element_by_id("id_card_number")
        cc_number.send_keys(credit_card_number)
        cc_expire_month = self.browser.find_element_by_id("id_expiry_date_month")
        cc_expire_month.send_keys("12")
        cc_expire_year = self.browser.find_element_by_id("id_expiry_date_year")
        cc_expire_year.send_keys("18")
        cc_cvv = self.browser.find_element_by_id("id_card_code")
        cc_cvv.send_keys("123")

    def test_can_enter_donation_form_and_execute_donation(self):
        # Donor has heard about the opportunity to donate to the organization and enters the website
        self.browser.get(self.live_server_url)

        self.fill_in_donation_fields_right()
        self.fill_in_personal_fields_right()
        self.fill_in_cc_fields("4111111111111111")

        # Submit
        submit = self.browser.find_element_by_name("subbtn")
        submit.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn('Muito obrigado pela sua doação!', self.browser.page_source))

    def test_donor_fills_wrong_info_and_gets_list_of_fields_to_correct(self):
        """
        I will start testing only payment info and them try to make it more generic
        """
        # Donor has heard about the opportunity to donate to the organization and enters the website
        self.browser.get(self.live_server_url)

        self.fill_in_donation_fields_right()
        self.fill_in_personal_fields_right()
        self.fill_in_cc_fields("411111111111111") # Missing one number

        # Submit
        submit = self.browser.find_element_by_name("subbtn")
        submit.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn('Alguns dados precisam ser corrigidos:', self.browser.page_source))
        self.assertIn('Erro nas informações de cartão de crédito enviadas.', self.browser.page_source)

    def test_donor_fills_wrong_credit_card_and_gets_error(self):
        # Donor has heard about the opportunity to donate to the organization and enters the website
        self.browser.get(self.live_server_url)

        self.fill_in_donation_fields_right()
        self.fill_in_personal_fields_right()
        self.fill_in_cc_fields("4111111111111112")

        # Submit
        submit = self.browser.find_element_by_name("subbtn")
        submit.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn('Erro nas informações de cartão de crédito enviadas.', self.browser.page_source))

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
            "/admin/dbwrapper/donation",
            "/admin/dbwrapper/donor",
        ]
        for page in admin_pages:
            resp = client.get(page)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'<!DOCTYPE html', resp.content)

