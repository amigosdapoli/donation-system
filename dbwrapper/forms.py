from django import forms
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from .models import Donor, Donation, PaymentTransaction
from localflavor.br.forms import BRCPFField


class FormDonor(forms.ModelForm):
    tax_id_no_pk_validation = BRCPFField(
        widget=forms.TextInput(attrs={'placeholder': '000.000.000-00', 'class': 'cpf', }),
        label="CPF")
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '(XX) XXXXX XXXX', 'class': 'phone_with_ddd',}),
        min_length=10,
        max_length=11,
        label="Telefone (Opcional)")

    class Meta:
        model = Donor
        fields = (
            "name", "surname", "phone_number", "email", "course_taken", "course_year",
        )
        labels = {
            "name": "Nome:",
            "surname": "Sobrenome",
            "email": "E-mail",
            "course_taken": "Engenharia cursada (Opcional):",
            "course_year": "Ano de formatura (Opcional):",
        }


class FormDonation(forms.ModelForm):
    donation_value = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': '', 'class':'money'}),
        label="Valor da doação")

    class Meta:
        model = Donation
        fields = ("donation_value", "referral_channel", "installments")
        labels = {
            "donation_value": "Valor da doação",
            "referral_channel": "Por onde você conheceu o amigos da Poli? (Opcional)",
            "installments": "Duração",
        }


class FormPayment(forms.ModelForm):
    card_number = forms.CharField(
        widget=forms.NumberInput(attrs={'placeholder': 'XXXX XXXX XXXX XXXX'}),
        min_length=16,
        max_length=16,
        label="Número do cartão (VISA/MASTER)")
    captcha = ReCaptchaField(widget=ReCaptchaWidget(), label="Teste de segurança")

    class Meta:
        model = PaymentTransaction
        fields = ("name_on_card", "card_number", "expiry_date_month", "expiry_date_year", "card_code",)
        labels = {
            "name_on_card": "Nome do titular",
            "expiry_date_month": "Mês da data de vencimento",
            "expiry_date_year": "Ano da data de vencimento",
            "card_code": "Código de segurança",
        }
        widgets = {
            'card_code': forms.NumberInput(attrs={'placeholder': 'CVV'}),
        }