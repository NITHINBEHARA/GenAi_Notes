import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Upload, FileText, LogOut } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const Sidebar = () => {
    const { logout } = useAuth();

    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <h2>RAG Admin</h2>
            </div>
            <nav className="sidebar-nav">
                <NavLink to="/dashboard" end className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <LayoutDashboard size={20} />
                    <span>Dashboard</span>
                </NavLink>
                <NavLink to="/dashboard/upload" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <Upload size={20} />
                    <span>Upload Documents</span>
                </NavLink>
                <NavLink to="/dashboard/documents" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <FileText size={20} />
                    <span>My Documents</span>
                </NavLink>
            </nav>
            <div className="sidebar-footer">
                <button onClick={logout} className="nav-item logout-btn">
                    <LogOut size={20} />
                    <span>Logout</span>
                </button>
            </div>
        </aside>
    );
};

export default Sidebar;
