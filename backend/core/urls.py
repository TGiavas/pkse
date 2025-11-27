from django.urls import path
from .views import FileUploadView, FileListView, SearchFileView  

urlpatterns = [
    
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('search/', SearchFileView.as_view(), name='file-search'),
]