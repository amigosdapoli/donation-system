from django import forms
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from .models import Donor, Donation, PaymentTransaction
from localflavor.br.forms import BRCPFField


class FormDonor(forms.ModelForm):
    CPF_field = BRCPFField(label="CPF")

    class Meta:
        model = Donor
        fields = (
            "name", "surname", "phone_number", "email",
        )
        labels = {
            "name": "Nome",
            "surname": "Sobrenome",
            "phone_number": "Telefone",
            "email": "E-mail",
        }


class FormDonation(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ("donation_value",)
        labels = {
            "donation_value": "Valor da doação",
        }


class FormPayment(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget(), label="Teste de segurança")
    class Meta:
        model = PaymentTransaction
        fields = ("name_on_card", "card_number", "expiry_date_month", "expiry_date_year", "card_code",)
        labels = {
            "name_on_card": "Nome do titular",
            "card_number": "Número do cartão",
            "expiry_date_month": "Mês da data de vencimento",
            "expiry_date_year": "Ano da data de vencimento",
            "card_code": "Código de segurança",
        }
        widgets = {
            'card_number': forms.NumberInput(attrs={'placeholder': 'XXXX XXXX XXXX XXXX'}),
            'card_code': forms.NumberInput(attrs={'placeholder': 'CVV'}),
        }