#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from dbwrapper.forms import FormDonor, FormDonation, FormPayment
from .models import Donor, Donation, PaymentTransaction
from .configuration import Configuration

from maxipago import Maxipago
from maxipago.utils import payment_processors
from datetime import date
import logging

logger = logging.getLogger(__name__)


class DonationFormView(View):
    """
    This class
    """
    def get(self, request):
        donor_form = FormDonor()
        donation_form = FormDonation()
        payment_form = FormPayment()

        return render(request, 'dbwrapper/donation_form.html', {'donor_form':donor_form,'donation_form':donation_form, 'payment_form':payment_form})

    def post(self, request):
        donor_form = FormDonor(request.POST)
        payment_form = FormPayment(request.POST)
        donation_form = FormDonation(request.POST)

        tax_id = request.POST.get('tax_id_no_pk_validation').replace(".","").replace("-","")

        if donation_form.is_valid() and donor_form.is_valid() and payment_form.is_valid():
            # tax id is required
            if not tax_id:
                raise Exception('donor_tax_id need to be provided')
            donor = Donor.objects.filter(tax_id=tax_id).first()

            # creates  a new donor
            if not donor:
                new_donor = Donor()
                new_donor.tax_id = tax_id
                new_donor.name = donor_form.cleaned_data['name']
                new_donor.surname = donor_form.cleaned_data['surname']
                new_donor.phone_number = donor_form.cleaned_data['phone_number']
                new_donor.email = donor_form.cleaned_data['email']
                new_donor.course_taken = donor_form.cleaned_data['course_taken']
                new_donor.course_year = donor_form.cleaned_data['course_year']
                if request.POST.get('is_anonymous') == "Sim":
                    new_donor.is_anonymous = True
                else:
                    new_donor.is_anonymous = False
                new_donor.save()
                donor = new_donor

            # Donation
            new_donation = Donation()
            new_donation.donation_value = donation_form.cleaned_data['donation_value']
            new_donation.donor = donor
            new_donation.donor_tax_id = donor.tax_id
            new_donation.referral_channel = donation_form.cleaned_data['referral_channel']
            if request.POST.get('is_recurring') == "Mensal":
                new_donation.is_recurring = True
                new_donation.installments = donation_form.cleaned_data['installments']
            else:
                new_donation.is_recurring = False
            new_donation.save()

            # Payment
            new_payment = PaymentTransaction()
            new_payment.name_on_card = payment_form.cleaned_data['name_on_card']
            new_payment.save()

            # Process payment
            maxipago_id = settings.MERCHANT_ID
            maxipago_key = settings.MERCHANT_KEY
            maxipago_sandbox = settings.GATEWAY_SANDBOX
            print("Using Maxipago with customer {}".format(maxipago_id))
            maxipago = Maxipago(maxipago_id, maxipago_key, sandbox=maxipago_sandbox)

            REFERENCE = new_donation.donation_id
            if maxipago_sandbox:
                payment_processor = payment_processors.TEST  # TEST or REDECARD
            else:
                payment_processor = payment_processors.REDECARD # TEST or REDECARD

            print("Donation is recurring: {}".format(new_donation.is_recurring))

            try:
                if new_donation.is_recurring:
                    data = {
                        'processor_id':payment_processor,
                        'reference_num':REFERENCE,
                        'billing_name':payment_form.cleaned_data['name_on_card'],
                        'billing_phone':donor.phone_number,
                        'billing_email':donor.email,
                        'card_number':payment_form.cleaned_data['card_number'],
                        'card_expiration_month':payment_form.cleaned_data['expiry_date_month'],
                        'card_expiration_year':payment_form.cleaned_data['expiry_date_year'],
                        'card_cvv':payment_form.cleaned_data['card_code'],
                        'charge_total':new_donation.donation_value,

                        'currency_code':u'BRL',
                        'recurring_action':u'new',
                        'recurring_start':date.today().strftime('%Y-%m-%d'),
                        'recurring_frequency':u'1',
                        'recurring_period':u'monthly',
                        'recurring_installments':new_donation.installments,
                        'recurring_failure_threshold':u'2',
                    }
                    if donor.phone_number is None:
                        data.pop('billing_phone', None)
                    response = maxipago.payment.create_recurring(**data)
                else:
                    data ={'processor_id': payment_processor,
                        'reference_num':REFERENCE,
                        'billing_name':payment_form.cleaned_data['name_on_card'],
                        'billing_phone':donor.phone_number,
                        'billing_email':donor.email,
                        'card_number':payment_form.cleaned_data['card_number'],
                        'card_expiration_month':payment_form.cleaned_data['expiry_date_month'],
                        'card_expiration_year':payment_form.cleaned_data['expiry_date_year'],
                        'card_cvv':payment_form.cleaned_data['card_code'],
                        'charge_total':new_donation.donation_value,}
                    if donor.phone_number is None:
                        data.pop('billing_phone', None)
                    response = maxipago.payment.direct(**data)

                print("Response code: {}".format(response.response_code))
                if hasattr(response, 'response_message'):
                    print("Response message: {}".format(response.response_message))
                if hasattr(response, 'error_message'):
                    print("Response error message: {}".format(response.error_message))
                print("Response authorized: {}".format(response.authorized))
                print("Response captured: {}".format(response.captured))

                donation = Donation.objects.get(donation_id=new_donation.donation_id)
                if response.authorized and response.captured:
                    donation.was_captured = response.captured
                    donation.response_code = response.response_code
                    donation.order_id = response.order_id
                    donation.nsu_id = response.transaction_id
                    donation.save()

                    d = {'first_name': donor.name,
                         'value': new_donation.donation_value,
                         'is_recurring': donation.is_recurring}

                    plaintext = get_template('dbwrapper/successful_donation_email.txt')
                    html_template = get_template('dbwrapper/successful_donation_email.html')

                    subject = 'Obrigado pela sua contribuição!'
                    text_content = plaintext.render(d)
                    html_content = html_template.render(d)

                    msg = EmailMultiAlternatives(
                        subject,
                        text_content,
                        'no-reply@amigosdapoli.com.br',
                        [donor.email], )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send(fail_silently=True)
                    return render(request, 'dbwrapper/successful_donation.html')
                else:
                    payment_form.add_error(None,
                        "Infelizmente, não conseguimos processar a sua doação. Nossa equipe já foi avisada. Por favor, tente novamente mais tarde.")
                    donation.was_captured = response.captured
                    donation.response_code = response.response_code
                    donation.save()

            except:
                payment_form.add_error(None,
                    "Infelizmente, não conseguimos processar a sua doação. Nossa equipe já foi avisada. Por favor, tente novamente mais tarde.")

        return render(
                request,
                'dbwrapper/donation_form.html',
                {'donor_form': donor_form, 'donation_form': donation_form, 'payment_form': payment_form})

