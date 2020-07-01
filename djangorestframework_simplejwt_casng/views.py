from .serializers import CASTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenViewBase


class CASTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = CASTokenObtainPairSerializer
