from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import File
from .search import index_file

@receiver(post_save, sender=File)
def update_index(sender, instance, created, **kwargs):
    # Synchronous indexing for now
    index_file(instance)