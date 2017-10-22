from django.db import models
from django.utils import timezone


COURSE_CHOICES = (
    (None, 'Escolha...'),
    ('Não cursei engenharia na Poli', 'Não cursei engenharia na Poli'),
    ('Engenharia Ambiental', 'Engenharia Ambiental'),
    ('Engenharia Civil', 'Engenharia Civil'),
    ('Engenharia de Computação', 'Engenharia de Computação'),
    ('Engenharia de Materiais', 'Engenharia de Materiais'),
    ('Engenharia de Minas', 'Engenharia de Minas'),
    ('Engenharia de Petróleo', 'Engenharia de Petróleo'),
    ('Engenharia de Produção', 'Engenharia de Produção'),
    ('Engenharia Elétrica', 'Engenharia Elétrica'),
    ('Engenharia Mecânica', 'Engenharia Mecânica'),
    ('Engenharia Mecatrônica', 'Engenharia Mecatrônica'),
    ('Engenharia Metalurgica', 'Engenharia Metalurgica'),
    ('Engenharia Naval', 'Engenharia Naval'),
    ('Engenharia Química', 'Engenharia Química'),
)

years = [(str(x), str(x)) for x in range(1950, 2026)]
years.insert(0, (None, 'Escolha...'))
YEAR_CHOICES = years

class Donor(models.Model):
    donor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    tax_id = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=15, default=None, null=True, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50)
    course_taken = models.CharField(max_length=30, choices=COURSE_CHOICES, default=None, null=True, blank=True)
    course_year = models.CharField(max_length=4, default=None, null=True, choices=YEAR_CHOICES, blank=True)
    is_anonymous = models.BooleanField(default=False)

REFERRAL_CHOICES = (
    (None, 'Escolha...'),
    ('Indicação de amigos', 'Indicação de amigos'),
    ('Facebook', 'Facebook'),
    ('Linkedin', 'Linkedin'),
    ('Site de buscas (Google)', 'Site de buscas (Google)'),
    ('Mídias externas (rádio/jornal/revista)', 'Mídias externas (rádio/jornal/revista)'),
)

INSTALLMENT_CHOICES=[(12,'1 ano'),
                     (48,'Irei notificar o Amigos da Poli via e-mail (contato@amigosdapoli.com.br)')]

class Donation(models.Model):
    donation_id = models.AutoField(primary_key=True, default=None)
    donation_value = models.IntegerField()
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donor_tax_id = models.CharField(max_length=15)
    is_recurring = models.NullBooleanField(null=True, default=False)
    was_captured = models.NullBooleanField(null=True, default=False)
    response_code = models.IntegerField(default=None, blank=True, null=True)
    error_message = models.TextField(default=None, blank=True, null=True)
    order_id = models.CharField(max_length=35, default=None, blank=True, null=True)
    nsu_id = models.CharField(max_length=10, default=None, blank=True, null=True)
    installments = models.IntegerField(default=1, null=True, choices=INSTALLMENT_CHOICES)
    created_at = models.DateTimeField(editable=False, default=None, null=True)
    updated_at = models.DateTimeField(default=None, null=True)
    referral_channel = models.CharField(max_length=40,choices=REFERRAL_CHOICES, default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.donation_id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Donation, self).save(*args, **kwargs)


class PaymentTransaction(models.Model):
    name_on_card = models.CharField(max_length=30)
    card_number = models.CharField(max_length=16)
    expiry_date_month = models.CharField(max_length=2)
    expiry_date_year = models.CharField(max_length=2)
    card_code = models.CharField(max_length=3)

    def save(self, *args, **kwargs):
        """
        Override save to make sure no credit card info is saved accidentally
        """
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
