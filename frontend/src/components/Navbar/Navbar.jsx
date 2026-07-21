import React, { useState, useEffect, useRef } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useTheme } from '../../context/ThemeContext';
import UploadTicketModal from '../UploadTicketModal/UploadTicketModal';
import './Navbar.css';

const Navbar = () => {
    const { user, isAuthenticated, logout } = useAuth();
    const { theme, toggleTheme } = useTheme();
    const [scrolled, setScrolled] = useState(false);
    const [menuOpen, setMenuOpen] = useState(false);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
    const location = useLocation();
    const isHomePage = location.pathname === '/';
    const dropdownRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setDropdownOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 50);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    // Close menu when route changes
    useEffect(() => {
        setMenuOpen(false);
        setDropdownOpen(false);
    }, [location]);

    const navClass = `navbar ${scrolled ? 'navbar-scrolled' : ''} ${!isHomePage ? 'navbar-solid' : ''}`;

    return (
        <header>
            <nav className={navClass}>
                <div className="navbar-container">
                    <Link to="/" className="navbar-logo">
                        <span className="logo-icon">🏛️</span>
                        <span className="logo-text">HeritageHub</span>
                    </Link>

                    <div className={`navbar-links ${menuOpen ? 'active' : ''}`}>
                        <Link to="/explore" className="nav-link">Explore</Link>
                        <Link to="/map" className="nav-link">Map</Link>
                        <Link to="/categories" className="nav-link">Categories</Link>

                        <Link to="/about" className="nav-link">About</Link>
                        
                        <button className="theme-toggle btn-icon" onClick={toggleTheme} aria-label="Toggle theme">
                            {theme === 'light' ? '🌙' : '☀️'}
                        </button>

                        {isAuthenticated ? (
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                <button className="btn btn-outline nav-upload-btn" onClick={() => setIsUploadModalOpen(true)}>
                                    + Upload Ticket
                                </button>
                                <div className="user-menu-wrapper" ref={dropdownRef}>
                                <button 
                                    className="user-btn" 
                                    onClick={() => setDropdownOpen(!dropdownOpen)}
                                >
                                    {user.avatar ? (
                                        <img src={user.avatar} alt="Avatar" className="user-avatar" />
                                    ) : (
                                        <div className="user-avatar-placeholder">
                                            {user.first_name?.[0] || user.username?.[0] || 'U'}
                                        </div>
                                    )}
                                    <span className="user-name hide-mobile">{user.first_name || user.username}</span>
                                </button>

                                {dropdownOpen && (
                                    <div className="user-dropdown">
                                        <Link to="/profile" className="dropdown-item">Profile</Link>
                                        <Link to="/my-bookings" className="dropdown-item">My Bookings</Link>
                                        <Link to="/profile#external-tickets" className="dropdown-item">My Tickets</Link>
                                        <Link to="/wishlist" className="dropdown-item">Wishlist</Link>
                                        {user.role === 'admin' && (
                                            <Link to="/admin" className="dropdown-item admin-link">Admin Dashboard</Link>
                                        )}
                                        <div className="dropdown-divider"></div>
                                        <button onClick={logout} className="dropdown-item text-error">Logout</button>
                                    </div>
                                )}
                            </div>
                            </div>
                        ) : (
                            <div className="auth-buttons">
                                <Link to="/login" className="btn btn-ghost hide-mobile">Log in</Link>
                                <Link to="/register" className="btn btn-primary">Sign up</Link>
                            </div>
                        )}
                    </div>

                    <button 
                        className="mobile-menu-btn" 
                        onClick={() => setMenuOpen(!menuOpen)}
                    >
                        <span className={`hamburger ${menuOpen ? 'active' : ''}`}></span>
                    </button>
                </div>
            </nav>
            <UploadTicketModal 
                isOpen={isUploadModalOpen} 
                onClose={() => setIsUploadModalOpen(false)}
                onUploadSuccess={() => {
                    // Optional: show a toast or message
                }}
            />
        </header>
    );
};

export default Navbar;
