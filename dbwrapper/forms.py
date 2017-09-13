from django import forms
from .models import Donor, Donation
from localflavor.br.forms import BRCPFField


class FormDonor(forms.ModelForm):
    email_checker = forms.EmailField(label='Insira o e-mail novamente')
    CPF_field = BRCPFField(label = "CPF")

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
        exclude = ["donation_id", "donor_tax_id"]
        labels = {
            "value": "Valor da doação",
            "recurring": "Mensal"
        }
