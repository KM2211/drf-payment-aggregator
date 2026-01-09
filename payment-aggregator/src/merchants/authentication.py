from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Merchant

class APIKeyAuthentication(BaseAuthentication):
    """
    DRF Custom Authentication
    Authenticates requests using X-API-KEY header
    """

    def authenticate(self, request):
        api_key = request.headers.get("X-API-KEY")

        if not api_key:
            return None  # DRF will treat as unauthenticated

        try:
            merchant = Merchant.objects.get(api_key=api_key, is_active=True)
        except Merchant.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")

        return (merchant, None)
