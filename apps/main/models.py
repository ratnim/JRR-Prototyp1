from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

class Profile(models.Model):
    """Profile data for experts and non-experts."""

    first_name = models.CharField(verbose_name='First Name', max_length=256)
    last_name = models.CharField(verbose_name='Last Name', max_length=256)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class State(models.Model):
    """State of an expert"""

    #training = models.ManyToOneRel(Training)
    passed = models.BooleanField(verbose_name='Passed Course', default=False)

    available = models.BooleanField(verbose_name='Is available', default=False)


class ExpertManager(models.Manager):
    """Manager for creating new experts"""

    def create(self, email, first_name, last_name, password):

        profile = Profile.objects.create(
            first_name=first_name,
            last_name=last_name
        )

        state = State.objects.create(

        )

        user = User.objects.create_user(
            email=email,
            username=email,
            password=password
        )

        expert = Expert(
            profile=profile,
            user=user,
            state=state
        )
        expert.save()
        return expert


class Expert(models.Model):
    """Expert data"""

    experts = ExpertManager()

    user = models.OneToOneField(User)
    profile = models.OneToOneField(Profile)
    state = models.OneToOneField(State)

    # expert specific data
    trained = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
