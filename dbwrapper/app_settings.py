from django.conf import settings

MERCHANT_ID = getattr(settings, 'MERCHANT_ID', None)
MERCHANT_KEY = getattr(settings, 'MERCHANT_KEY', None)
GATEWAY_SANDBOX = getattr(settings, 'GATEWAY_SANDBOX', None)