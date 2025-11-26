# Personal Knowledge Search Engine (PKSE)

A local, private, lightweight "internal Google" for your files, PDFs, notes, and bookmarks.

## Stack

- **Backend**: Django (Python)
    - File ingestion
    - Celery for async indexing
    - Postgres for metadata
    - Whoosh for search indexing
- **Frontend**: React (Vite + TypeScript)
    - Explorer UI
    - Full-text search
    - PDF preview

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
