from django import forms
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from .models import Donor, Donation, PaymentTransaction
from .models import INSTALLMENT_CHOICES
from localflavor.br.forms import BRCPFField


class FormDonor(forms.ModelForm):
    tax_id_no_pk_validation = BRCPFField(
        widget=forms.TextInput(attrs={'placeholder': '000.000.000-00', 'class': 'cpf', }),
        label="CPF")
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '(XX) XXXXX XXXX', 'class': 'phone_with_ddd',}),
        max_length=16,
        label="Telefone")

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        phone_number = phone_number.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        return phone_number

    class Meta:
        model = Donor
        fields = (
            "name", "surname", "phone_number", "email", "course_taken", "course_year",
        )
        labels = {
            "name": "Nome:",
            "surname": "Sobrenome",
            "email": "E-mail",
            "course_taken": "Engenharia cursada (Opcional)",
            "course_year": "Ano de formatura (Opcional)",
        }


class FormDonation(forms.ModelForm):
    donation_value = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        localize=True,
        widget=forms.TextInput(attrs={'placeholder': '', 'class': 'money'}),
        label="Valor da doação (R$) ")
    installments = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'id_installments_select'}),
        choices=INSTALLMENT_CHOICES,
        label="Duração",
        initial=INSTALLMENT_CHOICES[1][1])
    campaign_name = forms.CharField(
        widget=forms.HiddenInput(),
        required = False
    )

    class Meta:
        model = Donation
        fields = ("donation_value", "referral_channel", "installments", "campaign_name", "campaign_group")
        labels = {
            "donation_value": "Valor da doação (R$)",
            "referral_channel": "Como você conheceu o Amigos da Poli? (Opcional)",
        }


class FormPayment(forms.ModelForm):
    card_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'XXXX XXXX XXXX XXXX', 'class': 'card_number'}),
        min_length=16,
        max_length=19,
        label="Número do cartão (VISA/MASTER)")
    captcha = ReCaptchaField(widget=ReCaptchaWidget(), label="Teste de segurança")
    expiry_date_month = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'MM', 'class': 'expiry_date_month'}),
        label="Mês da data de vencimento")
    expiry_date_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'YY', 'class': 'expiry_date_year'}),
        label="Ano da data de vencimento")

    def clean_card_number(self):
        card_number = self.cleaned_data.get("card_number")
        card_number = card_number.replace(" ", "")
        return card_number

    class Meta:
        model = PaymentTransaction
        fields = ("name_on_card", "card_number", "expiry_date_month", "expiry_date_year", "card_code",)
        labels = {
            "name_on_card": "Nome do titular",
            "card_code": "Código de segurança",
        }
        widgets = {
            'card_code': forms.NumberInput(attrs={'placeholder': 'CVV'}),
        }