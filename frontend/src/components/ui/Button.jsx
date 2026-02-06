import React from 'react';

export const Button = ({ children, onClick, type = 'button', variant = 'primary', className = '', disabled = false }) => {
    const baseStyle = "px-4 py-2 rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2";
    const variants = {
        primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
        secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-500",
        danger: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
        ghost: "bg-transparent text-gray-600 hover:bg-gray-100 hover:text-gray-900",
    };

    // Note: Using standard class names that mimic Tailwind for clarity, 
    // but assuming we will add global CSS to support these or use inline styles if strict vanilla.
    // Wait, I am NOT using Tailwind. I should use CSS Modules or standard CSS classes.
    // The user asked for vanilla CSS. I will use a .css file for this component or inline styles for simplicity in this artifact.
    // Actually, standard CSS classes defined in index.css is cleaner.

    return (
        <button
            type={type}
            className={`btn btn-${variant} ${className}`}
            onClick={onClick}
            disabled={disabled}
        >
            {children}
        </button>
    );
};
