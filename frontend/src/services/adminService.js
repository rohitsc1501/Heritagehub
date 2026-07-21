import api from './api';

export const adminService = {
    getStats: async () => {
        const response = await api.get('/dashboard/stats/');
        return response.data;
    },
    
    getMonthlyRevenue: async () => {
        const response = await api.get('/dashboard/charts/monthly-revenue/');
        return response.data;
    },
    
    getCategoryDistribution: async () => {
        const response = await api.get('/dashboard/charts/category-distribution/');
        return response.data;
    },
    
    getBookingsPerDay: async () => {
        const response = await api.get('/dashboard/charts/bookings-per-day/');
        return response.data;
    },
    
    getTopPlaces: async () => {
        const response = await api.get('/dashboard/charts/top-places/');
        return response.data;
    },
    
    getUsers: async () => {
        const response = await api.get('/dashboard/users/');
        return response.data;
    },
    
    getBookings: async () => {
        const response = await api.get('/dashboard/bookings/');
        return response.data;
    }
};
