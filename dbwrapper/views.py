#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.db.models import Count, Min, Sum, Avg

from dbwrapper.forms import FormDonor, FormDonation, FormPayment
from .models import Donor, Donation, PaymentTransaction
from dbwrapper.actions import DonationProcess

from datetime import date
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DonationFormView(View):
    """
    This class
    """

    def get(self, request):
        donor_form = FormDonor()
        donation_form = FormDonation()
        payment_form = FormPayment()

        campaign_name = request.GET.get('campaign_name', None)
        campaign_group = request.GET.get('campaign_group', None)
        campaign_data = {"campaign_name": campaign_name,
                         "campaign_group": campaign_group}

        data = {'donor_form': donor_form,
                'donation_form': donation_form,
                'payment_form': payment_form,
                'campaign_data': campaign_data}

        return render(request, 'dbwrapper/donation_form.html', data)


    def post(self, request):
        donor_form = FormDonor(request.POST)
        payment_form = FormPayment(request.POST)
        donation_form = FormDonation(request.POST)

        tax_id = request.POST.get('tax_id_no_pk_validation', '').replace(".","").replace("-","")

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
            new_donation.donor_ip_address = request.META['REMOTE_ADDR']
            new_donation.referral_channel = donation_form.cleaned_data['referral_channel']
            if request.POST.get('is_recurring') == "Mensal":
                new_donation.is_recurring = True
                new_donation.installments = donation_form.cleaned_data['installments']
            else:
                new_donation.is_recurring = False
            new_donation.campaign_name = donation_form.cleaned_data['campaign_name']
            new_donation.campaign_group = donation_form.cleaned_data['campaign_group']
            new_donation.save()

            # Payment
            new_payment = PaymentTransaction()
            new_payment.name_on_card = payment_form.cleaned_data['name_on_card']
            new_payment.save()

            logger.info("Donation is recurring: {}".format(new_donation.is_recurring))
            logger.info("Donation value {}".format(donation_form.cleaned_data['donation_value']))

            payment_data = {
                'reference_num': new_donation.donation_id,
                'billing_name': payment_form.cleaned_data['name_on_card'],
                'billing_phone': donor.phone_number,
                'billing_email': donor.email,
                'card_number': payment_form.cleaned_data['card_number'],
                'card_expiration_month': payment_form.cleaned_data['expiry_date_month'],
                'card_expiration_year': payment_form.cleaned_data['expiry_date_year'],
                'card_cvv': payment_form.cleaned_data['card_code'],
                'charge_total': new_donation.donation_value,}

            if new_donation.is_recurring:
                payment_data['currency_code'] = u'BRL'
                payment_data['recurring_action'] = u'new'
                payment_data['recurring_start'] = date.today().strftime('%Y-%m-%d')
                payment_data['recurring_frequency'] = u'1'
                payment_data['recurring_period'] =  u'monthly'
                payment_data['recurring_installments'] = new_donation.installments
                payment_data['recurring_failure_threshold'] = u'2'

            if donor.phone_number is None:
                payment_data.pop('billing_phone', None)

            dp = DonationProcess(payment_data)
            #if dp.is_fraud():
            try:
                response = dp.register_donation(new_donation.is_recurring)
                donation = Donation.objects.get(donation_id=new_donation.donation_id)
                if response['was_captured']:
                    donation.was_captured = response['was_captured']
                    donation.response_code = response['response_code']
                    donation.order_id = response['order_id']
                    donation.nsu_id = response['transaction_id']
                    donation.save()

                    template_data = {'first_name': donor.name,
                         'value': new_donation.donation_value,
                         'is_recurring': donation.is_recurring}
                    logger.info("Preparing to send e-mail receipt with {}".format(template_data))
                    dp.send_email_receipt(donor.email, template_data)

                    return render(request, 'dbwrapper/successful_donation.html')
                else:
                    logger.info("Else")
                    payment_form.add_error(None,
                                           response['error_msg'])
                    donation.was_captured = response['was_captured']
                    donation.response_code = response['response_code']
                    donation.save()

            except Exception as e:
                logger.error('Failed to execute payment', exc_info=True)
                payment_form.add_error(None,
                                       "Infelizmente, não conseguimos processar a sua doação. Nossa equipe já foi avisada. Por favor, tente novamente mais tarde.")

        data = {'donor_form': donor_form,
                'donation_form': donation_form,
                'payment_form': payment_form,
                'campaign_data': {"campaign_name": request.POST.get('campaign_name', ''),
                                  "campaign_group": request.POST.get('campaign_group', '')}}

        return render(request, 'dbwrapper/donation_form.html', data)


class StatisticsView(View):
    """
    This class
    """
    def get(self, request):
        queryset = Donation.objects.exclude(
            campaign_name__isnull=True).exclude(
            was_captured=False).exclude(
            campaign_name="None").exclude(
            campaign_name="none").exclude(
            campaign_group="None").filter(
            campaign_name="dia-de-doar").filter(
            donation_value__gte=5.0).filter(
            created_at__month='11').values('campaign_group').annotate(donor_count=Count('donor_tax_id', distinct=True)).order_by('-donor_count')
        logger.info(queryset)

        labels = []
        data = []

        if not queryset:
            data = [0] # avoid graph from breaking
        else:
            for row in queryset:
                labels.append(row["campaign_group"].replace('-', ' ').replace('_', ' ').title())
                data.append(row["donor_count"])

        email_to_exclude = '@yopmail.com'
        total_qs = Donation.objects.exclude(
            donor__email__endswith=email_to_exclude).exclude(
            donor__name__icontains='nadjon').exclude(
            donor__surname__icontains='aquino').exclude(
            donor__name__icontains='nome').filter(
            was_captured=True).filter(
            donation_value__gte=5.0).filter(
            created_at__month='11').aggregate(Count('donor_tax_id', distinct=True))

        base_donors = 95
        total = base_donors + total_qs['donor_tax_id__count']
        logger.info(total)

        template_data = {"total": total,
                         "labels": labels,
                         "data": data,
                         "x_axis_max": max(data)+1}
        logger.info(template_data)


        return render(request, 'dbwrapper/statistics.html', template_data)
