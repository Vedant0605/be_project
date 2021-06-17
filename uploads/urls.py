from django.urls import path

from .views import (
    upload_view,
    detect_view,
    UploadTemplateView
)

app_name = 'uploads'

urlpatterns = [
    path('generate', upload_view, name='generate'),
    path('upload', UploadTemplateView.as_view(), name='upload'),
    path('report', detect_view, name='report-generate'),
]
