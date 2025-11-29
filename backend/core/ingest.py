import os
from core.models import File

def ingest_directory(directory, stdout=None):
    """
    Scans a directory and ingests files into the database.
    Returns a tuple (count, errors).
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f'Directory not found: {directory}')

    if stdout:
        stdout.write(f'Scanning directory: {directory}')

    count = 0
    errors = []

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
                
                if stdout:
                    action = "Created" if created else "Updated"
                    stdout.write(f'{action}: {filename}')
                
                count += 1

            except Exception as e:
                error_msg = f'Error processing {filename}: {e}'
                errors.append(error_msg)
                if stdout:
                    stdout.write(stdout.style.ERROR(error_msg))

    return count, errors
