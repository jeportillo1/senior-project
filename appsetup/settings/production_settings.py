from .base import * # noqa: F401

import os

ALLOWED_HOSTS = os.environ['DEPLOY_ALLOWED_HOST'].split(" ")
DEBUG = False # django will no longer serve static files, web handles that
CSRF_COOKIE_SECURE=True # 'django.middleware.csrf.CsrfViewMiddleware' Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
SESSION_COOKIE_SECURE=True # if is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
SECURE_CONTENT_TYPE_NOSNIFF = True # if is not set to True, so your pages will not be served with an 'X-Content-Type-Options: nosniff' header. You should consider enabling this header to prevent the browser from identifying content types incorrectly.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True # Without this, your site is potentially vulnerable to attack via an insecure connection to a subdomain. Only set this to True if you are certain that all subdomains of your domain should be served exclusively via SSL.
SECURE_BROWSER_XSS_FILTER = True # setting is not set to True, so your pages will not be served with an 'X-XSS-Protection: 1; mode=block' header. You should consider enabling this header to activate the browser's XSS filtering and help prevent XSS attacks.
SECURE_HSTS_SECONDS = 604800  # in seconds and forces HTTPS instead of HTTP
SECURE_SSL_REDIRECT = True # Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
SECURE_HSTS_PRELOAD = True # Without this, your site cannot be submitted to the browser preload list.
X_FRAME_OPTIONS = "DENY" # 'django.middleware.clickjacking.XFrameOptionsMiddleware' The default is 'SAMEORIGIN', but unless there is a good reason for your site to serve other parts of itself in a frame, you should change it to 'DENY'.
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {

        # MYSQL server
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('PRO_DB_NAME'),
        'USER': os.environ.get('PRO_DB_USER'),
        'PASSWORD': os.environ.get('PRO_DB_PASS'),
        'HOST': os.environ.get('PRO_DB_HOST'),
        'PORT': os.environ.get('PRO_DB_PORT'),
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}
