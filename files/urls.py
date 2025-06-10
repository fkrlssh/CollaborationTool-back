# files/urls.py
from django.urls import path
from files.views.download_file_view import FileDownloadView

urlpatterns = [
    path('<int:project_id>/<int:task_number>/<int:file_number>/download/', FileDownloadView.as_view(), name='file-download'),
]
