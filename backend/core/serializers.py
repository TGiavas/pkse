from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'path', 'file_type', 'size', 'created_at', 'indexed_at']
        read_only_fields = ['path', 'size', 'file_type', 'created_at', 'indexed_at']