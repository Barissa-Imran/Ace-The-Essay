"""
WSGI config for ATE project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""


import os
from django.core.wsgi import get_wsgi_application

here = os.path.dirname(__file__)
wsgi = os.path.join(here, 'wsgi.py')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ATE.settings')

application = get_wsgi_application()
