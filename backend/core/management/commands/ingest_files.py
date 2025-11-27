import os
from django.core.management.base import BaseCommand
from core.models import File

class Command(BaseCommand):
    help = 'Ingest files from a directory into the database'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='Path to the directory to ingest')

    def handle(self, *args, **options):
        directory = options['directory']

        if not os.path.isdir(directory):
            self.stdout.write(self.style.ERROR(f'Directory not found: {directory}'))
            return

        self.stdout.write(f'Scanning directory: {directory}')

        count = 0
        for root, dirs, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                # Skip hidden files
                if filename.startswith('.'):
                    continue

                try:
                    # Get file stats
                    stats = os.stat(file_path)
                    size = stats.st_size
                    _, ext = os.path.splitext(filename)
                    
                    # Create or update File object
                    # We use path as the unique identifier for simplicity here
                    file_obj, created = File.objects.update_or_create(
                        path=file_path,
                        defaults={
                            'name': filename,
                            'file_type': ext.lstrip('.').lower(),
                            'size': size,
                        }
                    )
                    
                    action = "Created" if created else "Updated"
                    self.stdout.write(f'{action}: {filename}')
                    count += 1

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing {filename}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {count} files'))
