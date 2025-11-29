import React, { useState } from 'react';
import { X, FolderOpen, Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import { ingestFiles, uploadFile } from '../api';
import { FilePicker } from './FilePicker';

interface IngestProps {
    isOpen: boolean;
    onClose: () => void;
}

export const Ingest: React.FC<IngestProps> = ({ isOpen, onClose }) => {
    const [path, setPath] = useState('');
    const [loading, setLoading] = useState(false);
    const [status, setStatus] = useState<{ type: 'success' | 'error', message: string } | null>(null);

    if (!isOpen) return null;

    const handleFilesSelected = async (files: File[]) => {
        setLoading(true);
        setStatus(null);
        let successCount = 0;
        let errors: string[] = [];

        try {
            for (const file of files) {
                try {
                    await uploadFile(file);
                    successCount++;
                } catch (error: any) {
                    errors.push(`Failed to upload ${file.name}: ${error.message}`);
                }
            }

            if (successCount > 0) {
                setStatus({
                    type: 'success',
                    message: `Successfully uploaded ${successCount} files.`
                });
            }

            if (errors.length > 0) {
                console.warn("Upload errors:", errors);
                if (successCount === 0) {
                    setStatus({
                        type: 'error',
                        message: "Failed to upload files."
                    });
                }
            }

        } catch (error: any) {
            setStatus({
                type: 'error',
                message: "An unexpected error occurred."
            });
        } finally {
            setLoading(false);
        }
    };

    const handleIngest = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!path.trim()) return;

        setLoading(true);
        setStatus(null);

        try {
            const result = await ingestFiles(path);
            setStatus({
                type: 'success',
                message: `Successfully processed ${result.count} files.`
            });
            if (result.errors.length > 0) {
                // Could show errors in detail, but keeping it simple for now
                console.warn("Ingestion errors:", result.errors);
            }
        } catch (error: any) {
            setStatus({
                type: 'error',
                message: error.response?.data?.error || "Failed to ingest files."
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl w-full max-w-md shadow-xl overflow-hidden">
                <div className="p-6 border-b border-gray-100 flex justify-between items-center">
                    <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
                        <FolderOpen className="h-5 w-5 text-blue-600" />
                        Add Files
                    </h2>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                    >
                        <X className="h-5 w-5" />
                    </button>
                </div>

                <div className="p-6 space-y-6">
                    {/* Option 1: Upload Files */}
                    <div className="space-y-3">
                        <h3 className="text-sm font-medium text-gray-900">Option 1: Upload Files</h3>
                        <div className="flex items-center gap-3">
                            <FilePicker onFilesSelected={handleFilesSelected} />
                            <span className="text-sm text-gray-500">Select files from your device</span>
                        </div>
                    </div>

                    <div className="relative">
                        <div className="absolute inset-0 flex items-center" aria-hidden="true">
                            <div className="w-full border-t border-gray-200" />
                        </div>
                        <div className="relative flex justify-center">
                            <span className="bg-white px-2 text-sm text-gray-500">OR</span>
                        </div>
                    </div>

                    {/* Option 2: Ingest Directory */}
                    <form onSubmit={handleIngest} className="space-y-4">
                        <div>
                            <label htmlFor="path" className="block text-sm font-medium text-gray-900 mb-1">
                                Option 2: Ingest Local Directory
                            </label>
                            <input
                                type="text"
                                id="path"
                                className="block w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all"
                                placeholder="/home/user/documents"
                                value={path}
                                onChange={(e) => setPath(e.target.value)}
                            />
                            <p className="mt-1 text-xs text-gray-500">
                                Enter the absolute path to a local folder.
                            </p>
                        </div>

                        <div className="flex justify-end">
                            <button
                                type="submit"
                                disabled={loading || !path.trim()}
                                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium flex items-center gap-2"
                            >
                                {loading && <Loader2 className="h-4 w-4 animate-spin" />}
                                Start Ingestion
                            </button>
                        </div>
                    </form>

                    {status && (
                        <div className={`p-3 rounded-lg flex items-start gap-2 text-sm ${status.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
                            }`}>
                            {status.type === 'success' ? (
                                <CheckCircle className="h-5 w-5 shrink-0" />
                            ) : (
                                <AlertCircle className="h-5 w-5 shrink-0" />
                            )}
                            <span>{status.message}</span>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};
