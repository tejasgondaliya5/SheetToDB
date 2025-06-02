from django.urls import path
from .views import EmployeeBulkUploadView

urlpatterns = [
    path('upload/', EmployeeBulkUploadView.as_view(), name='employee-bulk-upload'),
]