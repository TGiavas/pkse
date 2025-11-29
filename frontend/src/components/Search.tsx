import React, { useState } from 'react';
import { Search as SearchIcon, FileText, Loader2, Plus } from 'lucide-react';
import { searchFiles, openFile, type FileItem } from '../api';
import { Ingest } from './Ingest';

export const Search: React.FC = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<FileItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [hasSearched, setHasSearched] = useState(false);
    const [isIngestOpen, setIsIngestOpen] = useState(false);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        try {
            const data = await searchFiles(query);
            setResults(data);
            setHasSearched(true);
        } catch (error) {
            console.error("Search failed:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleOpenFile = async (path: string) => {
        try {
            await openFile(path);
        } catch (error) {
            console.error("Failed to open file:", error);
            alert("Failed to open file. Please check if the backend is running and the file exists.");
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col items-center py-20 px-4">
            <div className="absolute top-6 right-6">
                <button
                    onClick={() => setIsIngestOpen(true)}
                    className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-50 text-gray-700 font-medium transition-all"
                >
                    <Plus className="h-4 w-4" />
                    Add Files
                </button>
            </div>

            <Ingest isOpen={isIngestOpen} onClose={() => setIsIngestOpen(false)} />

            <div className="w-full max-w-2xl">
                <h1 className="text-4xl font-bold text-gray-900 text-center mb-8 tracking-tight">
                    PKSE <span className="text-blue-600">Search</span>
                </h1>

                <form onSubmit={handleSearch} className="relative mb-12">
                    <div className="relative group">
                        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                            <SearchIcon className="h-5 w-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                        </div>
                        <input
                            type="text"
                            className="block w-full pl-11 pr-4 py-4 bg-white border border-gray-200 rounded-2xl shadow-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all text-lg"
                            placeholder="Search your documents..."
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                        <div className="absolute inset-y-0 right-0 pr-4 flex items-center">
                            {loading && <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />}
                        </div>
                    </div>
                </form>

                <div className="space-y-4">
                    {hasSearched && results.length === 0 && !loading && (
                        <div className="text-center text-gray-500 py-8">
                            No results found for "{query}"
                        </div>
                    )}

                    {results.map((file) => (
                        <div
                            key={file.id}
                            onClick={() => handleOpenFile(file.path)}
                            className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200 cursor-pointer hover:border-blue-200"
                        >
                            <div className="flex items-start gap-4">
                                <div className="p-2 bg-blue-50 rounded-lg shrink-0">
                                    <FileText className="h-6 w-6 text-blue-600" />
                                </div>
                                <div className="flex-1 min-w-0">
                                    <h3 className="text-lg font-semibold text-gray-900 mb-1 truncate group-hover:text-blue-600">
                                        {file.name}
                                    </h3>
                                    <p className="text-xs text-gray-500 font-mono mb-3 truncate bg-gray-50 px-2 py-1 rounded inline-block">
                                        {file.path}
                                    </p>
                                    {file.snippet && (
                                        <div
                                            className="text-sm text-gray-600 leading-relaxed prose prose-sm max-w-none"
                                            dangerouslySetInnerHTML={{ __html: file.snippet }}
                                        />
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
