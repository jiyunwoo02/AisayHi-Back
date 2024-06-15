from django.contrib.auth.backends import ModelBackend
from pm.models import User

class LoginIdBackend(ModelBackend):
    def authenticate(self, request, login_id=None, password=None, **kwargs):
        try:
            user = User.objects.get(login_id=login_id)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user