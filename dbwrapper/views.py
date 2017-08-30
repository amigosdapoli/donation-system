from django.shortcuts import render
from django.http import HttpResponse
from .models import Donor, Donation, PaymentTransaction
from maxipago import Maxipago
from .configuration import Configuration

import logging
from random import randint


def donation_form(request):
    if request.method == 'POST':
        tax_id = request.POST.get('donor_tax_id')
        
        # tax id is required
        if not tax_id:
            raise Exception('donor_tax_id need to be provided')
        donor = Donor.objects.filter(tax_id=tax_id).first()

        # creates  a new donor
        if not donor:
            new_donor = Donor()
            new_donor.tax_id = tax_id
            new_donor.name = request.POST.get('donor_name')
            new_donor.surname = request.POST.get('donor_surname')
            new_donor.save()
            donor = new_donor

        # Payment
        new_payment = PaymentTransaction()
        new_payment.name_on_card = "Fulano de Tal"
        new_payment.card_number = "1111222233334444"
        new_payment.expiry_date = "2018-01"
        new_payment.card_code = "123"

        # Donation
        new_donation = Donation()
        new_donation.value = request.POST.get('donation_value')
        new_donation.donor_tax_id = donor.tax_id
        new_donation.recurring = False
        new_donation.save()

        # Process payment
        config = Configuration()
        maxipago_id = config.get("payment", "merchant_id")
        maxipago_key = config.get("payment", "merchant_key")
        logging.info("Using Maxipago with customer {}".format(maxipago_id))
        maxipago = Maxipago(maxipago_id, maxipago_key)

        REFERENCE = randint(1, 100000)
        response = maxipago.payment.direct(
            processor_id=1,
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
            pass
            # if sucess: update donation with transaction status and ids
        else:
            raise Exception('Payment not captured')
            # update donation with failed

    return render(request, 'dbwrapper/donation_form.html', {})
