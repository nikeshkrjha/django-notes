from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from cloudinary.models import CloudinaryField


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


class Label(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    created_by = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, blank=False,null=False)

    class Meta:
        unique_together = ('name', 'created_by',)

    def __str__(self):
        return self.name


class Note(models.Model):
    content = models.CharField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(
        auto_now_add=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        to=CustomUser, related_name='notes', null=False, on_delete=models.CASCADE)
    note_label = models.ForeignKey(
        to=Label, related_name="notes", null=True, blank=True, on_delete=models.CASCADE)
    uploaded_file = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.content[:10]
