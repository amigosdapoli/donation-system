from django.conf.urls import url, include
from . import views
from rest_framework import routers

#router = routers.DefaultRouter()
#router.register(r'donors/', views.DonorViewSet)
#router.register(r'donations/', views.DonationViewSet)

urlpatterns = [
    #url(r'^$', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.donation_form, name='donation_form'),
]
