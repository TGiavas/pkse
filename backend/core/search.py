import os
from django.conf import settings
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.qparser import QueryParser

# Define the schema
# path is stored so we can retrieve the file later
# content is indexed but not stored (to save space, we have the file)
SCHEMA = Schema(
    id=ID(stored=True, unique=True),
    path=STORED(),
    title=TEXT(stored=True),
    content=TEXT()
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
    Index a File model instance.
    For now, we just index the name as content. 
    Later we will extract real content.
    """
    ix = get_index()
    writer = ix.writer()
    
    # TODO: Extract actual text content from file_obj.path
    content = f"{file_obj.name} (Content extraction pending)"
    
    writer.update_document(
        id=str(file_obj.id),
        path=file_obj.path,
        title=file_obj.name,
        content=content
    )
    writer.commit()