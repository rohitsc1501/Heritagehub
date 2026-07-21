export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const TIME_SLOTS = [
    { value: '09:00-11:00', label: '9:00 AM - 11:00 AM' },
    { value: '11:00-13:00', label: '11:00 AM - 1:00 PM' },
    { value: '13:00-15:00', label: '1:00 PM - 3:00 PM' },
    { value: '15:00-17:00', label: '3:00 PM - 5:00 PM' },
    { value: '17:00-19:00', label: '5:00 PM - 7:00 PM' },
];

export const INDIAN_STATES = [
    "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam",
    "Bihar", "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli", "Daman and Diu",
    "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir",
    "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh",
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha",
    "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
    "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
];
