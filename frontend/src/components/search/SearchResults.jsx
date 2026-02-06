import React, { useState } from 'react';

const SearchResults = ({ results }) => {
    const [selectedImage, setSelectedImage] = useState(null);

    console.log("Rendering SearchResults with:", results);

    if (!results) return null;

    return (
        <div className="results-container">
            {/* AI Answer */}
            <div className="result-card answer-card">
                <h3>AI Answer</h3>
                <div className="answer-content">
                    {results.answer}
                </div>
            </div>

            {/* Images */}
            {results.image_sources && results.image_sources.length > 0 && (
                <div className="images-section">
                    <h4>Relevant Figures</h4>
                    <div className="images-grid">
                        {results.image_sources.map((img, index) => (
                            <div
                                key={index}
                                className="image-item"
                                onClick={() => setSelectedImage(img)}
                                style={{ display: 'flex', flexDirection: 'column', height: 'auto' }}
                            >
                                <img src={img.url} alt={img.image_name} loading="lazy" />
                                <div className="image-info" style={{ padding: '8px', fontSize: '0.85em', color: '#555' }}>
                                    <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
                                        {img.source_document} | Pg {img.page_number}
                                    </div>
                                    <div style={{ fontSize: '0.8em', color: '#888', wordBreak: 'break-all', marginBottom: '8px' }}>
                                        {img.image_path}
                                    </div>
                                    {img.pdf_url && (
                                        <a
                                            href={img.pdf_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            onClick={(e) => e.stopPropagation()}
                                            style={{
                                                display: 'inline-block',
                                                backgroundColor: '#f0f4f8',
                                                padding: '4px 8px',
                                                borderRadius: '4px',
                                                color: '#007bff',
                                                textDecoration: 'none',
                                                fontSize: '0.8em',
                                                fontWeight: 'bold',
                                                border: '1px solid #d1d9e6'
                                            }}
                                        >
                                            View in PDF ↗
                                        </a>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Sources */}
            {results.text_sources && results.text_sources.length > 0 && (
                <div className="sources-section">
                    <h4>Text Sources</h4>
                    <div className="sources-list">
                        {results.text_sources.map((source, index) => (
                            <div key={index} className="source-item">
                                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                    <span className="source-title">{source.source_document || source.source}</span>
                                    <span className="source-page">Pg {source.page_number || source.page}</span>
                                    {source.score && <span className="source-score">Score: {typeof source.score === 'number' ? source.score.toFixed(2) : source.score}</span>}
                                </div>
                                {source.pdf_url && (
                                    <a
                                        href={source.pdf_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="view-pdf-link"
                                        style={{
                                            backgroundColor: '#e3f2fd',
                                            padding: '6px 12px',
                                            borderRadius: '6px',
                                            color: '#007bff',
                                            textDecoration: 'none',
                                            fontSize: '0.85em',
                                            fontWeight: 'bold',
                                            transition: 'background-color 0.2s'
                                        }}
                                    >
                                        Jump to Page ↗
                                    </a>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Lightbox for Image Preview */}
            {selectedImage && (
                <div
                    style={{
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        zIndex: 1000,
                        cursor: 'pointer'
                    }}
                    onClick={() => setSelectedImage(null)}
                >
                    <div
                        style={{ maxWidth: '90%', maxHeight: '90%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <img
                            src={selectedImage.url}
                            style={{ maxWidth: '100%', maxHeight: '80vh', objectFit: 'contain' }}
                        />
                        <div style={{ marginTop: '15px', textAlign: 'center' }}>
                            <p style={{ color: 'white', marginBottom: '10px' }}>
                                {selectedImage.image_name} (Page {selectedImage.page_number})
                            </p>
                            {selectedImage.pdf_url && (
                                <a
                                    href={selectedImage.pdf_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    style={{
                                        color: 'white',
                                        backgroundColor: '#007bff',
                                        padding: '5px 15px',
                                        borderRadius: '4px',
                                        textDecoration: 'none'
                                    }}
                                >
                                    Open PDF Source ↗
                                </a>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default SearchResults;
