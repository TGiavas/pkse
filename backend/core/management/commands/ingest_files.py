import os
from django.core.management.base import BaseCommand
from core.ingest import ingest_directory

class Command(BaseCommand):
    help = 'Ingest files from a directory into the database'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='Path to the directory to ingest')

    def handle(self, *args, **options):
        directory = options['directory']

        try:
            count, errors = ingest_directory(directory, stdout=self.stdout)
            self.stdout.write(self.style.SUCCESS(f'Successfully processed {count} files'))
            if errors:
                self.stdout.write(self.style.WARNING(f'Encountered {len(errors)} errors'))
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(str(e)))

