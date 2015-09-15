from django.db import models

class Profile(models.Model):
    """Profile data for experts and non-experts."""

    name = models.CharField(verbose_name='Name', max_length=256)
    user = models.OneToOneField('auth.User', primary_key=True)

    def __str__(self):
        return self.name
