from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """Profile data for experts and non-experts."""

    name = models.CharField(verbose_name='Name', max_length=256)

    def __str__(self):
        return self.name


class ExpertManager(models.Manager):
    """Manager for creating new experts"""

    def create(self, username, email, name, password, date_joined):

        profile = Profile(
            name=name
        )
        profile.save()

        user = User(
            email=email,
            username=username,
            date_joined=date_joined
        )
        user.set_password(password)
        user.save()

        expert = Expert(
            profile=profile,
            user=user
        )
        expert.save()
        return expert


class Expert(models.Model):
    """Expert data"""

    experts = ExpertManager()

    user = models.OneToOneField('auth.User')
    profile = models.OneToOneField('profile')
    trained = models.BooleanField(default=False)

    def __str__(self):
        return self.user
