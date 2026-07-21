import api from './api';

export const authService = {
    login: async (username, password) => {
        const response = await api.post('/auth/login/', { username, password });
        return response.data;
    },
    
    register: async (userData) => {
        const response = await api.post('/auth/register/', userData);
        return response.data;
    },
    
    logout: async () => {
        const refreshToken = localStorage.getItem('refreshToken');
        if (refreshToken) {
            try {
                await api.post('/auth/logout/', { refresh: refreshToken });
            } catch (error) {
                console.error('Logout error', error);
            }
        }
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
    },
    
    getProfile: async () => {
        const response = await api.get('/auth/profile/');
        return response.data;
    },
    
    updateProfile: async (userData) => {
        const response = await api.put('/auth/profile/', userData);
        return response.data;
    },
    
    changePassword: async (passwords) => {
        const response = await api.post('/auth/change-password/', passwords);
        return response.data;
    }
};
