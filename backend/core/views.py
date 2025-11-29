import os
from rest_framework.views import APIView
from rest_framework import generics  # <--- Add this
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.files.storage import default_storage
from .models import File
from .serializers import FileSerializer
from .search import get_index
from .ingest import ingest_directory
from whoosh.qparser import MultifieldParser
import subprocess
import tkinter as tk
from tkinter import filedialog

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Save file to media directory
        file_name = file_obj.name
        save_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        # Ensure media directory exists
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        # Save the file manually to ensure we get the absolute path
        with open(save_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        # Create File model instance
        # This will trigger the post_save signal to index the file
        file_instance = File.objects.create(
            name=file_name,
            path=save_path,
            size=file_obj.size,
            file_type=os.path.splitext(file_name)[1].replace('.', '')
        )

        serializer = FileSerializer(file_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FileListView(generics.ListAPIView):
    queryset = File.objects.all().order_by('-created_at')
    serializer_class = FileSerializer

class SearchFileView(APIView):
    def get(self, request, *args, **kwargs):
        query_string = request.query_params.get('q', '')
        if not query_string:
            return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)

        ix = get_index()
        results_data = []
        
        with ix.searcher() as searcher:
            query = MultifieldParser(["title", "content"], ix.schema).parse(query_string)
            results = searcher.search(query, limit=20)
            
            for r in results:
                # Highlight matches in content
                snippet = r.highlights("content")
                results_data.append({
                    "id": r.get("id"),
                    "title": r.get("title"),
                    "path": r.get("path"),
                    "snippet": snippet
                })

        return Response(results_data, status=status.HTTP_200_OK)

class OpenFileView(APIView):
    def post(self, request, *args, **kwargs):
        path = request.data.get('path')
        if not path:
            return Response({"error": "Path is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not os.path.exists(path):
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Linux specific - opens file with default application
            subprocess.call(['xdg-open', path])
            return Response({"status": "opened"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class IngestView(APIView):
    def post(self, request, *args, **kwargs):
        path = request.data.get('path')
        if not path:
            return Response({"error": "Path is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            count, errors = ingest_directory(path)
            return Response({
                "status": "success",
                "count": count,
                "errors": errors
            }, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response({"error": "Directory not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PickDirectoryView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Create a root window and hide it
            root = tk.Tk()
            root.withdraw()
            
            # Make sure it appears on top
            root.attributes('-topmost', True)
            
            # Open the directory picker
            directory = filedialog.askdirectory()
            
            # Destroy the root window
            root.destroy()
            
            if directory:
                return Response({"path": directory}, status=status.HTTP_200_OK)
            else:
                return Response({"path": None}, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)