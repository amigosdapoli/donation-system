from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from dbwrapper.views import DonationFormView


class DonationPageTest(TestCase):

    def test_root_resolves_to_donation_form_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, DonationFormView)

    def test_donation_page_returns_correct_html(self):
        response = self.client.get('/')  
        html = response.content.decode('utf8')
        self.assertIn('<title>Doação Amigos da Poli</title>', html)  
        self.assertTemplateUsed(response, 'dbwrapper/donation_form.html')

    def test_POST_request_has_response(self):
        data = {'donation_value': 30,
				'donor_tax_id': 1,
				'donor_name': 'Fulano',
				'donor_surname': 'de Tal'}
        response = self.client.post('/', data=data)
        self.assertTemplateUsed(response, 'dbwrapper/donation_form.html')

    def test_payment(self):
        data = {'donation_value': 30,
				'donor_tax_id': "369.023.248-16",
				'donor_name': 'Fulano',
				'donor_surname': 'de Tal'}
        response = self.client.post('/', data=data)
        self.assertTemplateUsed(response, 'dbwrapper/donation_form.html')
