from django.utils import timezone

from django.db import models
from django.urls import reverse

from profiles.models import Profile
from uploads.models import Uploads


# Create your models here.

class Report(models.Model):
    name = models.CharField(max_length=120)
    upload = models.ForeignKey(Uploads, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    result = models.TextField(blank=True)
    pred_mean = models.TextField(blank=True)
    face_sample = models.TextField(blank=True)
    no_of_frames = models.IntegerField(blank=True, null=True)
    frame_pred_graph = models.TextField(blank=True)
    frame_graph = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('reports:detail', kwargs={'pk': self.pk})

    def get_upload_id(self):
        return self.upload.upload_id

    def get_author_name(self):
        return self.author.get_user_name()

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)
