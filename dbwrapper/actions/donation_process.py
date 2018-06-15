#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os

from konduto import Konduto
from konduto.models import Order, Customer, Payment
from konduto.utils import RECOMMENDATION_DECLINE    
from maxipago import Maxipago
from maxipago.utils import payment_processors
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from dbwrapper.models import EmailBlacklist

from datetime import date
from random import randint

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AntiFraudService:
    def __init__(self):
        self.KONDUTO_PUBLIC_KEY = settings.KONDUTO_PUBLIC_KEY
        self.KONDUTO_PRIVATE_KEY = settings.KONDUTO_PRIVATE_KEY

    def get_customer(self, donor):
        customer_json = {
                "id": str(donor.donor_id),
                "name": "{} {}".format(donor.name, donor.surname),
                "tax_id": donor.tax_id,
                "phone1": str(donor.phone_number),
                "email": donor.email,
                "created_at": donor.created_at.strftime("%Y-%m-%d"),
                "vip": False}
        return Customer(**customer_json)

    def get_order(self, donation, customer, payment):
        order_json = {
            "id": str(donation.donation_id), # for tests str(randint(1,10000)), 
            "visitor": donation.visitor_id,
            "total_amount": float(donation.donation_value),
            "currency": "BRL",
            "installments": int(donation.installments),
            "ip": donation.donor_ip_address,
            "customer": self.get_customer(customer),
            "payment": self.get_payment(payment)
            }

        order = Order(**order_json)
        return order

    def get_payment(self, payment):
        payment_json = {
            "type": "credit", 
            "bin": payment.card_number[:6],
            "last4": payment.card_number[-4:],
            "expiration_date": "{MM}20{YY}".format(
                MM=payment.expiry_date_month,
                YY=payment.expiry_date_year),
            "status": "pending"}
        payment = Payment(**payment_json)
        return payment

    def analyze_order(self, donor, donation, payment):
        k = Konduto(self.KONDUTO_PUBLIC_KEY, self.KONDUTO_PRIVATE_KEY)
        order = self.get_order(donation, donor, payment)
        print(order.to_json())
        resp = k.analyze(order)
        return resp

class PaymentGateway:
    def __init__(self, data):
        merchant_id = settings.MERCHANT_ID
        gateway_key = settings.MERCHANT_KEY
        is_sandbox = settings.GATEWAY_SANDBOX
        logger.info("Using gateway with customer {} with Sandbox mode: {}".format(merchant_id, is_sandbox))
        self.gateway = Maxipago(merchant_id, gateway_key, sandbox=is_sandbox)
        self.payment_processor = None

        if is_sandbox:
            self.payment_processor = payment_processors.TEST  # TEST or REDECARD
        else:
            self.payment_processor = payment_processors.REDECARD  # TEST or REDECARD

        self.data = data
        data['processor_id'] = self.payment_processor

    def __get_error_msg(self, error_code):
        standard_error = """Infelizmente, não conseguimos processar a sua doação. """\
            """Nossa equipe já foi avisada. Por favor, tente novamente mais tarde."""
        error_msgs = {
            "1": "Transação negada.",
            "2": "Transação negada por duplicidade ou fraude.",
            "5": "Em análise manual de fraude.",
            "1022": "Erro na operadora do cartão.",
            "1024": "Erro nas informações de cartão de crédito enviadas.",
            "1025": "Erro nas credenciais.",
            "2048": "Erro interno do gateway de pagamento.",
            "4097": "Timeout do tempo de resposta da adquirente.",
        }
        return error_msgs.get(error_code, standard_error)

    def donate(self, is_recurring):
        if is_recurring:
            r = self.gateway.payment.create_recurring(**self.data)
        else:
            r = self.gateway.payment.direct(**self.data)
        if hasattr(r, 'response_message'):
            logger.info("Response message: {}".format(r.response_message))
        if hasattr(r, 'error_message'):
            logger.info("Response error message: {}".format(r.error_message))

        response = {}
        if r.captured is False:
            response['error_msg'] = self.__get_error_msg(r.response_code)
        response['was_captured'] = r.captured
        response['response_code'] = r.response_code
        response['order_id'] = r.order_id
        response['transaction_id'] = r.transaction_id
        return response


