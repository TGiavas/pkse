import os
import shutil
import time
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings
from .models import File
from .search import get_index


class FileUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_file_path = 'test_upload.txt'
        with open(self.test_file_path, 'w') as f:
            f.write("This is a test content for search indexing.")
            
        # Clear index for testing
        self.index_dir = os.path.join(settings.BASE_DIR, 'search_index')
        if os.path.exists(self.index_dir):
            shutil.rmtree(self.index_dir)

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        # Clean up media
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

    def test_upload_file(self):
        with open(self.test_file_path, 'rb') as f:
            response = self.client.post('/api/upload/', {'file': f}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 1)
        
        file_obj = File.objects.first()
        self.assertEqual(file_obj.name, 'test_upload.txt')
        
        # Verify Search Index
        ix = get_index()
        with ix.searcher() as searcher:
            results = list(searcher.documents())
            self.assertTrue(len(results) > 0)
            found = False
            for r in results:
                if 'test content' in r.get('content', ''):
                    found = True
            self.assertTrue(found, "Content not found in search index")



class FileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_file_path = 'test_upload.txt'
        with open(self.test_file_path, 'w') as f:
            f.write("This is a test content for search indexing.")
            
        # Clear index for testing
        self.index_dir = os.path.join(settings.BASE_DIR, 'search_index')
        if os.path.exists(self.index_dir):
            shutil.rmtree(self.index_dir)

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

    def test_upload_and_search(self):
        # 1. Upload
        with open(self.test_file_path, 'rb') as f:
            response = self.client.post('/api/upload/', {'file': f}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2. List
        response = self.client.get('/api/files/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # 3. Search
        # Re-open index to ensure changes are committed
        # (In real app, commit happens in signal, but we might need a small delay or force refresh in tests if using async, but here it is sync)
        
        response = self.client.get('/api/search/?q=content')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.data[0]['title'], 'test_upload.txt')
        print(f"Search Snippet: {response.data[0]['snippet']}")