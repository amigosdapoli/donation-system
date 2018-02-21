#!/usr/bin/python
import logging
from maxipago import Maxipago
from maxipago.utils import payment_processors
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from dbwrapper.models import EmailBlacklist

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
        standard_error = "Infelizmente, não conseguimos processar a sua doação. Nossa equipe já foi avisada. Por favor, tente novamente mais tarde."
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
    def __init__(self, payment_data):
        self.payment_data = payment_data
        self.gateway = PaymentGateway(self.payment_data)

    def register_donation(self, is_recurring):
        response = self.gateway.donate(is_recurring)
        return response

    def fraud_check(self):
        qs = EmailBlacklist.objects.all()
        for item in qs:
            if item.email_pattern in self.payment_data['billing_email']:
                return True
        return False

    def send_email_receipt(self, to, template_data):
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
