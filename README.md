## Project Description

A JSON Web Token authentication plugin for the [Django REST Framework](https://www.django-rest-framework.org/) integrated with [cas-ng](https://djangocas.dev/docs/latest/).

### Requirements

* Python ( > 3.6)
* Django ( > 3.0)
* djangorestframework ( > 3.11 )
* djangorestframework-simplejwt ( >4.4.0 )
* django-cas-ng (> 4.1.1 )

### Installation

Install with pip:

```python
pip install djangorestframework-simplejwt-casng
```

Then in `settings.py`, add the package to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
		...
    'rest_framework',
    'django_cas_ng',
	  'rest_framework_simplejwt',
    'djangorestframework_simplejwt_casng',
]
```

 Then add `REST_FRAMEWORK`  and `AUTHENTICATION_BACKENDS` settings

```python
# REST framework settings
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

```python
# CAS Authentication
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)
CAS_SERVER_URL = 'https://cas.<your_cas_server>.com/cas/'
```

In the root `urls.py`, include the token url

```python
from djangorestframework_simplejwt_casng.views import CASTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    ...
    path('api/token/', CASTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ...
]
```

### Usage

Instead of `username` and `password`, `api/token/` requires `ticket` and `service` as parameters in the request body to send a POST request

```python
# request.POST
{
    "ticket": "<ticket_token>",
    "service": "<server_name>"
}

# response content
{  
  "access":"<access_token>",
  "refresh":"<refresh_token>"
}
```

### Settings

Other JWT settings could be used as shown in the [simplejwt documentation](https://pypi.org/project/djangorestframework-simplejwt/#settings)

```python
# Django project settings.py

from datetime import timedelta

...

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
```

