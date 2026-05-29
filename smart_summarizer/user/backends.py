from user.models import User


class EmailBackend:
    """
    Custom auth backend — users log in with email + password.

    Add to settings.py:
        AUTHENTICATION_BACKENDS = ['user.backends.EmailBackend']
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        if not email or not password:
            return None

        try:
            user = User.objects.get(email_id=email, is_active=True)
        except User.DoesNotExist:
            return None

        if user.verify_password(password):
            return user
        return None

    def get_user(self, user_id):
        """Required by Django's auth framework."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
