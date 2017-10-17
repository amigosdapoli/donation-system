from django.conf.urls import url, include
from . import views
from dbwrapper.views import DonationFormView

urlpatterns = [
    url(r'^', DonationFormView.as_view(), name='donation_form'),
]
