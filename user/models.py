from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    bio = models.TextField(max_length=500, blank=True)
    registration_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.user.username