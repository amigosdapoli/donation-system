from django.conf.urls import url, include
from . import views
from dbwrapper.views import DonationFormView
from dbwrapper.views import StatisticsView
from dbwrapper.views import DonationWizard

urlpatterns = [
    url(r'^$', DonationFormView.as_view(), name='donation_form'),
    url(r'^statistics', StatisticsView.as_view(), name='statistics'),
    url(r'^donation_wizard', DonationWizard.as_view(), name='donation_wizard'),
]

