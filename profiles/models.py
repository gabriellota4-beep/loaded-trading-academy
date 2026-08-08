from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    EXPERIENCE = [('new', 'New trader'), ('developing', 'Developing trader'),
                  ('experienced', 'Experienced trader')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile')
    display_name = models.CharField(max_length=80, blank=True)
    trading_experience = models.CharField(
        max_length=20, choices=EXPERIENCE, default='new')
    preferred_market = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.display_name or self.user.username

# Create your models here.
