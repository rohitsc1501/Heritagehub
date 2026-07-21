import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { formatCurrency, formatRating, truncateText } from '../../utils/formatters';
import api from '../../services/api';
import './PlaceCard.css';

const PlaceCard = ({ place }) => {
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();
    const [isWishlisted, setIsWishlisted] = useState(place.is_wishlisted || false);
    
    // Fallback image if null
    const imageUrl = place.main_image_url || 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=80';

    const handleWishlistClick = async (e) => {
        e.preventDefault(); // Prevent navigating to place details
        e.stopPropagation();
        
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }

        try {
            const res = await api.post('/wishlist/toggle/', { place_id: place.id });
            setIsWishlisted(res.data.is_wishlisted);
        } catch (error) {
            console.error('Wishlist error', error);
        }
    };

    return (
        <Link to={`/place/${place.slug}`} className="place-card">
            <div className="place-card-image">
                <img src={imageUrl} alt={place.place_name} loading="lazy" />
                
                {/* Badges */}
                <div className="place-badges">
                    {place.unesco_status === 'Yes' && <span className="badge badge-unesco">UNESCO</span>}
                    {place.asi_protected === 'Yes' && <span className="badge badge-asi">ASI</span>}
                </div>
                
                {/* Wishlist Button */}
                <button 
                    className={`wishlist-btn ${isWishlisted ? 'active' : ''}`}
                    onClick={handleWishlistClick}
                    aria-label="Toggle Wishlist"
                >
                    <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
                        <path d="m16 28c7-4.733 14-10 14-17 0-1.792-.683-3.583-2.05-4.95-1.367-1.366-3.158-2.05-4.95-2.05-1.791 0-3.583.684-4.949 2.05l-2.051 2.051-2.05-2.051c-1.367-1.366-3.158-2.05-4.95-2.05-1.791 0-3.583.684-4.949 2.05-1.367 1.367-2.051 3.158-2.051 4.95 0 7 7 12.267 14 17z"></path>
                    </svg>
                </button>
            </div>
            
            <div className="place-card-content">
                <div className="place-card-header">
                    <h3 className="place-name" title={place.place_name}>
                        {truncateText(place.place_name, 35)}
                    </h3>
                    <div className="place-rating">
                        <span className="star">★</span>
                        <span className="rating-val">{formatRating(place.rating)}</span>
                    </div>
                </div>
                
                <p className="place-location">
                    {place.city_name}, {place.state_name}
                </p>
                
                <p className="place-category">
                    {place.category_name}
                </p>
                
                <div className="place-card-footer">
                    <div className="place-price">
                        {place.entry_fee_indian && Number(place.entry_fee_indian) > 0 ? (
                            <div className="price-tag">
                                <span className="price-val">{formatCurrency(place.entry_fee_indian)}</span>
                                <span className="price-label"> per adult</span>
                            </div>
                        ) : (
                            <span className="price-free">Free Entry</span>
                        )}
                    </div>
                    {/* <button className="btn btn-sm btn-outline">Book</button> */}
                </div>
            </div>
        </Link>
    );
};

export default PlaceCard;
