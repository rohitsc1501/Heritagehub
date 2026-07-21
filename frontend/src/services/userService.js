import axios from 'axios';
import api from './api';

export const userService = {
    // Bookings
    getMyBookings: async () => {
        const response = await api.get('/bookings/my_bookings/');
        return response.data;
    },
    
    getBookingDetails: async (id) => {
        const response = await api.get(`/bookings/${id}/`);
        return response.data;
    },
    
    cancelBooking: async (id) => {
        const response = await api.post(`/bookings/${id}/cancel/`);
        return response.data;
    },
    
    // External Tickets
    getExternalTickets: async () => {
        const response = await api.get('/bookings/external/');
        return response.data;
    },
    
    uploadExternalTicket: async (formData) => {
        const token = localStorage.getItem('accessToken');
        const response = await axios.post(`${api.defaults.baseURL}/bookings/external/`, formData, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return response.data;
    },
    
    deleteExternalTicket: async (id) => {
        const response = await api.delete(`/bookings/external/${id}/`);
        return response.data;
    },

    // Wishlist
    getWishlist: async () => {
        const response = await api.get('/wishlist/');
        return response.data;
    },
    
    clearWishlist: async () => {
        const response = await api.post('/wishlist/clear/');
        return response.data;
    },
    
    // Notifications
    getNotifications: async () => {
        const response = await api.get('/notifications/');
        return response.data;
    },
    
    markNotificationRead: async (id) => {
        const response = await api.post(`/notifications/${id}/mark_read/`);
        return response.data;
    },
    
    markAllNotificationsRead: async () => {
        const response = await api.post('/notifications/mark_all_read/');
        return response.data;
    }
};
