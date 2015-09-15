import os

from django.utils.crypto import get_random_string
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Generate a local settings file for the django application'

    def _generate_secret_key(self):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        return get_random_string(50, chars)

    def buildLocalSettings(self):
        with open(os.path.join(settings.BASE_DIR, 'boilerplate', 'settings', 'local.py'), 'w+') as file_object:
            file_object.write('\n'.join([
                'from __future__ import absolute_import',
                'from .dev import *',
                '',
                "SECRET_KEY = '{0}'".format(self._generate_secret_key()),
                '',
            ]))

    def handle(self, *args, **options):
        self.buildLocalSettings()