class DonationProcess:
    def __init__(self, donation, donor, payment):
        self.donation = donation
        self.donor = donor
        self.payment = payment

        self.payment_data = self.get_payment_data()
        self.gateway = PaymentGateway(self.payment_data)
        self.antifraud_service = AntiFraudService()

    def get_payment_data(self):
        payment_data = {
            'reference_num': self.donation.donation_id,
            'billing_name': self.payment.name_on_card,
            'billing_phone': self.donor.phone_number,
            'billing_email': self.donor.email,
            'card_number': self.payment.card_number,
            'card_expiration_month': self.payment.expiry_date_month,
            'card_expiration_year': self.payment.expiry_date_year,
            'card_cvv': self.payment.card_code,
            'charge_total': self.donation.donation_value,}

        if self.donation.is_recurring:
            payment_data['currency_code'] = u'BRL'
            payment_data['recurring_action'] = u'new'
            payment_data['recurring_start'] = date.today().strftime('%Y-%m-%d')
            payment_data['recurring_frequency'] = u'1'
            payment_data['recurring_period'] =  u'monthly'
            payment_data['recurring_installments'] = self.donation.installments
            payment_data['recurring_failure_threshold'] = u'2'

        if self.donor.phone_number is None:
            payment_data.pop('billing_phone', None)

        return payment_data

    def register_donation(self, is_recurring):
        response = self.gateway.donate(is_recurring)
        return response

    def is_blacklisted(self):
        qs = EmailBlacklist.objects.all()
        for item in qs:
            if item.email_pattern and (item.email_pattern in self.payment_data['billing_email']):
                self.donation.is_fraud = True
                self.donation.save()
        return None

    def is_fraud_external_service(self):
        resp_af = self.antifraud_service.analyze_order(self.donor, self.donation, self.payment)
        logger.info("Value (R$): {} Recommendation: {}".format(
            self.donation.donation_value, resp_af.recommendation))
        if resp_af.recommendation == RECOMMENDATION_DECLINE:
            self.donation.is_fraud = True
        return None

    def fraud_check(self):
        """
        Checks frauds using 2 methods.
        - e-mail blacklist
        - konduto antifraud service

        Marks donation as fraud

        Returns None
        """
        self.is_blacklisted()
        self.is_fraud_external_service()
        return None

    def notify_donation(self, donor, donation):
        self.__send_email_receipt(donor, donation)
        self.__notify_slack(donor, donation)

    def __notify_slack(self, donor, donation):
        slack_token = os.environ["SLACK_TOKEN"]
        slack_channel = os.environ["SLACK_CHANNEL"]

        requests.post(
            'https://slack.com/api/chat.postMessage',
            data = {
                'token': slack_token,
                'channel': slack_channel,
                'text': "Ocorreu uma doação de {0} reais!"
                    .format(donation.donation_value) 
            }
        )

    def __send_email_receipt(self, donor, donation):  
        template_data = {'first_name': donor.name,
                             'value': donation.donation_value,
                             'is_recurring': donation.is_recurring}
        to = donor.email

        plaintext = get_template('dbwrapper/successful_donation_email.txt')
        html_template = get_template('dbwrapper/successful_donation_email.html')

        subject = 'Obrigado pela sua contribuição!'
        text_content = plaintext.render(template_data)
        html_content = html_template.render(template_data)
        logger.info("Templates loaded")

        msg = EmailMultiAlternatives(
            subject,
            text_content,
            'no-reply@amigosdapoli.com.br',
            [to], )
        msg.attach_alternative(html_content, "text/html")
        response = msg.send(fail_silently=True)
        email_success = False
        if response == 1:
            email_success = True
        logger.info("E-mail sent successfuly: {}".format(email_success))
