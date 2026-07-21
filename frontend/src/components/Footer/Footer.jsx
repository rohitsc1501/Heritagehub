import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="container">
                <div className="footer-grid">
                    <div className="footer-brand">
                        <Link to="/" className="footer-logo">
                            <span className="logo-icon">🏛️</span>
                            <span className="logo-text">HeritageHub</span>
                        </Link>
                        <p className="footer-description">
                            Discover and explore India's timeless cultural heritage. 
                            Book tickets, plan your journey, and create unforgettable memories.
                        </p>
                        <div className="social-links">
                            <a href="#" className="social-icon">IG</a>
                            <a href="#" className="social-icon">FB</a>
                            <a href="#" className="social-icon">TW</a>
                            <a href="#" className="social-icon">YT</a>
                        </div>
                    </div>

                    <div className="footer-links">
                        <h4 className="footer-title">Explore</h4>
                        <Link to="/explore">All Places</Link>
                        <Link to="/categories">Categories</Link>
                        <Link to="/explore?unesco=Yes">UNESCO Sites</Link>
                        <Link to="/events">Upcoming Events</Link>
                    </div>

                    <div className="footer-links">
                        <h4 className="footer-title">Support</h4>
                        <Link to="/about">About Us</Link>
                        <Link to="/contact">Contact</Link>
                        <Link to="/faq">FAQs</Link>
                        <Link to="/terms">Terms & Conditions</Link>
                    </div>

                    <div className="footer-newsletter">
                        <h4 className="footer-title">Newsletter</h4>
                        <p>Subscribe for travel tips and updates.</p>
                        <form className="newsletter-form" onSubmit={(e) => e.preventDefault()}>
                            <input type="email" placeholder="Your email address" required />
                            <button type="submit" className="btn btn-primary">Subscribe</button>
                        </form>
                    </div>
                </div>

                <div className="footer-bottom">
                    <p>&copy; {new Date().getFullYear()} HeritageHub. Made with <span className="heart">❤️</span> in India.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
