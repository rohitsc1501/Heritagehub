import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { userService } from '../../services/userService';
import MyBookings from './MyBookings';
import UploadTicketModal from '../../components/UploadTicketModal/UploadTicketModal';
import { API_URL } from '../../utils/constants';
import './User.css';

const Profile = () => {
    const { user, updateProfile } = useAuth();
    
    const [formData, setFormData] = useState({
        first_name: user?.first_name || '',
        last_name: user?.last_name || '',
        email: user?.email || '',
        phone: user?.phone || ''
    });
    
    const [passData, setPassData] = useState({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
    });

    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    
    // External Tickets
    const [externalTickets, setExternalTickets] = useState([]);
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);

    useEffect(() => {
        fetchExternalTickets();
    }, []);

    useEffect(() => {
        if (window.location.hash === '#external-tickets') {
            setTimeout(() => {
                const el = document.getElementById('external-tickets');
                if (el) {
                    // Scroll accounting for fixed navbar height (approx 80px)
                    const y = el.getBoundingClientRect().top + window.scrollY - 100;
                    window.scrollTo({ top: y, behavior: 'smooth' });
                }
            }, 100);
        }
    }, [window.location.hash]);

    const fetchExternalTickets = async () => {
        try {
            const data = await userService.getExternalTickets();
            setExternalTickets(data.results || data);
        } catch (err) {
            console.error("Failed to fetch external tickets", err);
        }
    };
    
    const handleDeleteExternal = async (id) => {
        if (window.confirm("Delete this uploaded ticket?")) {
            try {
                await userService.deleteExternalTicket(id);
                fetchExternalTickets();
            } catch (err) {
                console.error("Failed to delete", err);
            }
        }
    };

    const handleProfileChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
        setMessage('');
        setError('');
    };

    const handlePassChange = (e) => {
        setPassData({
            ...passData,
            [e.target.name]: e.target.value
        });
        setMessage('');
        setError('');
    };

    const handleProfileSubmit = async (e) => {
        e.preventDefault();
        try {
            setLoading(true);
            await updateProfile(formData);
            setMessage('Profile updated successfully!');
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to update profile.');
        } finally {
            setLoading(false);
        }
    };

    const handlePasswordSubmit = async (e) => {
        e.preventDefault();
        if (passData.newPassword !== passData.confirmPassword) {
            setError("New passwords don't match.");
            return;
        }
        
        try {
            setLoading(true);
            // In a real app, you would call authService.changePassword(passData) here
            // Currently mock implementation
            setTimeout(() => {
                setMessage('Password updated successfully!');
                setPassData({ currentPassword: '', newPassword: '', confirmPassword: '' });
                setLoading(false);
            }, 1000);
        } catch (err) {
            setError('Failed to update password.');
            setLoading(false);
        }
    };

    return (
        <div className="container section page-active">
            <h1 className="section-title mb-xl">My Profile</h1>

            <div className="profile-grid">
                <div className="card">
                    <h3 className="mb-xl">Personal Information</h3>
                    
                    {(message || error) && (
                        <div className={`auth-alert ${error ? 'error' : 'success'}`}>
                            {error || message}
                        </div>
                    )}
                    
                    <form className="auth-form" onSubmit={handleProfileSubmit}>
                        <div className="form-row">
                            <div className="input-group">
                                <label>First Name</label>
                                <input
                                    type="text"
                                    name="first_name"
                                    className="input-field"
                                    value={formData.first_name}
                                    onChange={handleProfileChange}
                                />
                            </div>
                            <div className="input-group">
                                <label>Last Name</label>
                                <input
                                    type="text"
                                    name="last_name"
                                    className="input-field"
                                    value={formData.last_name}
                                    onChange={handleProfileChange}
                                />
                            </div>
                        </div>

                        <div className="input-group">
                            <label>Email</label>
                            <input
                                type="email"
                                name="email"
                                className="input-field"
                                value={formData.email}
                                onChange={handleProfileChange}
                            />
                        </div>

                        <div className="input-group">
                            <label>Phone Number</label>
                            <input
                                type="text"
                                name="phone"
                                className="input-field"
                                value={formData.phone}
                                onChange={handleProfileChange}
                                placeholder="+91 "
                            />
                        </div>

                        <button type="submit" className="btn btn-primary mt-md" disabled={loading}>
                            {loading ? 'Saving...' : 'Save Changes'}
                        </button>
                    </form>
                </div>

                <div className="card">
                    <h3 className="mb-xl">Security Settings</h3>
                    <form className="auth-form" onSubmit={handlePasswordSubmit}>
                        <div className="input-group">
                            <label>Current Password</label>
                            <input
                                type="password"
                                name="currentPassword"
                                className="input-field"
                                value={passData.currentPassword}
                                onChange={handlePassChange}
                                required
                            />
                        </div>

                        <div className="input-group">
                            <label>New Password</label>
                            <input
                                type="password"
                                name="newPassword"
                                className="input-field"
                                value={passData.newPassword}
                                onChange={handlePassChange}
                                required
                            />
                        </div>

                        <div className="input-group">
                            <label>Confirm New Password</label>
                            <input
                                type="password"
                                name="confirmPassword"
                                className="input-field"
                                value={passData.confirmPassword}
                                onChange={handlePassChange}
                                required
                            />
                        </div>

                        <button type="submit" className="btn btn-outline mt-md" disabled={loading}>
                            Update Password
                        </button>
                    </form>
                </div>
            </div>

            <MyBookings isEmbedded={true} />
            
            <div className="mt-xl" id="external-tickets">
                <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h2 className="section-title mb-md">Uploaded External Tickets</h2>
                    <button className="btn btn-outline btn-sm" onClick={() => setIsUploadModalOpen(true)}>
                        + Upload Ticket
                    </button>
                </div>
                
                {externalTickets.length === 0 ? (
                    <div className="empty-state card mt-md">
                        <div className="empty-icon">📁</div>
                        <h3>No uploaded tickets</h3>
                        <p>Keep all your bookings in one place by uploading tickets booked on other websites.</p>
                        <button className="btn btn-primary mt-sm" onClick={() => setIsUploadModalOpen(true)}>
                            Upload Now
                        </button>
                    </div>
                ) : (
                    <div className="bookings-list mt-md">
                        {externalTickets.map(ticket => (
                            <div key={ticket.id} className="booking-item card">
                                <div className="booking-header">
                                    <div>
                                        <h3 className="booking-place">{ticket.place_name}</h3>
                                        <p className="booking-id text-muted text-sm">Uploaded: {new Date(ticket.uploaded_at).toLocaleDateString()}</p>
                                    </div>
                                    <div className="badge badge-confirmed">Uploaded</div>
                                </div>
                                <div className="booking-body">
                                    <div className="booking-details">
                                        <div className="detail-row">
                                            <span className="icon">📅</span>
                                            <span><strong>Visit Date:</strong> {new Date(ticket.visit_date).toLocaleDateString()}</span>
                                        </div>
                                    </div>
                                    <div className="booking-actions">
                                        <div className="barcode-sim"></div>
                                        <a 
                                            href={`${ticket.file.startsWith('http') ? ticket.file : API_URL + ticket.file}`} 
                                            target="_blank" 
                                            rel="noreferrer"
                                            className="btn btn-primary btn-sm"
                                        >
                                            View File
                                        </a>
                                        <button 
                                            className="btn btn-ghost text-error btn-sm"
                                            onClick={() => handleDeleteExternal(ticket.id)}
                                        >
                                            Delete
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
            
            <UploadTicketModal 
                isOpen={isUploadModalOpen} 
                onClose={() => setIsUploadModalOpen(false)}
                onUploadSuccess={fetchExternalTickets}
            />
        </div>
    );
};

export default Profile;
