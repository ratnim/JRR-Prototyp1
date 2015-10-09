from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from address.models import AddressField

from annoying.fields import AutoOneToOneField
from mongoengine import Document, fields, ListField, DateTimeField


class Page(Document):

    title = fields.StringField(max_length=200)
    date_modified = DateTimeField(datetime.now())


class EmergencyContact(models.Model):

    """
    EmergencyContact, part of the Profile model
    """
    # emergecy contact
    name = models.CharField(max_length=64, blank=True, null=True)
    relation = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)


class Expertise(models.Model):
    expertise = models.CharField(blank=True, max_length=64)


class Skills(models.Model):
    main_profession = models.CharField(max_length=64, blank=True)
    secondary_profession = models.CharField(max_length=64, blank=True)
    level_of_employment = models.CharField(max_length=64, blank=True)
    un_security_test = models.BooleanField(default=False)
    un_security_test_date = models.CharField(max_length=64, blank=True)
    expertise = models.ForeignKey(Expertise, blank=True, null=True)


class UserMail(models.Model):
    mail = models.EmailField(null=True, blank=True)


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=30, default='')


class Address(models.Model):
    address = models.CharField(max_length=64, blank=True, null=True)
    postal_code = models.IntegerField(blank=True, default=0, null=True)
    city = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64, blank=True)


class ContactInfo(models.Model):
    mail_addresses = models.ForeignKey(UserMail, blank=True, null=True)
    phone_numbers = models.ForeignKey(PhoneNumber, blank=True, null=True)
    address = models.ForeignKey(Address, blank=True, null=True)


class Profile(models.Model):

    """Profile data for experts and non-experts."""
    GENDER = (
        ('m', 'male'),
        ('f', 'female'),
    )
    EMPTY_SPACE = ''
    DEFAULT_DATE = date.today()

    # personal details #
    user = models.OneToOneField('auth.User', primary_key=True)
    emergency_contact = models.ForeignKey(EmergencyContact, blank=True,
                                          null=True, unique=True)

    professional_info = models.ForeignKey(Skills, blank=True,
                                          null=True, unique=True)
    contact_info = models.ForeignKey(ContactInfo, blank=True,
                                     null=True, unique=True)
    name = models.CharField("person's first name", max_length=30,
                            default=EMPTY_SPACE, null=True)
    surname = models.CharField("person's family name", max_length=30,
                               default=EMPTY_SPACE, null=True)
    gender = models.CharField(max_length=1, choices=GENDER, default='m',
                              null=True)
    date_of_birth = models.DateField(
        default=DEFAULT_DATE,
        help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
        null=True)

    # medical info
    details_medical_conditions = models.CharField(blank=True, max_length=64)
    medical_conditions = models.BooleanField(default=False)

    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + self.middle_name + self.last_name


class State(models.Model):

    """State of an expert"""

    #training = models.ManyToOneRel(Training)
    passed = models.BooleanField(verbose_name='Passed Course', default=False)

    available = models.BooleanField(verbose_name='Is available', default=False)


class ExpertManager(models.Manager):

    """Manager for creating new experts"""

    def create(self, email, first_name, last_name, password):

        user = User.objects.create_user(
            email=email,
            username=email,
            password=password
        )

        profile = Profile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name
        )

        state = State.objects.create(

        )

        expert = Expert(
            profile=profile,
            user=user,
            state=state
        )

        profile.save()
        state.save()
        user.save()
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


class CountryLog(models.Model):

    """Country Log"""
