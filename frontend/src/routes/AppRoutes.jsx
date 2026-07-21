import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Layouts
import MainLayout from '../layouts/MainLayout';
import AdminLayout from '../layouts/AdminLayout';

// Pages
import Home from '../pages/Home/Home';
import Login from '../pages/Auth/Login';
import Register from '../pages/Auth/Register';
import Explore from '../pages/Explore/Explore';
import PlaceDetails from '../pages/PlaceDetails/PlaceDetails';
import MyBookings from '../pages/User/MyBookings';
import Wishlist from '../pages/User/Wishlist';
import Profile from '../pages/User/Profile';
import Dashboard from '../pages/Admin/Dashboard';
import AdminUsers from '../pages/Admin/AdminUsers';
import AdminBookings from '../pages/Admin/AdminBookings';
import AdminPlaces from '../pages/Admin/AdminPlaces';
import About from '../pages/Static/About';
import Contact from '../pages/Static/Contact';
import PlacesMap from '../pages/Map/Map';

// Public Pages (Placeholders for now)

// Protected Route Component
const ProtectedRoute = ({ children, requireAdmin = false }) => {
    const { isAuthenticated, isAdmin, loading } = useAuth();
    
    if (loading) return <div className="page-loader"><div className="loader-spinner"></div></div>;
    
    if (!isAuthenticated) return <Navigate to="/login" replace />;
    if (requireAdmin && !isAdmin) return <Navigate to="/" replace />;
    
    return children;
};

const AppRoutes = () => {
    return (
        <Routes>
            {/* Public Routes with MainLayout */}
            <Route element={<MainLayout />}>
                <Route path="/" element={<Home />} />
                <Route path="/explore" element={<Explore />} />
                <Route path="/map" element={<PlacesMap />} />
                <Route path="/about" element={<About />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/place/:slug" element={<PlaceDetails />} />
                
                {/* Protected Routes (Visitor) */}
                <Route path="/my-bookings" element={
                    <ProtectedRoute><MyBookings /></ProtectedRoute>
                } />
                <Route path="/wishlist" element={
                    <ProtectedRoute><Wishlist /></ProtectedRoute>
                } />
                <Route path="/profile" element={
                    <ProtectedRoute><Profile /></ProtectedRoute>
                } />
            </Route>

            {/* Admin Routes */}
            <Route path="/admin" element={
                <ProtectedRoute requireAdmin={true}><AdminLayout /></ProtectedRoute>
            }>
                <Route index element={<Dashboard />} />
                <Route path="users" element={<AdminUsers />} />
                <Route path="bookings" element={<AdminBookings />} />
                <Route path="places" element={<AdminPlaces />} />
            </Route>
            
            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
};

export default AppRoutes;
