from django import forms
from .models import Donor, Donation, PaymentTransaction
from localflavor.br.forms import BRCPFField


class FormDonor(forms.ModelForm):
    email_checker = forms.EmailField(label='Insira o e-mail novamente')
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
        exclude = ["donation_id", "donor_tax_id", "order_id", "nsu_id"]
        labels = {
            "value": "Valor da doação",
            "recurring": "Mensal"
        }


class FormPayment(forms.ModelForm):

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
