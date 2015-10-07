from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from address.models import AddressField

from mongoengine import Document, fields, ListField, DateTimeField


class Page(Document):

    title = fields.StringField(max_length=200)
    date_modified = DateTimeField(datetime.now())


class Profile(models.Model):
    """Profile data for experts and non-experts."""
    GENDER = (
        ('m', 'male'),
        ('f', 'female'),
    )
    EMPTY_SPACE = ''
    DEFAULT_DATE = datetime.now()

    # personal details #
    user = models.OneToOneField('auth.User', primary_key=True)
    first_name = models.CharField("person's first name", 
        max_length=30, default=EMPTY_SPACE, null=True)
    middle_name = models.CharField("person's middle name", max_length=30, blank=True)
    last_name = models.CharField("person's family name", max_length=30, 
        default=EMPTY_SPACE, null=True)
    gender = models.CharField(max_length=1, choices=GENDER, default='m', null=True)
    title = models.CharField(max_length=64, blank=True)
    date_of_birth = models.DateField(default=DEFAULT_DATE, 
        help_text="Please use the following format: <em>YYYY-MM-DD</em>.", null=True)
    city_of_birth = models.CharField(max_length=30, default=EMPTY_SPACE, null=True)
    country_of_birth = models.CharField(max_length=30, default=EMPTY_SPACE, null=True)
    citizenship = models.CharField(max_length=256, default=EMPTY_SPACE, null=True)
    # passport_number = models.SlugField(max_length=9, unique=True, default=EMPTY_SPACE)

    # contact details #
    address = models.CharField(max_length=64, blank=True, null=True)
    postal_code = models.IntegerField(blank=True, default=0, null=True)
    city = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64, blank=True)
    
    mail_address = models.EmailField(null=True)
    # phone_number = models.CharField(max_length=30, unique=True, default=EMPTY_SPACE)
    # work_phone_number = models.CharField(max_length=30, default=EMPTY_SPACE)
    # home_phone_number = models.CharField(max_length=30, blank=True)
    # current_address = AddressField(default='1 Somewhere Ave, Northcote, VIC 3070, AU', blank=True)
    # permanent_address = AddressField(related_name='+', blank=True, default='1 Somewhere Ave, Northcote, VIC 3070, AU, Australia')

    # professional info
    main_profession = models.CharField(max_length=64, blank=True)
    secondary_profession = models.CharField(max_length=64, blank=True)
    level_of_employment = models.CharField(max_length=64, blank=True)
    un_security_test = models.BooleanField(default=False)
    un_security_test_date = models.CharField(max_length=64, blank=True)

    expertise = models.CharField(blank=True, max_length=64)

    # medical info
    details_medical_conditions = models.CharField(blank=True, max_length=64)
    medical_conditions = models.BooleanField(default=False)

    last_modified = models.DateTimeField(auto_now=True)
    member_since = models.DateField("date of registration", auto_now_add=True)


    # emergecy contact
    eme_name = models.CharField(max_length=64, blank=True)
    eme_relation = models.CharField(max_length=64, blank=True)
    eme_phone = models.CharField(max_length=64, blank=True)
    eme_email = models.CharField(max_length=64, blank=True)
    eme_city = models.CharField(max_length=64, blank=True)
    eme_country = models.CharField(max_length=64, blank=True)

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