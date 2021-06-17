from django.db import models
from django.utils import timezone

from profiles.models import Profile
from .utils import generate_code
from .utils import path_and_rename


class Uploads(models.Model):
    upload_id = models.CharField(max_length=12, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    file_name = models.CharField(blank=True, max_length=128)
    changed_file_name = models.FileField(upload_to=path_and_rename)

    def save(self, *args, **kwargs):
        if self.upload_id == "":
            self.upload_id = generate_code()
        if self.created is None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)

    def get_upload_id(self):
        return self.upload_id

    def get_upload_filename(self):
        return self.file_name

    def get_upload_date(self):
        return self.created.strftime('%Y-%m-%d')

    def __str__(self):
        return f"ID: {self.upload_id}, Uploader: {self.author}, Video File Name: {self.file_name}, Created: {self.get_upload_date()}"
