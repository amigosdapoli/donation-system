from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Donor, Donation
from .serializers import DonorSerializer, DonationSerializer
import json
class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all().order_by('CPF')
    serializer_class = DonorSerializer

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all().order_by('value')
    serializer_class = DonationSerializer


def donation_form(request):
    if request.method == 'POST':
        tax_id = request.POST.get('donor_tax_id')
        
        # tax id is required
        if not tax_id:
            raise Exception('tax_id need to be provided')
        donor = Donor.objects.filter(tax_id=tax_id).first()

        # creates  a new donor
        if not donor:
            new_donor = Donor()
            new_donor.tax_id = tax_id
            new_donor.name = request.POST.get('donor_name')
            new_donor.surname = request.POST.get('donor_surname')
            new_donor.save()
            donor = new_donor

        # Donation
        new_donation = Donation()
        new_donation.value = request.POST.get('donation_value')
        new_donation.donor_tax_id = donor.tax_id
        new_donation.recurring = False
        new_donation.save()
    return render(request, 'dbwrapper/donation_form.html', {})
