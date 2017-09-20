from django.shortcuts import render
from .models import Donor, Donation, PaymentTransaction
from maxipago import Maxipago
from .configuration import Configuration
from datetime import date
import logging
from random import randint
from dbwrapper.forms import FormDonor, FormDonation, FormPayment


import json

def donation_form(request):
    donor_form = FormDonor()
    donation_form = FormDonation()
    payment_form = FormPayment()
    
    if request.method == 'POST':
        donor_form = FormDonor(request.POST)
        tax_id = request.POST.get('CPF_field')

        if donor_form.is_valid():
            # tax id is required
            if not tax_id:
                raise Exception('donor_tax_id need to be provided')
            donor = Donor.objects.filter(tax_id=tax_id).first()

            # creates  a new donor
            if not donor:
                new_donor = Donor()
                new_donor.tax_id = tax_id
                new_donor.name = request.POST.get('name')
                new_donor.surname = request.POST.get('surname')
                new_donor.phone_number = request.POST.get('phone_number')
                new_donor.email = request.POST.get('email')
                new_donor.save()
                donor = new_donor

            # Payment
            new_payment = PaymentTransaction()
            new_payment.name_on_card = request.POST.get("name_on_card")
            new_payment.card_number = request.POST.get("card_number")
            new_payment.expiry_date_month = request.POST.get("expiry_date_month")
            new_payment.expiry_date_year = request.POST.get("expiry_date_year")
            new_payment.card_code = request.POST.get("card_code")
            new_payment.save()

            # Donation
            new_donation = Donation()
            new_donation.value = request.POST.get('value')
            new_donation.donor_tax_id = donor.tax_id
            new_donation.recurring = False
            new_donation.save()

            # Process payment
            config = Configuration()
            maxipago_id = config.get("payment", "merchant_id")
            maxipago_key = config.get("payment", "merchant_key")
            maxipago_sandbox = config.get("payment", "sandbox")
            logging.info("Using Maxipago with customer {}".format(maxipago_id))
            maxipago = Maxipago(maxipago_id, maxipago_key, sandbox=maxipago_sandbox)

            REFERENCE = randint(1, 100000)
            response = maxipago.payment.direct(
                processor_id=u'1', # TEST, REDECARD = u'1', u'2'
                reference_num=REFERENCE,
                billing_name=u'Fulano de Tal',
                billing_address1=u'Rua das Alamedas, 123',
                billing_city=u'Rio de Janeiro',
                billing_state=u'RJ',
                billing_zip=u'20345678',
                billing_country=u'RJ',
                billing_phone=u'552140634666',
                billing_email=u'fulano@detal.com',
                card_number='4111111111111111',
                card_expiration_month=u'02',
                card_expiration_year=date.today().year + 3,
                card_cvv='123',
                charge_total='100.00',
            )

            logging.info("Response authorized: ".format(response.authorized))
            logging.info("Response captured: ".format(response.captured))
            if response.authorized and response.captured:
                donation = Donation.objects.get(donation_id=new_donation.donation_id)
                donation.order_id = response.order_id
                donation.nsu_id = response.transaction_id
                donation.save()

                # if sucess: update donation with transaction status and ids
                return render(request, 'dbwrapper/successful_donation.html')
            else:
                raise Exception('Payment not captured')
                # update donation with failed


    return render(request, 'dbwrapper/donation_form.html', {'donor_form':donor_form,'donation_form':donation_form, 'payment_form':payment_form})

