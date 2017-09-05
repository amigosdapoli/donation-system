from django.shortcuts import render
from django.http import HttpResponse
from .models import Donor, Donation
from . import forms

import json

def donation_form(request):
    form = forms.FormDonor()
    donation_form = forms.FormDonation()
    
    if request.method == 'POST':
        form = forms.FormDonor(request.POST)
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
    return render(request, 'dbwrapper/donation_form.html', {'form':form,'donation_form':donation_form})
