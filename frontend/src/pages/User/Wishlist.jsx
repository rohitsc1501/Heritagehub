import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { userService } from '../../services/userService';
import PlaceCard from '../../components/PlaceCard/PlaceCard';
import { PageLoader } from '../../components/Loader/Loader';
import './User.css';

const Wishlist = () => {
    const [wishlistItems, setWishlistItems] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchWishlist = async () => {
            try {
                setLoading(true);
                const data = await userService.getWishlist();
                setWishlistItems(data);
            } catch (error) {
                console.error("Error fetching wishlist", error);
            } finally {
                setLoading(false);
            }
        };

        fetchWishlist();
    }, []);

    const clearWishlist = async () => {
        if (window.confirm("Are you sure you want to clear your wishlist?")) {
            try {
                await userService.clearWishlist();
                setWishlistItems([]);
            } catch (error) {
                console.error("Error clearing wishlist", error);
            }
        }
    };

    if (loading) return <PageLoader />;

    return (
        <div className="container section page-active">
            <div className="section-header">
                <h1 className="section-title">My Wishlist</h1>
                {wishlistItems.length > 0 && (
                    <button className="btn btn-outline text-error" onClick={clearWishlist}>
                        Clear Wishlist
                    </button>
                )}
            </div>

            {wishlistItems.length === 0 ? (
                <div className="empty-state card">
                    <div className="empty-icon">❤️</div>
                    <h3>Your wishlist is empty</h3>
                    <p>Save places you want to visit later.</p>
                    <Link to="/explore" className="btn btn-primary mt-md">Explore Places</Link>
                </div>
            ) : (
                <div className="places-grid">
                    {wishlistItems.map(item => (
                        <div key={item.id} className="wishlist-item-wrapper">
                            <PlaceCard place={item.place} />
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Wishlist;
