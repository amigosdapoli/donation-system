from django.db import models


class Donor(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    tax_id = models.CharField(max_length=11, primary_key=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50)


class Donation(models.Model):
    donation_id = models.AutoField(primary_key=True, default=None)
    value = models.IntegerField()
    donor_tax_id = models.CharField(max_length=11)
    recurring = models.BooleanField()
    order_id = models.CharField(max_length=35, default=None, blank=True, null=True)
    nsu_id = models.CharField(max_length=10, default=None, blank=True, null=True)


class PaymentTransaction(models.Model):
    name_on_card = models.CharField(max_length=30)
    card_number = models.CharField(max_length=16)
    expiry_date_month = models.CharField(max_length=2)
    expiry_date_year = models.CharField(max_length=2)
    card_code = models.CharField(max_length=3)

    def save(self, *args, **kwargs):
        pass

    class Meta:
        managed = False

class TransactionResponse(models.Model):
    boleto_url = models.CharField(max_length=100)
    onlineDebit_url = models.CharField(max_length=100)
    authentication_url = models.CharField(max_length=100)
    auth_code = models.CharField(max_length=20)
    reference_num = models.CharField(max_length=20)
    order_id = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=20)
    transaction_timestamp = models.DateTimeField()
    response_code = models.IntegerField()




