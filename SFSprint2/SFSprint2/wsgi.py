"""
WSGI config for SFSprint2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from SFSprint2.settings import get_wsgi_application

print("Python Path:", sys.path)  # Add this line to print the Python path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SFSprint2.settings')
application = get_wsgi_application()