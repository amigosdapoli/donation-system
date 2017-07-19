from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Donor, Donation
from .serializers import DonorSerializer, DonationSerializer

class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all().order_by('CPF')
    serializer_class = DonorSerializer

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all().order_by('value')
    serializer_class = DonationSerializer

def donation_form(request):
	return render(request, 'dbwrapper/donation_form.html', {})
