import React, { useState } from 'react';
import SearchBar from '../components/search/SearchBar';
import SearchResults from '../components/search/SearchResults';
import { ragService } from '../services/api';
import { Link } from 'react-router-dom';

const LandingPage = () => {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async (query) => {
        setLoading(true);
        setError(null);
        setResults(null);

        try {
            const response = await ragService.query(query);
            console.log("RAG Search Response:", response.data);
            setResults(response.data);
        } catch (err) {
            console.error(err);
            setError("Failed to retrieve information. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="landing-page">
            <nav className="public-nav">
                <div className="brand">RAG Search</div>
                <Link to="/login" className="login-link">Admin Login</Link>
            </nav>

            <main className="search-wrapper">
                <div className="search-header">
                    <h1>Knowledge Base</h1>
                    <p>Instant answers from your company documents</p>
                </div>

                <SearchBar onSearch={handleSearch} isLoading={loading} />

                {error && <div className="error-message">{error}</div>}

                {loading && !results && (
                    <div className="loading-indicator">Thinking...</div>
                )}

                {results && <SearchResults results={results} />}
            </main>
        </div>
    );
};

export default LandingPage;
