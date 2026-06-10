export type StatusEnum = 'pending' | 'processing' | 'success' | 'error';

export interface CompilerError {
    fase: string;
    mensagem: string;
    linha: number;
    column?: number | null;
}

export interface SymbolTableItem {
    id?: string;
    token?: string;
    valor?: string;
    linha?: number;
    tipo?: string;
    [key: string]: unknown;
}

export interface Disciplina {
    codigo: string;
    nome: string;
    ch: number;
    situacao: string;
}

export interface StudentData {
    nome: string;
    matricula: string;
    ira: number;
    disciplinas: Disciplina[];
}

export interface DocumentList {
    id: string;
    fileName: string;
    date: string;
    status: StatusEnum;
}

export interface PaginatedDocumentList {
    count: number;
    next: string | null;
    previous: string | null;
    results: DocumentList[];
}

export interface DocumentDetail {
    id: string;
    fileName: string;
    date: string;
    status: StatusEnum;
    processing_time_ms?: number | null;
    engine_version?: string;
    symbolTable: SymbolTableItem[];
    errors: CompilerError[];
    studentData: StudentData | null;
    syntaxTree: Record<string, unknown>;
    semanticAnalysis: Record<string, unknown>;
}
