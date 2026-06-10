import { useCompilerStore } from '@/store/compilerStore';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Code } from 'lucide-react';

export const SymbolTable = () => {
    const { activeDocumentDetail } = useCompilerStore();
    const symbolTable = activeDocumentDetail?.symbolTable || [];

    return (
        <Card className="h-full">
            <CardHeader className="flex items-center justify-between pb-4">
                <CardTitle className="text-lg font-semibold">Tabela de Símbolos</CardTitle>
                <Code className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent className="p-0">
                <ScrollArea className="h-full w-full">
                    {symbolTable.length === 0 ? (
                        <div className="text-center py-8 text-muted-foreground">Nenhum símbolo detectado ainda</div>
                    ) : (
                        <Table className="w-full">
                            <TableHeader>
                                <TableRow>
                                    <TableHead className="w-20">ID</TableHead>
                                    <TableHead className="w-24">Token</TableHead>
                                    <TableHead className="w-36">Valor</TableHead>
                                    <TableHead className="w-12">Linha</TableHead>
                                    <TableHead>Tipo</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {symbolTable.map((symbol) => (
                                    <TableRow key={symbol.id}>
                                        <TableCell className="font-mono">{symbol.id}</TableCell>
                                        <TableCell className="font-mono">{symbol.token}</TableCell>
                                        <TableCell className="font-mono">{symbol.valor}</TableCell>
                                        <TableCell className="font-mono text-center">{symbol.linha}</TableCell>
                                        <TableCell className="font-mono text-capitalize">{symbol.tipo}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                </ScrollArea>
            </CardContent>
        </Card>
    );
};
