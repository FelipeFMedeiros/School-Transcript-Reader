import { api } from './api';
import type { PaginatedDocumentList, DocumentDetail } from '../types/api';

export const HistoriesService = {
    async list(page: number = 1): Promise<PaginatedDocumentList> {
        const response = await api.get<PaginatedDocumentList>(`/histories/?page=${page}`);
        return response.data;
    },

    async retrieve(id: string): Promise<DocumentDetail> {
        const response = await api.get<DocumentDetail>(`/histories/${id}/`);
        return response.data;
    },

    async create(file: File): Promise<DocumentDetail> {
        const formData = new FormData();
        formData.append('file', file);

        const response = await api.post<DocumentDetail>('/histories/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    async destroy(id: string): Promise<void> {
        await api.delete(`/histories/${id}/`);
    },
};
