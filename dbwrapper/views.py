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
        visitor_id = request.POST.get('visitorID', '')

        if donation_form.is_valid() and donor_form.is_valid() and payment_form.is_valid():
            
            # Tax id is required
            if not tax_id:
                raise Exception('donor_tax_id need to be provided')
            donor = Donor.objects.filter(tax_id=tax_id).first()
            logger.debug("Donor already exists?: {}".format(donor))
            
            # Creates a new donor
            if not donor:
                donor = donor_form.save(commit=False)
                donor.tax_id = tax_id
                if request.POST.get('is_anonymous') == "Sim":
                    donor.is_anonymous = True
                else:
                    donor.is_anonymous = False
            
            donor.save()
            logger.info("Donor created: {}".format(donor.donor_id))

            # Creates a new donation
            donation = donation_form.save(commit=False)
            donation.donor = donor
            donation.donor_tax_id = donor.tax_id
            donation.donor_ip_address = request.META['REMOTE_ADDR']
            donation.visitor_id = visitor_id
            if request.POST.get('is_recurring') == "Mensal":
                donation.is_recurring = True
                donation.installments = donation_form.cleaned_data['installments']
            else:
                donation.is_recurring = False
                donation.installments = 1
            donation.campaign_name = donation_form.cleaned_data['campaign_name']
            donation.campaign_group = donation_form.cleaned_data['campaign_group']
            donation.save()

            # Creates a new payment
            payment = payment_form.save(commit=False)

            logger.info("Donation is recurring: {}".format(donation.is_recurring))
            logger.info("Donation value: {}".format(donation.donation_value))

            dp = DonationProcess(donation, donor, payment)
            dp.fraud_check()
            if donation.is_fraud:
                logger.info("Donor is blacklisted")                
                payment_form.add_error(None,
                                       "Erro nas informações de cartão de crédito enviadas.")
            else:
                try:
                    response = dp.register_donation(donation.is_recurring)
                    #donation = Donation.objects.get(donation_id=donation.donation_id)
                    if response['was_captured']:
                        donation.was_captured = response['was_captured']
                        donation.response_code = response['response_code']
                        donation.order_id = response['order_id']
                        donation.nsu_id = response['transaction_id']
                        donation.save()

                        logger.info("Preparing to send e-mail receipt...")
                        dp.send_email_receipt(donor, donation)

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
