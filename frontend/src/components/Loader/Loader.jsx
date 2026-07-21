import React from 'react';

export const PageLoader = () => (
    <div className="page-loader">
        <div className="loader-spinner"></div>
    </div>
);

export const Spinner = () => <div className="spinner-sm"></div>;

export const SkeletonCard = () => (
    <div className="card skeleton-card">
        <div className="skeleton" style={{ height: '60%', width: '100%', borderBottomLeftRadius: 0, borderBottomRightRadius: 0 }}></div>
        <div style={{ padding: '1rem' }}>
            <div className="skeleton skeleton-text" style={{ width: '80%' }}></div>
            <div className="skeleton skeleton-text" style={{ width: '60%' }}></div>
            <div className="skeleton skeleton-text" style={{ width: '40%', marginTop: '1rem' }}></div>
        </div>
    </div>
);
