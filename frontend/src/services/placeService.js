import api from './api';

export const placeService = {
    getPlaces: async (params = {}) => {
        const response = await api.get('/places/', { params });
        return response.data;
    },
    
    getPlace: async (slug) => {
        const response = await api.get(`/places/${slug}/`);
        return response.data;
    },
    
    getTrendingPlaces: async () => {
        const response = await api.get('/places/trending/');
        return response.data;
    },
    
    getUnescoPlaces: async () => {
        const response = await api.get('/places/unesco/');
        return response.data;
    },
    
    getTopRatedPlaces: async () => {
        const response = await api.get('/places/top_rated/');
        return response.data;
    },
    
    getNearbyPlaces: async (slug) => {
        const response = await api.get(`/places/${slug}/nearby/`);
        return response.data;
    },
    
    getCategories: async () => {
        const response = await api.get('/categories/');
        return response.data;
    },
    
    getCategoryPlaces: async (slug) => {
        const response = await api.get(`/categories/${slug}/places/`);
        return response.data;
    },
    
    getStates: async () => {
        const response = await api.get('/states/');
        return response.data;
    },
    
    getSearchSuggestions: async (query) => {
        const response = await api.get(`/places/search_suggestions/?q=${encodeURIComponent(query)}`);
        return response.data;
    }
};
