import React from 'react';

export const Card = ({ children, className = '', title }) => {
    return (
        <div className={`card ${className}`}>
            {title && <div className="card-header"><h3>{title}</h3></div>}
            <div className="card-body">
                {children}
            </div>
        </div>
    );
};
