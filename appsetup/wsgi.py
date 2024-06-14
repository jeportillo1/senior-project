"""
WSGI config for appsetup project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

For more information, visit
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling
import sys

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, the WSGI_APPLICATION
# setting points here.

RUNNING_DEVSERVER = (len(sys.argv) > 1 and (sys.argv[1] == 'runserver' or sys.argv[1] == 'test'))
if RUNNING_DEVSERVER:
    print("development")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appsetup.settings.development_settings')
    application = Cling(get_wsgi_application()) # cling for django to serve static (server should do this)
else:
    print("production")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appsetup.settings.production_settings')
    application = get_wsgi_application() # can get errors like 'Not Found: /accounts/profile/' if you aren't servering static correctly

