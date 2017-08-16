from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from dbwrapper.views import donation_form


class DonationPageTest(TestCase):

    def test_root_resolves_to_donation_form_view(self):
        found = resolve('/')
        self.assertEqual(found.func, donation_form)

    def test_donation_page_returns_correct_html(self):
        response = self.client.get('/')  
        html = response.content.decode('utf8')  
        self.assertTrue(html.startswith('<!DOCTYPE html>'))  
        self.assertIn('<title>Doação Amigos da Poli</title>', html)  
        self.assertTemplateUsed(response, 'dbwrapper/donation_form.html')

    def test_POST_request_has_response(self):
        data = {'donation': { 
                    'value': 10,
                    'type': 'recurrent',
		            'donor':{
		                'wants_anonimity': True,
		                'first_name': 'João',
		                'last_name': 'Batista Santos',
		                'tax_id':    66625911143,
		                'email': 'joaobatista@gmail.com',
		                'phone': 119957252267,
		                'course': 'Engenharia de Produção',
		                'graduation_year': 1970,
		                'source': 'friends',},
		            'card':{
		                'name': 'Joao batista santos',
		                'number': '1111222233334444',
		                'expiration': '2017-08-01',
		                'cvv': 123}
		            }}
        response = self.client.post('/', data=data)
        self.assertIn('status', response.content.decode())         



