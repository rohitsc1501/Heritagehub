import React, { useState } from 'react';
import './Pages.css';

const Contact = () => {
    const [formData, setFormData] = useState({ name: '', email: '', message: '' });
    const [status, setStatus] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        setStatus('sending');
        setTimeout(() => {
            setStatus('success');
            setFormData({ name: '', email: '', message: '' });
        }, 1000);
    };

    return (
        <div className="page-active">
            <div className="container section">
                <div className="page-header text-center">
                    <h1 className="section-title">Contact Us</h1>
                    <p className="section-subtitle">Have a question or need assistance? We're here to help.</p>
                </div>

                <div className="contact-grid">
                    <div className="contact-info card">
                        <h3>Get in Touch</h3>
                        <p className="text-muted mb-xl">Fill out the form and our team will get back to you within 24 hours.</p>
                        
                        <div className="info-item">
                            <span className="icon">📍</span>
                            <div>
                                <strong>Address</strong>
                                <p>123 Heritage Marg, New Delhi, India 110001</p>
                            </div>
                        </div>
                        
                        <div className="info-item">
                            <span className="icon">📞</span>
                            <div>
                                <strong>Phone</strong>
                                <p>+91 11 2345 6789</p>
                            </div>
                        </div>
                        
                        <div className="info-item">
                            <span className="icon">✉️</span>
                            <div>
                                <strong>Email</strong>
                                <p>support@heritagehub.in</p>
                            </div>
                        </div>
                    </div>

                    <div className="contact-form card">
                        <h3>Send a Message</h3>
                        
                        {status === 'success' && (
                            <div className="auth-alert success mb-md">
                                Your message has been sent successfully!
                            </div>
                        )}

                        <form onSubmit={handleSubmit} className="auth-form">
                            <div className="input-group">
                                <label>Full Name</label>
                                <input 
                                    type="text" 
                                    className="input-field" 
                                    value={formData.name}
                                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                                    required 
                                />
                            </div>
                            
                            <div className="input-group">
                                <label>Email Address</label>
                                <input 
                                    type="email" 
                                    className="input-field"
                                    value={formData.email}
                                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                                    required 
                                />
                            </div>
                            
                            <div className="input-group">
                                <label>Message</label>
                                <textarea 
                                    className="input-field" 
                                    rows="5"
                                    value={formData.message}
                                    onChange={(e) => setFormData({...formData, message: e.target.value})}
                                    required 
                                ></textarea>
                            </div>
                            
                            <button 
                                type="submit" 
                                className="btn btn-primary mt-md"
                                disabled={status === 'sending'}
                            >
                                {status === 'sending' ? 'Sending...' : 'Send Message'}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Contact;
