import React from 'react';
import Sidebar from './Sidebar';
import { useAuth } from '../../context/AuthContext';
import { Menu } from 'lucide-react';

const DashboardLayout = ({ children }) => {
    const { user, tenantId } = useAuth();

    return (
        <div className="dashboard-layout">
            <Sidebar />
            <div className="main-content">
                <header className="top-bar">
                    <div className="breadcrumb">
                        Dashboard
                    </div>
                    <div className="user-info">
                        <span className="tenant-badge">Tenant: {tenantId}</span>
                        <span className="user-name">{user?.name}</span>
                    </div>
                </header>
                <main className="page-content">
                    {children}
                </main>
            </div>
        </div>
    );
};

export default DashboardLayout;
