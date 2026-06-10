import { useCompilerStore } from '@/store/compilerStore';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export const SuccessDashboard = () => {
  const { activeDocumentDetail } = useCompilerStore(); 
  const studentData = activeDocumentDetail?.studentData || null;

  if (!studentData) {
    return (
      <Card className="h-full">
        <CardContent className="flex h-full items-center justify-center">
          <p className="text-muted-foreground">Nenhum dado disponível</p>
        </CardContent>
      </Card>
    );
  }

  const { nome, matricula, ira, disciplinas } = studentData;

  return (
    <Card className="h-full">
      <CardHeader className="pb-4">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          Dados Acadêmicos
          <Badge variant="secondary">
            {/* IRA badge */}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Student Info */}
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-sm">
            <span className="font-mono">Nome:</span>
            <span className="font-semibold">{nome}</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span className="font-mono">Matrícula:</span>
            <span className="font-semibold">{matricula}</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span className="font-mono">IRA:</span>
            <span className="font-semibold">{ira.toFixed(2)}</span>
          </div>
        </div>

        {/* Disciplinas */}
        <div>
          <h3 className="font-semibold mb-2">Disciplinas</h3>
          <div className="space-y-2">
            {disciplinas.map((disc) => (
              <div key={disc.codigo} className="flex justify-between items-center px-3 py-2 bg-muted/50 rounded-md">
                <div>
                  <span className="font-mono">{disc.codigo}</span>
                  <span className="ml-2 font-medium">{disc.nome}</span>
                </div>
                <div className="flex gap-3 text-sm">
                  <span className="font-mono">{disc.ch}h</span>
                  <Badge
                    variant={disc.situacao === 'APROVADO' ? 'default' : disc.situacao === 'EM CURSO' ? 'secondary' : 'destructive'}
                  >
                    {disc.situacao}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
