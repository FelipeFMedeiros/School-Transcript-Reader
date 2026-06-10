import { create } from 'zustand';
import { HistoriesService } from '../services/histories.service';
import type { DocumentList, DocumentDetail } from '../types/api';

interface CompilerState {
    history: DocumentList[];
    activeDocumentId: string | null;
    activeDocumentDetail: DocumentDetail | null;
    isLoading: boolean;

    // Actions
    fetchHistories: () => Promise<void>;
    fetchDocument: (id: string) => Promise<void>;
    processNewDocument: (file: File) => Promise<string>;
    setActiveDocument: (id: string) => void;
    clearHistory: () => Promise<void>;
    deleteDocument: (id: string) => Promise<void>;
}

export const useCompilerStore = create<CompilerState>((set, get) => ({
    history: [],
    activeDocumentId: null,
    activeDocumentDetail: null,
    isLoading: false,

    fetchHistories: async () => {
        set({ isLoading: true });
        try {
            const data = await HistoriesService.list(1);
            set({ history: data.results, isLoading: false });
        } catch (error) {
            console.error('Failed to fetch histories', error);
            set({ isLoading: false });
        }
    },

    fetchDocument: async (id: string) => {
        set({ isLoading: true, activeDocumentId: id });
        try {
            const data = await HistoriesService.retrieve(id);
            set({ activeDocumentDetail: data, isLoading: false });
        } catch (error) {
            console.error(`Failed to fetch document ${id}`, error);
            set({ isLoading: false, activeDocumentDetail: null });
        }
    },

    processNewDocument: async (file: File) => {
        set({ isLoading: true });
        try {
            const data = await HistoriesService.create(file);
            set((state) => ({
                history: [
                    {
                        id: data.id,
                        fileName: data.fileName,
                        date: data.date,
                        status: data.status,
                    },
                    ...state.history,
                ],
                activeDocumentId: data.id,
                activeDocumentDetail: data,
                isLoading: false,
            }));
            return data.id;
        } catch (error) {
            console.error('Failed to process document', error);
            set({ isLoading: false });
            throw error;
        }
    },

    setActiveDocument: (id) => {
        set({ activeDocumentId: id });
    },

    clearHistory: async () => {
        const { history } = get();
        set({ isLoading: true });
        try {
            // Wait for all delete calls
            await Promise.all(history.map((doc) => HistoriesService.destroy(doc.id)));
            set({ history: [], activeDocumentId: null, activeDocumentDetail: null, isLoading: false });
        } catch (error) {
            console.error('Failed to clear history', error);
            set({ isLoading: false });
            // Refresh list in case of partial success
            get().fetchHistories();
        }
    },

    deleteDocument: async (id: string) => {
        try {
            await HistoriesService.destroy(id);
            set((state) => ({
                history: state.history.filter((d) => d.id !== id),
                activeDocumentId: state.activeDocumentId === id ? null : state.activeDocumentId,
                activeDocumentDetail: state.activeDocumentId === id ? null : state.activeDocumentDetail,
            }));
        } catch (error) {
            console.error(`Failed to delete document ${id}`, error);
        }
    },
}));
