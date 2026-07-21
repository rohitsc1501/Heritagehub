import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { formatCurrency } from '../../utils/formatters';
import { PageLoader } from '../../components/Loader/Loader';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import './Admin.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
    const [stats, setStats] = useState(null);
    const [monthlyRevenue, setMonthlyRevenue] = useState([]);
    const [categoryDist, setCategoryDist] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                setLoading(true);
                const [statsData, revData, catData] = await Promise.all([
                    adminService.getStats(),
                    adminService.getMonthlyRevenue(),
                    adminService.getCategoryDistribution()
                ]);
                
                setStats(statsData);
                setMonthlyRevenue(revData);
                setCategoryDist(catData);
            } catch (error) {
                console.error("Error fetching dashboard data", error);
            } finally {
                setLoading(false);
            }
        };

        fetchDashboardData();
    }, []);

    if (loading) return <PageLoader />;

    // Prepare chart data
    const revenueChartData = {
        labels: monthlyRevenue.map(d => {
            const date = new Date(d.month);
            return date.toLocaleString('default', { month: 'short', year: 'numeric' });
        }),
        datasets: [
            {
                label: 'Revenue (INR)',
                data: monthlyRevenue.map(d => d.total),
                borderColor: '#1a365d',
                backgroundColor: 'rgba(26, 54, 93, 0.1)',
                fill: true,
                tension: 0.4
            }
        ]
    };

    const categoryChartData = {
        labels: categoryDist.map(d => d.name),
        datasets: [
            {
                label: 'Places Count',
                data: categoryDist.map(d => d.count),
                backgroundColor: [
                    '#1a365d', '#d4a053', '#2d6a4f', '#c0603c', 
                    '#3d6098', '#e8c07a', '#40916c', '#e07850'
                ],
                borderWidth: 0,
            }
        ]
    };

    return (
        <div className="admin-dashboard page-active">
            {/* Stats Grid */}
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-icon bg-primary-light text-primary">👥</div>
                    <div className="stat-info">
                        <span className="stat-label">Total Users</span>
                        <span className="stat-value">{stats.total_users}</span>
                    </div>
                </div>
                
                <div className="stat-card">
                    <div className="stat-icon bg-success-light text-success">💰</div>
                    <div className="stat-info">
                        <span className="stat-label">Total Revenue</span>
                        <span className="stat-value">{formatCurrency(stats.revenue)}</span>
                    </div>
                </div>
                
                <div className="stat-card">
                    <div className="stat-icon bg-accent-light text-accent">🎫</div>
                    <div className="stat-info">
                        <span className="stat-label">Total Bookings</span>
                        <span className="stat-value">{stats.total_bookings}</span>
                    </div>
                </div>
                
                <div className="stat-card">
                    <div className="stat-icon bg-info-light text-info">📍</div>
                    <div className="stat-info">
                        <span className="stat-label">Active Places</span>
                        <span className="stat-value">{stats.total_places}</span>
                    </div>
                </div>
            </div>

            {/* Charts Row */}
            <div className="charts-grid">
                <div className="chart-card card">
                    <h3 className="chart-title">Revenue Overview</h3>
                    <div className="chart-container">
                        <Line 
                            data={revenueChartData} 
                            options={{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: { legend: { position: 'top' } }
                            }} 
                        />
                    </div>
                </div>

                <div className="chart-card card">
                    <h3 className="chart-title">Places by Category</h3>
                    <div className="chart-container">
                        <Doughnut 
                            data={categoryChartData} 
                            options={{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: { legend: { position: 'right' } },
                                cutout: '70%'
                            }} 
                        />
                    </div>
                </div>
            </div>

            {/* Bottom Row */}
            <div className="dashboard-insights card mt-xl">
                <h3 className="chart-title">Quick Insights</h3>
                <div className="insights-grid">
                    <div className="insight-item">
                        <span className="insight-label">Most Popular Destination</span>
                        <span className="insight-value">{stats.most_popular_place}</span>
                    </div>
                    <div className="insight-item">
                        <span className="insight-label">Top Category</span>
                        <span className="insight-value">{stats.top_category}</span>
                    </div>
                    <div className="insight-item">
                        <span className="insight-label">Bookings Today</span>
                        <span className="insight-value">{stats.today_bookings}</span>
                    </div>
                    <div className="insight-item">
                        <span className="insight-label">Pending Approvals</span>
                        <span className="insight-value text-warning">{stats.pending_bookings}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
