from django import forms
from .models import Donor, Donation, PaymentTransaction
from localflavor.br.forms import BRCPFField


class FormDonor(forms.ModelForm):
    CPF_field = BRCPFField(label="CPF")
    is_anonymous = forms.BooleanField(required=False)

    class Meta:
        model = Donor
        fields = (
            "name", "surname", "phone_number", "email", "is_anonymous",
        )
        labels = {
            "name": "Nome",
            "surname": "Sobrenome",
            "phone_number": "Telefone",
            "email": "E-mail",
            "is_anonymous": "Gostaria de permanecer anônimo?",
        }


class FormDonation(forms.ModelForm):
    IS_RECURRING = (
        (0, "Pontual"),
        (1, "Mensal"),
    )
    is_recurring_field = forms.ChoiceField(choices=IS_RECURRING, label="Recorrência", widget=forms.RadioSelect())
    class Meta:
        model = Donation
        fields = ("value",)
        labels = {
            "value": "Valor da doação",

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
