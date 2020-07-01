from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken


class CASTokenObtainSerializer(serializers.Serializer):
    """
    This class is inspired by the `TokenObtainPairSerializer` and `TokenObtainSerializer`
    from the `rest_framework_simplejwt` package.
    """
    username_field = User.USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = None
        self.fields['ticket'] = serializers.CharField()
        self.fields['service'] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            'ticket': attrs['ticket'],
            'service': attrs['service'],
        }

        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError(f'Must implement `get_token` method for `{cls.__name__}` subclasses')


class CASTokenObtainPairSerializer(CASTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
