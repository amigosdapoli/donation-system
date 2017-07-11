from django.db import models

class Donor(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    CPF = models.CharField(max_length=11, primary_key=True)
    phone_number = models.CharField()
    email = models.CharField()
    address = models.CharField()

class Donation(models.Model):
    value = models.IntegerField()
    donor_CPF = models.CharField(max_length=11)
    recurring = models.BoolField()

class TransactionResponse(models.Model):
    boletoURL =
    onlineDebitURL =
    authenticationURL =
    authCode =
    referenceNum =
    orderID =
    transactionID =
    transactionTimestamp = 
    responseCode =

class TransactionRequest(models.Model):
# Create your models here.
