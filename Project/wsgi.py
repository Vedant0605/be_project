"""
WSGI config for Project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from detection.load_model import export_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
det_transformer, det_face_extractor, det_net, det_device = export_model()
application = get_wsgi_application()
