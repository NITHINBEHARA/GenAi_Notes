import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [tenantId, setTenantId] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check local storage on mount
        const storedToken = localStorage.getItem('auth_token');
        const storedTenant = localStorage.getItem('tenant_id');
        const storedUser = localStorage.getItem('user_info');

        if (storedToken && storedTenant) {
            setUser(storedUser ? JSON.parse(storedUser) : { name: 'Admin' });
            setTenantId(storedTenant);
            setIsAuthenticated(true);
        }
        setLoading(false);
    }, []);

    const login = async (email, password) => {
        try {
            // In a real app, this calls the API
            // const response = await authService.login(email, password);
            // const { token, tenant_id, user } = response.data;

            // For ARCHITECTURE DEMO purposes (since no backend exists yet):
            // We simulate a successful login if fields are filled
            if (!email || !password) throw new Error("Invalid credentials");

            const mockResponse = {
                token: "demo_token_123",
                tenant_id: "tenant_" + email.split('@')[0], // Derive tenant from email for demo
                user: { email, name: email.split('@')[0] }
            };

            const { token, tenant_id, user: userInfo } = mockResponse;

            localStorage.setItem('auth_token', token);
            localStorage.setItem('tenant_id', tenant_id);
            localStorage.setItem('user_info', JSON.stringify(userInfo));

            setUser(userInfo);
            setTenantId(tenant_id);
            setIsAuthenticated(true);
            return true;
        } catch (error) {
            console.error("Login failed:", error);
            throw error;
        }
    };

    const logout = () => {
        authService.logout();
        setUser(null);
        setTenantId(null);
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ user, tenantId, isAuthenticated, login, logout, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
