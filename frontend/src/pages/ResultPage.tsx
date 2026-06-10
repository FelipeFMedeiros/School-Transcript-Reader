import { useEffect, useState } from 'react';
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
    const { activeDocumentDetail, fetchDocument, isLoading } = useCompilerStore();
    const [activeTab, setActiveTab] = useState<'dashboard' | 'symbols'>('dashboard');

    useEffect(() => {
        if (id) fetchDocument(id);
    }, [id, fetchDocument]);

    if (isLoading) {
        return (
            <div className="flex-1 flex flex-col items-center justify-center text-center">
                Carregando detalhes do documento...
            </div>
        );
    }

    if (!activeDocumentDetail) {
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
                <h1 className="text-2xl font-bold text-gray-900 truncate">
                    Resultados: {activeDocumentDetail.fileName}
                </h1>
            </div>

            <div className="flex space-x-2 mb-6 p-1 bg-gray-100/80 rounded-lg max-w-fit mx-auto sm:mx-0 shadow-sm border border-gray-200/50">
                <button
                    onClick={() => setActiveTab('dashboard')}
                    className={`px-5 py-2.5 text-sm font-medium rounded-md transition-all duration-200 hover:cursor-pointer ${activeTab === 'dashboard' ? 'bg-white text-primary shadow-sm ring-1 ring-black/5' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-200/50'}`}
                >
                    Visão Geral
                </button>
                <button
                    onClick={() => setActiveTab('symbols')}
                    className={`px-5 py-2.5 text-sm font-medium rounded-md transition-all duration-200 hover:cursor-pointer ${activeTab === 'symbols' ? 'bg-white text-primary shadow-sm ring-1 ring-black/5' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-200/50'}`}
                >
                    Tabela de Símbolos (Debug)
                </button>
            </div>

            <div className="w-full pb-8">
                {activeTab === 'dashboard' ? (
                    <div className="max-w-4xl mx-auto h-full animate-in fade-in slide-in-from-bottom-2 duration-300">
                        {activeDocumentDetail.status === 'success' ? <SuccessDashboard /> : <ErrorConsole />}
                    </div>
                ) : (
                    <div className="w-full animate-in fade-in slide-in-from-bottom-2 duration-300">
                        <SymbolTable />
                    </div>
                )}
            </div>
        </div>
    );
};
