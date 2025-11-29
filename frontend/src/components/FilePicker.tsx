import { useRef } from "react";
import { Folder } from 'lucide-react';

type FilePickerProps = {
    onFilesSelected: (files: File[]) => void;
};

export function FilePicker({ onFilesSelected }: FilePickerProps) {
    const inputRef = useRef<HTMLInputElement | null>(null);

    const handleClick = () => {
        inputRef.current?.click();
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files ? Array.from(e.target.files) : [];
        if (files.length > 0) {
            onFilesSelected(files);
            // optional: clear so selecting the same file again still fires change
            e.target.value = "";
        }
    };

    return (
        <>
            <button
                type="button"
                onClick={handleClick}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium flex items-center gap-2"
            >
                <Folder className="h-4 w-4" />
                Browse Files
            </button>

            <input
                ref={inputRef}
                type="file"
                multiple
                onChange={handleChange}
                className="hidden"
            />
        </>
    );
}
