#!/usr/bin/env python
import os
import sys


def createEmptyFile(path):
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    with open(path, 'a'):
        os.utime(path, None)

def createEmptyFileIfNotExistant(path):
    if not os.path.isfile(path):
        createEmptyFile(path)


if __name__ == "__main__":
    from django.conf import settings
    from django.core.management import execute_from_command_line

    # create log file by default to prevent django logger errors
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    debugLogs = os.path.join(BASE_DIR, 'logs', 'debug.log')
    createEmptyFileIfNotExistant(debugLogs)

    # choose local settings if available
    devSettings = "boilerplate.settings.dev"
    localSettings = "boilerplate.settings.local"

    djangoSettings = localSettings
    if not os.path.isfile(os.path.join(BASE_DIR, 'boilerplate', 'settings', 'local.py')):
        djangoSettings = devSettings

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", djangoSettings)

    # run manage command
    execute_from_command_line(sys.argv)
