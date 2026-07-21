import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { userService } from '../../services/userService';
import { formatCurrency, formatDate } from '../../utils/formatters';
import { PageLoader } from '../../components/Loader/Loader';
import { API_URL } from '../../utils/constants';
import './User.css';

const MyBookings = ({ isEmbedded = false }) => {
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchBookings();
    }, []);

    const fetchBookings = async () => {
        try {
            setLoading(true);
            const data = await userService.getMyBookings();
            setBookings(data.results || data);
        } catch (error) {
            console.error("Error fetching bookings", error);
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = async (id) => {
        if (window.confirm("Are you sure you want to cancel this booking?")) {
            try {
                await userService.cancelBooking(id);
                fetchBookings(); // Refresh the list
            } catch (error) {
                console.error("Error cancelling booking", error);
                alert("Failed to cancel booking.");
            }
        }
    };

    if (loading) return <PageLoader />;

    return (
        <div className={isEmbedded ? "mt-xl" : "container section page-active"}>
            <h2 className="section-title mb-xl">{isEmbedded ? 'My Tickets' : 'My Bookings'}</h2>

            {bookings.length === 0 ? (
                <div className="empty-state card">
                    <div className="empty-icon">🎫</div>
                    <h3>No bookings yet</h3>
                    <p>You haven't made any bookings. Start exploring places to visit!</p>
                    <Link to="/explore" className="btn btn-primary mt-md">Explore Places</Link>
                </div>
            ) : (
                <div className="bookings-list">
                    {bookings.map(booking => (
                        <div key={booking.id} className="booking-item card">
                            <div className="booking-header">
                                <div>
                                    <h3 className="booking-place">{booking.place_name}</h3>
                                    <p className="booking-id text-muted text-sm">Booking ID: {booking.id}</p>
                                </div>
                                <div className={`badge badge-${booking.status.toLowerCase()}`}>
                                    {booking.status}
                                </div>
                            </div>

                            <div className="booking-body">
                                <div className="booking-details">
                                    <div className="detail-row">
                                        <span className="icon">📅</span>
                                        <span><strong>Date:</strong> {formatDate(booking.visit_date)}</span>
                                    </div>
                                    <div className="detail-row">
                                        <span className="icon">👥</span>
                                        <span><strong>Tickets:</strong> {booking.adults} Adults</span>
                                    </div>
                                    <div className="detail-row">
                                        <span className="icon">💰</span>
                                        <span><strong>Total Paid:</strong> {formatCurrency(booking.total_price)}</span>
                                    </div>
                                </div>

                                <div className="booking-actions">
                                <div className="barcode-sim"></div>
                                    {booking.status === 'Confirmed' && booking.qr_code && (
                                        <a 
                                            href={`${API_URL}${booking.qr_code}`} 
                                            target="_blank" 
                                            rel="noreferrer"
                                            className="btn btn-outline btn-sm"
                                        >
                                            View QR Code
                                        </a>
                                    )}
                                    {booking.status !== 'Cancelled' && (
                                        <button 
                                            className="btn btn-ghost text-error btn-sm"
                                            onClick={() => handleCancel(booking.id)}
                                        >
                                            Cancel Booking
                                        </button>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default MyBookings;
