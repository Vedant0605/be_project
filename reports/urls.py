from django.urls import path

from .views import (
    ReportsListView,
    ReportsDetailView,
    delete_report,
    pdf_export
)

app_name = 'reports'

urlpatterns = [
    path('', ReportsListView.as_view(), name='reports_home'),
    path('<pk>/', ReportsDetailView.as_view(), name='detail'),
    path('<pk>/delete', delete_report, name='delete'),
    path('<pk>/pdf', pdf_export, name='pdf')
]
