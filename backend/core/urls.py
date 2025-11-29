from django.urls import path
from .views import FileUploadView, FileListView, SearchFileView, OpenFileView, IngestView, PickDirectoryView

urlpatterns = [
    
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('search/', SearchFileView.as_view(), name='file-search'),
    path('open/', OpenFileView.as_view(), name='file-open'),
    path('ingest/', IngestView.as_view(), name='file-ingest'),
    path('pick-directory/', PickDirectoryView.as_view(), name='pick-directory'),
]