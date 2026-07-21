import React, { useState } from 'react';
import { userService } from '../../services/userService';
import './UploadTicketModal.css';

const UploadTicketModal = ({ isOpen, onClose, onUploadSuccess }) => {
    const [formData, setFormData] = useState({
        place_name: '',
        visit_date: '',
        file: null
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    // Reset when modal opens/closes
    React.useEffect(() => {
        if (isOpen) {
            setSuccess(false);
            setError('');
            setFormData({ place_name: '', visit_date: '', file: null });
        }
    }, [isOpen]);

    if (!isOpen) return null;

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            setFormData({
                ...formData,
                file: e.target.files[0]
            });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!formData.place_name || !formData.visit_date || !formData.file) {
            setError("All fields are required.");
            return;
        }

        try {
            setLoading(true);
            setError('');
            
            const submitData = new FormData();
            submitData.append('place_name', formData.place_name);
            submitData.append('visit_date', formData.visit_date);
            submitData.append('file', formData.file);

            await userService.uploadExternalTicket(submitData);
            setLoading(false);
            setSuccess(true);
            setFormData({ place_name: '', visit_date: '', file: null });
            if (onUploadSuccess) onUploadSuccess();
            
            // Auto close after 2 seconds
            setTimeout(() => {
                onClose();
            }, 2000);
        } catch (err) {
            setError("Failed to upload ticket. Please try again.");
            setLoading(false);
        }
    };

    return (
        <div className="modal-backdrop">
            <div className="modal-content upload-modal">
                <button className="modal-close" onClick={onClose}>×</button>
                <div className="modal-header-section">
                    <h2 className="mb-md" style={{ fontWeight: 800, textTransform: 'uppercase', letterSpacing: '1px' }}>Upload Ticket</h2>
                    <p className="text-muted text-sm">Booked on another platform? Upload your ticket PDF or Image to keep all your bookings in one place.</p>
                </div>
                
                <div className="modal-body-section">
                    {success ? (
                        <div className="empty-state">
                            <div className="empty-icon" style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎉</div>
                            <h3 style={{ color: '#059669' }}>Ticket Uploaded Successfully!</h3>
                            <p className="text-muted mt-sm">Your ticket has been securely added to your profile.</p>
                        </div>
                    ) : (
                        <>
                            {error && <div className="auth-alert error mb-md">{error}</div>}
                            
                            <form onSubmit={handleSubmit} className="upload-form">
                                <div className="input-group">
                                    <label>Place Name</label>
                        <input 
                            type="text" 
                            name="place_name"
                            className="input-field" 
                            placeholder="e.g. Taj Mahal"
                            value={formData.place_name}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    
                    <div className="input-group">
                        <label>Date of Visit</label>
                        <input 
                            type="date" 
                            name="visit_date"
                            className="input-field" 
                            value={formData.visit_date}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="input-group file-upload-group">
                        <label>Ticket File (PDF or Image)</label>
                        <input 
                            type="file" 
                            name="file"
                            id="ticket-file"
                            className="file-input"
                            accept=".pdf,image/*"
                            onChange={handleFileChange}
                            required
                        />
                        <label htmlFor="ticket-file" className="file-label">
                            <span className="file-icon">🎟️</span>
                            <span className="file-text">
                                {formData.file ? formData.file.name : "Click to select a file"}
                            </span>
                        </label>
                    </div>

                                <button type="submit" className="btn btn-primary mt-md w-100" disabled={loading}>
                                    {loading ? 'Uploading...' : 'Upload Ticket'}
                                </button>
                            </form>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default UploadTicketModal;
