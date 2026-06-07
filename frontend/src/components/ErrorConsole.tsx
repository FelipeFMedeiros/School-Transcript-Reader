import { useCompilerStore } from '@/store/compilerStore';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { CircleAlert } from 'lucide-react';

export const ErrorConsole = () => {
    const { history, activeDocumentId } = useCompilerStore();
    const document = history.find((doc) => doc.id === activeDocumentId);
    const errors = document?.errors || [];

    return (
        <Card className="h-full">
            <CardHeader className="flex items-center justify-between pb-4">
                <CardTitle className="text-lg font-semibold">Console de Erros</CardTitle>
                <CircleAlert className="h-4 w-4 text-destructive" />
            </CardHeader>
            <CardContent className="p-0">
                {errors.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">Nenhum erro detectado</div>
                ) : (
                    <div className="space-y-4">
                        {errors.map((error, index) => (
                            <Alert
                                key={index}
                                variant="destructive"
                                className="border-none bg-destructive/5 text-destructive"
                            >
                                <AlertTitle>
                                    {error.fase} - Linha {error.linha}
                                </AlertTitle>
                                <AlertDescription>{error.mensagem}</AlertDescription>
                            </Alert>
                        ))}
                    </div>
                )}
            </CardContent>
        </Card>
    );
};
