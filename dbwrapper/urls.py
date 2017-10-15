from django.conf.urls import url, include
from . import views
from dbwrapper.views import DonationFormView

urlpatterns = [
    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', DonationFormView.as_view(), name='donation_form'),
]
