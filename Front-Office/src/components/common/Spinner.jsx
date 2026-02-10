import React from 'react';
import './Spinner.css';

const Spinner = ({ 
  size = 'medium', 
  color = 'primary', 
  text = '', 
  overlay = false,
  className = '' 
}) => {
  const sizeClasses = {
    small: 'w-4 h-4',
    medium: 'w-8 h-8',
    large: 'w-12 h-12',
    xlarge: 'w-16 h-16'
  };

  const colorClasses = {
    primary: 'border-blue-600',
    secondary: 'border-gray-600',
    success: 'border-green-600',
    warning: 'border-yellow-600',
    danger: 'border-red-600',
    white: 'border-white'
  };

  const spinnerElement = (
    <div className={`spinner-container ${overlay ? 'spinner-overlay' : ''} ${className}`}>
      <div 
        className={`
          spinner 
          ${sizeClasses[size]} 
          ${colorClasses[color]}
          border-4 border-t-transparent rounded-full animate-spin
        `}
      />
      {text && (
        <p className={`spinner-text mt-2 text-sm ${color === 'white' ? 'text-white' : 'text-gray-600'}`}>
          {text}
        </p>
      )}
    </div>
  );

  if (overlay) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        {spinnerElement}
      </div>
    );
  }

  return spinnerElement;
};

// Composant Spinner avec points
export const DotSpinner = ({ color = 'primary', className = '' }) => {
  const colorClasses = {
    primary: 'bg-blue-600',
    secondary: 'bg-gray-600',
    success: 'bg-green-600',
    warning: 'bg-yellow-600',
    danger: 'bg-red-600'
  };

  return (
    <div className={`dot-spinner ${className}`}>
      <div className={`dot ${colorClasses[color]}`}></div>
      <div className={`dot ${colorClasses[color]}`}></div>
      <div className={`dot ${colorClasses[color]}`}></div>
    </div>
  );
};

// Composant Spinner en barres
export const BarSpinner = ({ color = 'primary', className = '' }) => {
  const colorClasses = {
    primary: 'bg-blue-600',
    secondary: 'bg-gray-600',
    success: 'bg-green-600',
    warning: 'bg-yellow-600',
    danger: 'bg-red-600'
  };

  return (
    <div className={`bar-spinner ${className}`}>
      {[...Array(5)].map((_, i) => (
        <div 
          key={i} 
          className={`bar ${colorClasses[color]}`}
          style={{ animationDelay: `${i * 0.1}s` }}
        ></div>
      ))}
    </div>
  );
};

export default Spinner;