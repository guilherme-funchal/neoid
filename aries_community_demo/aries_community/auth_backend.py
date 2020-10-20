from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.conf import settings

from .forms import *
from .models import *
from .wallet_utils import *
from .registration_utils import *
from .agent_utils import *


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """

    def authenticate(self, request, email=None):
        try:
            user = AriesUser.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return AriesUser.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None