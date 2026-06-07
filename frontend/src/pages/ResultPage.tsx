import { useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useCompilerStore } from '@/store/compilerStore';
import { SymbolTable } from '@/components/SymbolTable';
import { SuccessDashboard } from '@/components/SuccessDashboard';
import { ErrorConsole } from '@/components/ErrorConsole';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';

export const ResultPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { history, setActiveDocument } = useCompilerStore();

    const document = history.find((doc) => doc.id === id);

    useEffect(() => {
        if (id) setActiveDocument(id);
    }, [id, setActiveDocument]);

    if (!document) {
        return (
            <div className="flex-1 flex flex-col items-center justify-center text-center">
                <h2 className="text-2xl font-bold mb-2">Documento não encontrado</h2>
                <p className="text-gray-500 mb-6">A análise que você procura não está no histórico.</p>
                <Link to="/historico">
                    <Button>Voltar ao Histórico</Button>
                </Link>
            </div>
        );
    }

    return (
        <div className="flex-1 w-full animate-in fade-in duration-500">
            <div className="mb-6 flex items-center">
                <Button
                    variant="ghost"
                    onClick={() => navigate(-1)}
                    className="mr-4 text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors duration-200 hover:cursor-pointer"
                >
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Voltar
                </Button>
                <h1 className="text-2xl font-bold text-gray-900 truncate">Resultados: {document.fileName}</h1>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 w-full pb-8">
                <div className="lg:col-span-6">
                    <SymbolTable />
                </div>
                <div className="lg:col-span-6 h-full">
                    {document.status === 'success' ? <SuccessDashboard /> : <ErrorConsole />}
                </div>
            </div>
        </div>
    );
};
