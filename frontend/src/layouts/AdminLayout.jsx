import React from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import './AdminLayout.css';

const AdminLayout = () => {
    const { user, logout } = useAuth();
    const { theme, toggleTheme } = useTheme();
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="admin-layout">
            <aside className="admin-sidebar">
                <div className="admin-brand">
                    <Link to="/" className="navbar-logo">
                        <span className="logo-icon">🏛️</span>
                        <span className="logo-text">HeritageHub</span>
                    </Link>
                </div>
                
                <nav className="admin-nav">
                    <div className="nav-label">Dashboard</div>
                    <Link to="/admin" className={`admin-nav-link ${location.pathname === '/admin' ? 'active' : ''}`}>
                        <span className="icon">📊</span> Overview
                    </Link>
                    <Link to="/admin/bookings" className={`admin-nav-link ${location.pathname === '/admin/bookings' ? 'active' : ''}`}>
                        <span className="icon">🎫</span> Bookings
                    </Link>
                    <Link to="/admin/places" className={`admin-nav-link ${location.pathname === '/admin/places' ? 'active' : ''}`}>
                        <span className="icon">📍</span> Places
                    </Link>
                    <Link to="/admin/users" className={`admin-nav-link ${location.pathname === '/admin/users' ? 'active' : ''}`}>
                        <span className="icon">👥</span> Users
                    </Link>
                </nav>
            </aside>

            <main className="admin-main">
                <header className="admin-header">
                    <h2 className="page-title">
                        {location.pathname === '/admin' ? 'Dashboard Overview' : 
                         location.pathname.split('/').pop().charAt(0).toUpperCase() + location.pathname.split('/').pop().slice(1)}
                    </h2>
                    
                    <div className="admin-header-actions">
                        <button className="theme-toggle btn-icon" onClick={toggleTheme}>
                            {theme === 'light' ? '🌙' : '☀️'}
                        </button>
                        
                        <div className="admin-user-menu">
                            <div className="user-info">
                                <span className="user-name">{user?.first_name || user?.username}</span>
                                <span className="user-role">Administrator</span>
                            </div>
                            <button className="btn btn-ghost text-error btn-sm" onClick={handleLogout}>
                                Logout
                            </button>
                        </div>
                    </div>
                </header>

                <div className="admin-content">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default AdminLayout;
