import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils.timezone import now


class User(models.Model):
    """
    Custom User model.
    Users log in with email and password.
    """

    user_id = models.BigAutoField(primary_key=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_name = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.EmailField(unique=True, max_length=124)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    creation_date = models.DateTimeField(default=now)
    updation_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        ordering = ["-creation_date"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.user_name

    @property
    def is_authenticated(self):
        """Always True for real users. Django's auth framework checks this."""
        return True

    @property
    def is_anonymous(self):
        """Always False for real users."""
        return False

    REQUIRED_FIELDS = []

    # Password helpers

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password = make_password(raw_password)

    def verify_password(self, raw_password):
        """Check a raw password against the stored hash."""
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        """
        Override save to ensure the password is always stored as a hash.
        """
        if self.password and not self.password.startswith(("pbkdf2_sha256$", "bcrypt$", "argon2")):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)