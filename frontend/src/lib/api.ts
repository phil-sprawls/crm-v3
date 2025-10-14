import axios from 'axios';
import { Account, UseCase, Update, Platform, PrimaryITPartner } from '../types';

const getApiBaseUrl = () => {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  if (hostname.includes('replit.dev')) {
    return `${protocol}//${hostname}:8000`;
  }
  
  return 'http://localhost:8000';
};

const API_BASE_URL = getApiBaseUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const accountsApi = {
  getAll: () => api.get<Account[]>('/api/accounts'),
  getOne: (uid: string) => api.get<Account>(`/api/accounts/${uid}`),
  create: (data: Account) => api.post<Account>('/api/accounts', data),
  update: (uid: string, data: Partial<Account>) => api.put<Account>(`/api/accounts/${uid}`, data),
  delete: (uid: string) => api.delete(`/api/accounts/${uid}`),
  getUseCases: (uid: string) => api.get<UseCase[]>(`/api/accounts/${uid}/use-cases`),
  getUpdates: (uid: string) => api.get<Update[]>(`/api/accounts/${uid}/updates`),
  getPlatforms: (uid: string) => api.get<Platform[]>(`/api/accounts/${uid}/platforms`),
  getPrimaryITPartner: (uid: string) => api.get<PrimaryITPartner>(`/api/accounts/${uid}/primary-it-partner`),
};

export const useCasesApi = {
  create: (data: UseCase) => api.post<UseCase>('/api/use-cases', data),
  update: (id: number, data: Partial<UseCase>) => api.put<UseCase>(`/api/use-cases/${id}`, data),
  delete: (id: number) => api.delete(`/api/use-cases/${id}`),
};

export const updatesApi = {
  create: (data: Update) => api.post<Update>('/api/updates', data),
  update: (id: number, data: Partial<Update>) => api.put<Update>(`/api/updates/${id}`, data),
  delete: (id: number) => api.delete(`/api/updates/${id}`),
};

export const platformsApi = {
  create: (data: Platform) => api.post<Platform>('/api/platforms', data),
  update: (id: number, data: Partial<Platform>) => api.put<Platform>(`/api/platforms/${id}`, data),
  delete: (id: number) => api.delete(`/api/platforms/${id}`),
};

export const primaryITPartnersApi = {
  create: (data: PrimaryITPartner) => api.post<PrimaryITPartner>('/api/primary-it-partners', data),
  update: (id: number, data: Partial<PrimaryITPartner>) => api.put<PrimaryITPartner>(`/api/primary-it-partners/${id}`, data),
  delete: (id: number) => api.delete(`/api/primary-it-partners/${id}`),
};
