from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from dbwrapper.views import donation_form


class DonationPageTest(TestCase):

    def test_root_resolves_to_donation_form_view(self):
        found = resolve('/doar/donation_form')
        self.assertEqual(found.func, donation_form)

    def test_donation_page_returns_correct_html(self):
        request = HttpRequest()  
        response = donation_form(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.startswith('<!DOCTYPE html>'))  
        self.assertIn('<title>Doação Amigos da Poli</title>', html)  
        self.assertTrue(html.endswith('</html>'))          

