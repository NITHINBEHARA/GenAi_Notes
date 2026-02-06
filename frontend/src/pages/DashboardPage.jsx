import React from 'react';
import { Card } from '../components/ui/Card';
import { useAuth } from '../context/AuthContext';

const DashboardPage = () => {
    const { tenantId } = useAuth();
    return (
        <div className="dashboard-overview">
            <h1>Welcome Back</h1>
            <p style={{ color: '#666', marginBottom: '2rem' }}>Overview for {tenantId}</p>

            <div className="stats-grid">
                <Card title="Total Documents">
                    <div className="stat-value">12</div>
                    <div className="stat-label">Uploaded</div>
                </Card>
                <Card title="Knowledge Base">
                    <div className="stat-value active">Active</div>
                    <div className="stat-label">Status</div>
                </Card>
                <Card title="Total Queries">
                    <div className="stat-value">148</div>
                    <div className="stat-label">This Month</div>
                </Card>
            </div>

            <div className="recent-activity">
                <h3>Recent Activity</h3>
                <p>No recent activity.</p>
            </div>
        </div>
    );
};

export default DashboardPage;
