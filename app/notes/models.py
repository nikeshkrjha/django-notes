from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

def file_upload_path(instance, filename):
    return 'file_uploads/user_{0}/{1}'.format(instance.created_by.id, filename)

class Note(models.Model):
    content = models.CharField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=CustomUser, related_name='notes', null=False, on_delete=models.CASCADE)
    uploaded_file = models.FileField(upload_to=file_upload_path, null=True, blank=True)

    def __str__(self) -> str:
        return self.content[:10]

