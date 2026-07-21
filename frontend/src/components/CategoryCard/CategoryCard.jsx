import React from 'react';
import { Link } from 'react-router-dom';
import './CategoryCard.css';

const CategoryCard = ({ category }) => {
    return (
        <Link to={`/explore?category_slug=${category.slug}`} className="category-card">
            <div className="category-icon">{category.icon || '📍'}</div>
            <div className="category-info">
                <h3 className="category-name">{category.name}</h3>
                <span className="category-count">{category.place_count} Places</span>
            </div>
        </Link>
    );
};

export default CategoryCard;
