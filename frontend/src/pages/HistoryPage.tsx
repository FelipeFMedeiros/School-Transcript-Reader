import { Link } from 'react-router-dom';
import { useCompilerStore } from '@/store/compilerStore';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { FileText, ArrowRight, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';

export const HistoryPage = () => {
    const { history, clearHistory } = useCompilerStore();

    return (
        <div className="flex-1 w-full max-w-5xl mx-auto py-8 animate-in fade-in duration-500">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Histórico de Análises</h1>
                    <p className="text-gray-500 mt-1">Todos os documentos processados no seu navegador recetemente.</p>
                </div>
                {history.length > 0 && (
                    <Button
                        variant="outline"
                        className="text-red-500 hover:text-red-600 hover:bg-red-50 hover:cursor-pointer hover:shadow-md"
                        onClick={clearHistory}
                    >
                        <Trash2 className="w-4 h-4 mr-2" />
                        Limpar Histórico
                    </Button>
                )}
            </div>

            {history.length === 0 ? (
                <Card className="border-dashed shadow-none bg-gray-50/50">
                    <CardContent className="flex flex-col items-center justify-center py-16 text-center">
                        <FileText className="w-16 h-16 text-gray-300 mb-4" />
                        <h3 className="text-xl font-semibold text-gray-700">Nenhum documento</h3>
                        <p className="text-gray-500 mt-2 mb-6">Você ainda não analisou nenhum histórico hoje.</p>
                        <Link to="/">
                            <Button className="bg-gray-500 hover:bg-gray-600 text-white hover:shadow-md hover:cursor-pointer">
                                Fazer primeiro upload
                            </Button>
                        </Link>
                    </CardContent>
                </Card>
            ) : (
                <div className="grid gap-4">
                    {history.map((doc) => (
                        <Card key={doc.id} className="overflow-hidden hover:shadow-md transition-shadow">
                            <div className="flex items-center p-4 sm:p-6">
                                <div className="bg-primary/10 p-3 rounded-xl mr-4 sm:mr-6">
                                    <FileText className="w-6 h-6 text-primary" />
                                </div>
                                <div className="flex-1">
                                    <h3 className="font-semibold text-lg text-gray-900 line-clamp-1">{doc.fileName}</h3>
                                    <div className="flex items-center gap-3 mt-1 text-sm text-gray-500">
                                        <span>{doc.date}</span>
                                        <span>•</span>
                                        <Badge
                                            variant={doc.status === 'success' ? 'default' : 'destructive'}
                                            className="font-normal capitalize shadow-none"
                                        >
                                            {doc.status === 'success' ? 'Sucesso' : 'Erro Encontrado'}
                                        </Badge>
                                    </div>
                                </div>
                                <Link to={`/resultado/${doc.id}`}>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        className="hidden sm:flex hover:text-gray-700 transition-colors duration-200 hover:cursor-pointer"
                                    >
                                        Ver Detalhes
                                        <ArrowRight className="w-4 h-4 ml-2" />
                                    </Button>
                                    <Button variant="ghost" size="icon" className="sm:hidden">
                                        <ArrowRight className="w-4 h-4" />
                                    </Button>
                                </Link>
                            </div>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
};
