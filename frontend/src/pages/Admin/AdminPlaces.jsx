import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { PageLoader } from '../../components/Loader/Loader';
import { placeService } from '../../services/placeService';
import { formatCurrency } from '../../utils/formatters';

const AdminPlaces = () => {
    const [places, setPlaces] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPlaces = async () => {
            try {
                // Using existing placeService to get places for admin
                const data = await placeService.getPlaces({ limit: 50 });
                setPlaces(data.results || data);
            } catch (error) {
                console.error("Error fetching places", error);
            } finally {
                setLoading(false);
            }
        };

        fetchPlaces();
    }, []);

    if (loading) return <PageLoader />;

    return (
        <div className="admin-page">
            <div className="admin-page-header">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                        <h1 className="section-title">Manage Places</h1>
                        <p className="text-muted">View and manage all destination places.</p>
                    </div>
                    <button className="btn btn-primary">
                        <span className="icon">+</span> Add New Place
                    </button>
                </div>
            </div>

            <div className="card mt-lg">
                <div className="table-responsive">
                    <table className="admin-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Place Name</th>
                                <th>Category</th>
                                <th>Location</th>
                                <th>Entry Fee (INR)</th>
                                <th>UNESCO</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {places.map(place => (
                                <tr key={place.id}>
                                    <td>#{place.id}</td>
                                    <td><strong>{place.place_name}</strong></td>
                                    <td>{place.category_name}</td>
                                    <td>{place.city_name}, {place.state_name}</td>
                                    <td>{place.entry_fee_indian ? formatCurrency(place.entry_fee_indian) : 'Free'}</td>
                                    <td>
                                        {place.unesco_status === 'Yes' ? 
                                            <span className="text-accent">★ Yes</span> : 'No'}
                                    </td>
                                    <td>
                                        <span className="badge badge-success">Active</span>
                                    </td>
                                    <td>
                                        <button className="btn btn-sm btn-ghost text-primary">Edit</button>
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

export default AdminPlaces;
