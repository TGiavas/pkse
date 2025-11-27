import os
from django.conf import settings
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.qparser import QueryParser
from .utils import extract_text_from_file  # <--- Import this

# ... (Schema and get_index remain the same) ...
SCHEMA = Schema(
    id=ID(stored=True, unique=True),
    path=STORED(),
    title=TEXT(stored=True),
    content=TEXT(stored=True)
)

INDEX_DIR = os.path.join(settings.BASE_DIR, 'search_index')

def get_index():
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
        return create_in(INDEX_DIR, SCHEMA)
    if not exists_in(INDEX_DIR):
        return create_in(INDEX_DIR, SCHEMA)
    return open_dir(INDEX_DIR)

def index_file(file_obj):
    """
    Index a File model instance with actual content extraction.
    """
    ix = get_index()
    writer = ix.writer()
    
    # Extract real content
    content = extract_text_from_file(file_obj.path)
    
    # If no content extracted, fallback to name
    if not content.strip():
        content = file_obj.name

    writer.update_document(
        id=str(file_obj.id),
        path=file_obj.path,
        title=file_obj.name,
        content=content
    )
    writer.commit()