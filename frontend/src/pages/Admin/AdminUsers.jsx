import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { PageLoader } from '../../components/Loader/Loader';
import { formatDate } from '../../utils/formatters';

const AdminUsers = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const data = await adminService.getUsers();
                setUsers(data);
            } catch (error) {
                console.error("Error fetching users", error);
            } finally {
                setLoading(false);
            }
        };

        fetchUsers();
    }, []);

    if (loading) return <PageLoader />;

    return (
        <div className="admin-page">
            <div className="admin-page-header">
                <h1 className="section-title">Manage Users</h1>
                <p className="text-muted">View and manage all registered users.</p>
            </div>

            <div className="card mt-lg">
                <div className="table-responsive">
                    <table className="admin-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Username</th>
                                <th>Email</th>
                                <th>Role</th>
                                <th>Joined</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map(user => (
                                <tr key={user.id}>
                                    <td>#{user.id}</td>
                                    <td>{user.first_name} {user.last_name}</td>
                                    <td>{user.username}</td>
                                    <td>{user.email}</td>
                                    <td>
                                        <span className={`badge ${user.role === 'admin' ? 'badge-primary' : 'badge-info'}`}>
                                            {user.role}
                                        </span>
                                    </td>
                                    <td>{formatDate(user.date_joined)}</td>
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

export default AdminUsers;
