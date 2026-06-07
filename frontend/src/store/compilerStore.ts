import { create } from 'zustand';

export interface Symbol {
    id: string;
    token: string;
    valor: string;
    linha: number;
    tipo: string;
}

export interface CompilerError {
    fase: 'Léxica' | 'Sintática' | 'Semântica';
    mensagem: string;
    linha: number;
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

export interface Document {
    id: string;
    fileName: string;
    date: string;
    status: 'analyzing' | 'success' | 'error';
    symbolTable: Symbol[];
    errors: CompilerError[];
    studentData: StudentData | null;
}

interface CompilerState {
    history: Document[];
    activeDocumentId: string | null;

    // Actions
    processNewDocument: (file: File) => Promise<string>;
    setActiveDocument: (id: string) => void;
    clearHistory: () => void;
}

export const useCompilerStore = create<CompilerState>((set) => ({
    history: [],
    activeDocumentId: null,

    processNewDocument: async (file: File) => {
        const id = Date.now().toString();
        const date = new Date().toLocaleString('pt-BR');

        const newDoc: Document = {
            id,
            fileName: file.name,
            date,
            status: 'analyzing',
            symbolTable: [],
            errors: [],
            studentData: null,
        };

        set((state) => ({
            history: [newDoc, ...state.history],
            activeDocumentId: id,
        }));

        // Simulating processing time
        return new Promise((resolve) => {
            setTimeout(() => {
                // Generating mock data
                const success = Math.random() > 0.3; // 70% chance of success

                set((state) => ({
                    history: state.history.map((doc) => {
                        if (doc.id === id) {
                            if (success) {
                                return {
                                    ...doc,
                                    status: 'success',
                                    symbolTable: [
                                        { id: '1', token: 'NOME', valor: 'FELIPE', linha: 1, tipo: 'IDENTIFICADOR' },
                                        { id: '2', token: 'MATRICULA', valor: '2023000123', linha: 2, tipo: 'NUMERO' },
                                        {
                                            id: '3',
                                            token: 'CURSO',
                                            valor: 'CIENCIA DA COMPUTACAO',
                                            linha: 3,
                                            tipo: 'STRING',
                                        },
                                        {
                                            id: '4',
                                            token: 'DISCIPLINA',
                                            valor: 'CALCULO I',
                                            linha: 4,
                                            tipo: 'IDENTIFICADOR',
                                        },
                                        { id: '5', token: 'NOTA', valor: '8.5', linha: 5, tipo: 'FLOAT' },
                                    ],
                                    studentData: {
                                        nome: 'FELIPE MEDEIROS',
                                        matricula: '2023000123',
                                        ira: 8.7,
                                        disciplinas: [
                                            {
                                                codigo: 'CC101',
                                                nome: 'ALGORITMOS E ESTRUTURAS DE DADOS',
                                                ch: 60,
                                                situacao: 'APROVADO',
                                            },
                                            { codigo: 'MT101', nome: 'CALCULO I', ch: 60, situacao: 'APROVADO' },
                                        ],
                                    },
                                };
                            } else {
                                return {
                                    ...doc,
                                    status: 'error',
                                    symbolTable: [
                                        { id: '1', token: 'NOME', valor: 'FELIPE', linha: 1, tipo: 'IDENTIFICADOR' },
                                        { id: 'err1', token: 'UNKNOWN', valor: '@%*', linha: 2, tipo: 'ERRO_LEXICO' },
                                    ],
                                    errors: [
                                        {
                                            fase: 'Léxica',
                                            mensagem: 'Caracteres inválidos encontrados no cabeçalho.',
                                            linha: 2,
                                        },
                                    ],
                                };
                            }
                        }
                        return doc;
                    }),
                }));
                resolve(id);
            }, 2500);
        });
    },

    setActiveDocument: (id) => set({ activeDocumentId: id }),
    clearHistory: () => set({ history: [], activeDocumentId: null }),
}));
