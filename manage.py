#!/usr/bin/env python
"""
Command-line utility for administrative tasks.

# For more information about this file, visit
# https://docs.djangoproject.com/en/4.0/ref/django-admin/
"""

import os
import sys

# from django.conf import settings

if __name__ == '__main__':

    RUNNING_DEVSERVER = (len(sys.argv) > 1 and (sys.argv[1] == 'runserver' or sys.argv[1] == 'test'))
    if RUNNING_DEVSERVER:
        print("development")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appsetup.settings.development_settings')
    else:
        print("production")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appsetup.settings.production_settings')


    try:
        from django.core.management.commands.runserver import Command as runserver # noqa: F401
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    
