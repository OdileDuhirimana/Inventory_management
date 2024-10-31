"""
ASGI config for inventory_management project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from .routing import application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventory_management.settings")

django_asgi_app = get_asgi_application()

application = application
