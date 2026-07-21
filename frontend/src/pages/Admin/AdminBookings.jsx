import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { PageLoader } from '../../components/Loader/Loader';
import { formatDate, formatCurrency } from '../../utils/formatters';

const AdminBookings = () => {
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchBookings = async () => {
            try {
                const data = await adminService.getBookings();
                setBookings(data);
            } catch (error) {
                console.error("Error fetching bookings", error);
            } finally {
                setLoading(false);
            }
        };

        fetchBookings();
    }, []);

    if (loading) return <PageLoader />;

    return (
        <div className="admin-page">
            <div className="admin-page-header">
                <h1 className="section-title">Manage Bookings</h1>
                <p className="text-muted">View all platform bookings and statuses.</p>
            </div>

            <div className="card mt-lg">
                <div className="table-responsive">
                    <table className="admin-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Place</th>
                                <th>User</th>
                                <th>Visit Date</th>
                                <th>Amount</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {bookings.map(booking => (
                                <tr key={booking.id}>
                                    <td>#{booking.id}</td>
                                    <td><strong>{booking.place_name}</strong></td>
                                    <td>{booking.user_name || `User #${booking.user}`}</td>
                                    <td>{formatDate(booking.visit_date)}</td>
                                    <td>{formatCurrency(booking.total_price)}</td>
                                    <td>
                                        <span className={`badge badge-${booking.status.toLowerCase()}`}>
                                            {booking.status}
                                        </span>
                                    </td>
                                    <td>
                                        <button className="btn btn-sm btn-ghost text-primary">View</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default AdminBookings;
