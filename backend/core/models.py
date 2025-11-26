from django.db import models

class File(models.Model):
    path = models.CharField(max_length=1024)
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)  # e.g. 'pdf'
    size = models.BigIntegerField()
    indexed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name