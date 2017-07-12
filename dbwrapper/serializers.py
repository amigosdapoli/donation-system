from .models import Donor, Donation
from rest_framework import serializers

class DonorSerializer(serializers.HyperlinkedModelSerializer):
    model = Donor
    fields = ('name', 'surname', 'CPF', 'phone_number', 'email', 'address')

class DonationSerializer(serializers.HyperlinkedModelSerializer):
    model = Donation
    fields = ('value', 'donor_CPF', 'recurring')
