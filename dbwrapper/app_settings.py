from django.conf import settings

MERCHANT_ID = getattr(settings, 'MERCHANT_ID', None)
MERCHANT_KEY = getattr(settings, 'MERCHANT_KEY', None)
GATEWAY_SANDBOX = getattr(settings, 'GATEWAY_SANDBOX', None)
KONDUTO_PUBLIC_KEY = getattr(settings, 'KONDUTO_PUBLIC_KEY', None)
KONDUTO_PRIVATE_KEY = getattr(settings, 'KONDUTO_PRIVATE_KEY', None)
