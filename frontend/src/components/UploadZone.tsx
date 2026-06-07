import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCompilerStore } from '@/store/compilerStore';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { UploadCloud, FileType } from 'lucide-react';

export const UploadZone = () => {
    const { processNewDocument } = useCompilerStore();
    const navigate = useNavigate();
    const [isDragActive, setIsDragActive] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(true);
    };

    const handleDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);
    };

    const handleDrop = async (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);

        const file = e.dataTransfer.files?.[0];
        if (file && file.type === 'application/pdf') {
            await uploadFile(file);
        } else {
            alert('Por favor, envie um arquivo .pdf');
        }
    };

    const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            await uploadFile(file);
        }
    };

    const uploadFile = async (file: File) => {
        setIsProcessing(true);
        const docId = await processNewDocument(file);
        setIsProcessing(false);
        navigate(`/resultado/${docId}`);
    };

    return (
        <Card
            className={`w-full max-w-2xl mx-auto drop-zone border-2 border-dashed transition-all duration-300 rounded-2xl cursor-pointer ${isDragActive ? 'border-primary bg-primary/10 shadow-md' : 'border-muted-foreground/30 hover:border-primary/50 hover:bg-muted/5'}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById('file-upload')?.click()}
        >
            <div className="pointer-events-none">
                <CardHeader className="text-center pt-10">
                    <div className="flex justify-center mb-6">
                        {isProcessing ? (
                            <div className="h-16 w-16 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
                        ) : isDragActive ? (
                            <div className="bg-primary/20 p-4 rounded-full">
                                <FileType className="w-12 h-12 text-primary animate-bounce" />
                            </div>
                        ) : (
                            <div className="bg-muted p-4 rounded-full">
                                <UploadCloud className="w-12 h-12 text-muted-foreground" />
                            </div>
                        )}
                    </div>
                    <CardTitle className="mb-2 text-2xl">
                        {isProcessing
                            ? 'Analisando Histórico...'
                            : isDragActive
                              ? 'Pode Soltar o Arquivo!'
                              : 'Enviar Histórico Escolar'}
                    </CardTitle>
                    <CardDescription className="text-base">
                        {isProcessing
                            ? 'Por favor, aguarde enquanto compilamos seu documento...'
                            : 'Arraste e solte o arquivo PDF aqui ou clique para buscar'}
                    </CardDescription>
                </CardHeader>

                {!isProcessing && (
                    <CardContent className="flex justify-center pb-10">
                        <input
                            id="file-upload"
                            type="file"
                            accept=".pdf"
                            className="hidden"
                            onChange={handleFileSelect}
                        />
                    </CardContent>
                )}
            </div>
        </Card>
    );
};
