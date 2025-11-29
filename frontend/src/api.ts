import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
});

export interface FileItem {
    id: number;
    name: string;
    path: string;
    file_type: string;
    size: number;
    created_at: string;
    snippet?: string; // For search results
}

export const fetchFiles = async () => {
    const response = await api.get<FileItem[]>('/files/');
    return response.data;
};

export const searchFiles = async (query: string) => {
    const response = await api.get<FileItem[]>(`/search/?q=${encodeURIComponent(query)}`);
    return response.data;
};

export const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post<FileItem>('/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const openFile = async (path: string) => {
    const response = await api.post('/open/', { path });
    return response.data;
};

export interface IngestResponse {
    status: string;
    count: number;
    errors: string[];
}

export const ingestFiles = async (path: string) => {
    const response = await api.post<IngestResponse>('/ingest/', { path });
    return response.data;
};

export const pickDirectory = async () => {
    const response = await api.post<{ path: string | null }>('/pick-directory/');
    return response.data;
};