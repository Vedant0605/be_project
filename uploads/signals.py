import os

from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Uploads


@receiver(post_delete, sender=Uploads)
def post_delete_remove_media(sender, instance, **kwargs):
    print(os.path.join(settings.MEDIA_ROOT, str(instance.changed_file_name)))
    os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.changed_file_name)))
