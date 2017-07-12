from django.db import models

class Donor(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    CPF = models.CharField(max_length=11, primary_key=True)
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    address = models.CharField(max_length=50)

class Donation(models.Model):
    value = models.IntegerField()
    donor_CPF = models.CharField(max_length=11, primary_key=True)
    recurring = models.BooleanField()
    

class TransactionResponse(models.Model):
    boletoURL = models.CharField(max_length=100)
    onlineDebitURL = models.CharField(max_length=100)
    authenticationURL = models.CharField(max_length=100)
    authCode = models.CharField(max_length=20)
    referenceNum = models.CharField(max_length=20)
    orderID = models.CharField(max_length=20)
    transactionID = models.CharField(max_length=20)
    transactionTimestamp = models.DateTimeField()
    responseCode = models.IntegerField()


