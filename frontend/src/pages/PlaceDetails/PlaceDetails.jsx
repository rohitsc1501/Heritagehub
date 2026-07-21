import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { placeService } from '../../services/placeService';
import { useAuth } from '../../context/AuthContext';
import { formatCurrency, formatRating } from '../../utils/formatters';
import { PageLoader } from '../../components/Loader/Loader';
import api from '../../services/api';
import './PlaceDetails.css';

const PlaceDetails = () => {
    const { slug } = useParams();
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();
    
    const [place, setPlace] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeImage, setActiveImage] = useState(0);
    const [isWishlisted, setIsWishlisted] = useState(false);

    // Booking modal state
    const [showBookingModal, setShowBookingModal] = useState(false);
    const [bookingData, setBookingData] = useState({
        visit_date: '',
        adults: 1,
    });
    const [bookingLoading, setBookingLoading] = useState(false);
    const [bookingError, setBookingError] = useState('');

    useEffect(() => {
        const fetchPlaceDetails = async () => {
            try {
                setLoading(true);
                const data = await placeService.getPlace(slug);
                setPlace(data);
                setIsWishlisted(data.is_wishlisted);
            } catch (err) {
                setError("Failed to load place details. It may not exist.");
            } finally {
                setLoading(false);
            }
        };

        fetchPlaceDetails();
        window.scrollTo(0, 0);
    }, [slug]);

    const handleWishlistToggle = async () => {
        if (!isAuthenticated) {
            navigate('/login', { state: { from: { pathname: `/place/${slug}` } } });
            return;
        }

        try {
            const res = await api.post('/wishlist/toggle/', { place_id: place.id });
            setIsWishlisted(res.data.is_wishlisted);
        } catch (error) {
            console.error('Wishlist error', error);
        }
    };

    const handleBookNow = () => {
        if (!isAuthenticated) {
            navigate('/login', { state: { from: { pathname: `/place/${slug}` } } });
            return;
        }
        setShowBookingModal(true);
    };

    const handleBookingSubmit = async (e) => {
        e.preventDefault();
        
        if (!bookingData.visit_date) {
            setBookingError("Please select a visit date.");
            return;
        }

        try {
            setBookingLoading(true);
            setBookingError('');
            
            await api.post('/bookings/', {
                place: place.id,
                visit_date: bookingData.visit_date,
                adults: bookingData.adults,
                children: 0,
                senior_citizens: 0,
                students: 0
            });
            
            setShowBookingModal(false);
            navigate('/profile');
        } catch (err) {
            setBookingError(err.response?.data?.detail || "Failed to create booking.");
        } finally {
            setBookingLoading(false);
        }
    };

    if (loading) return <PageLoader />;
    
    if (error || !place) return (
        <div className="container section empty-state">
            <h2>Oops!</h2>
            <p>{error || "Place not found"}</p>
            <button className="btn btn-primary mt-4" onClick={() => navigate('/explore')}>Back to Explore</button>
        </div>
    );

    // Collect all images including main image and gallery images
    const allImages = [
        { id: 'main', image_url: place.main_image_url || 'https://images.unsplash.com/photo-1548013146-72479768bada?w=1200&q=80' },
        ...(place.images || [])
    ];

    return (
        <div className="place-details-page page-active">
            {/* Header Section */}
            <div className="container pd-header-section">
                <div className="pd-title-row">
                    <div>
                        <h1 className="pd-title">{place.place_name}</h1>
                        <div className="pd-subtitle">
                            <span className="pd-rating">
                                <span className="star">★</span> {formatRating(place.rating)} 
                                <span className="text-muted"> ({place.number_of_reviews} reviews)</span>
                            </span>
                            <span className="pd-dot">•</span>
                            <span className="pd-location">{place.city_name}, {place.state_name}</span>
                            <span className="pd-dot">•</span>
                            <span className="pd-category">{place.category_name}</span>
                        </div>
                    </div>
                    
                    <div className="pd-actions">
                        {place.latitude && place.longitude && (
                            <button className="btn btn-ghost" onClick={() => navigate('/map', { state: { focusCoords: [place.latitude, place.longitude] } })}>
                                <span className="icon">📍</span> See on Map
                            </button>
                        )}
                        <button className="btn btn-ghost">
                            <span className="icon">📤</span> Share
                        </button>
                        <button 
                            className={`btn ${isWishlisted ? 'btn-accent' : 'btn-ghost'}`} 
                            onClick={handleWishlistToggle}
                        >
                            <span className="icon">{isWishlisted ? '❤️' : '🤍'}</span> 
                            {isWishlisted ? 'Saved' : 'Save'}
                        </button>
                    </div>
                </div>

                {/* Image Gallery */}
                <div className="pd-gallery">
                    <div className="pd-main-image">
                        <img src={allImages[activeImage].image_url} alt={place.place_name} />
                        <div className="pd-badges">
                            {place.unesco_status === 'Yes' && <span className="badge badge-unesco">UNESCO World Heritage</span>}
                            {place.asi_protected === 'Yes' && <span className="badge badge-asi">ASI Protected</span>}
                        </div>
                    </div>
                    {allImages.length > 1 && (
                        <div className="pd-thumbnail-list">
                            {allImages.slice(0, 5).map((img, idx) => (
                                <div 
                                    key={img.id || idx} 
                                    className={`pd-thumbnail ${activeImage === idx ? 'active' : ''}`}
                                    onClick={() => setActiveImage(idx)}
                                >
                                    <img src={img.image_url} alt="Thumbnail" />
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Content Section */}
            <div className="container pd-content-section">
                <div className="pd-main-content">
                    
                    <section className="pd-section">
                        <h2>About this place</h2>
                        <p className="pd-description">{place.description}</p>
                        {place.history && (
                            <>
                                <h3>History</h3>
                                <p className="pd-description">{place.history}</p>
                            </>
                        )}
                        
                        {place.year_established && (
                            <p className="pd-meta"><strong>Established:</strong> {place.year_established}</p>
                        )}
                    </section>

                    <div className="pd-divider"></div>

                    <section className="pd-section">
                        <h2>Visitor Information</h2>
                        <div className="pd-info-grid">
                            <div className="pd-info-item">
                                <div className="info-icon">🕒</div>
                                <div>
                                    <h4>Timings</h4>
                                    <p>{place.opening_time ? place.opening_time.substring(0, 5) : '09:00'} to {place.closing_time ? place.closing_time.substring(0, 5) : '18:00'}</p>
                                    <p className="text-muted text-sm">Open on: {place.opening_days || 'All days'}</p>
                                </div>
                            </div>
                            
                            <div className="pd-info-item">
                                <div className="info-icon">⏳</div>
                                <div>
                                    <h4>Duration</h4>
                                    <p>{place.average_visit_duration || '2-3 hours'} recommended</p>
                                </div>
                            </div>

                            <div className="pd-info-item">
                                <div className="info-icon">🌤️</div>
                                <div>
                                    <h4>Best Time to Visit</h4>
                                    <p>{place.best_time_to_visit || 'October to March'}</p>
                                </div>
                            </div>
                        </div>
                    </section>

                    <div className="pd-divider"></div>

                    <section className="pd-section">
                        <h2>Amenities & Access</h2>
                        <ul className="pd-amenities-list">
                            {place.parking_available === 'Yes' && <li><span className="icon">🅿️</span> Parking Available</li>}
                            {place.wheelchair_accessible === 'Yes' && <li><span className="icon">♿</span> Wheelchair Accessible</li>}
                            {place.guided_tours === 'Yes' && <li><span className="icon">🗣️</span> Guided Tours</li>}
                            {place.audio_guide === 'Yes' && <li><span className="icon">🎧</span> Audio Guide</li>}
                            {place.photography_allowed === 'Yes' && <li><span className="icon">📷</span> Photography Allowed</li>}
                        </ul>
                    </section>
                </div>

                {/* Sidebar Booking Card */}
                <div className="pd-sidebar">
                    <div className="booking-card glass">
                        <div className="booking-price">
                            {place.entry_fee_indian && Number(place.entry_fee_indian) > 0 ? (
                                <>
                                    <span className="price-amount">{formatCurrency(place.entry_fee_indian)}</span>
                                    <span className="price-label">/ adult</span>
                                </>
                            ) : (
                                <span className="price-amount text-success">Free Entry</span>
                            )}
                        </div>

                        <div className="booking-info">
                            <p>Foreigner Fee: {place.entry_fee_foreigner ? formatCurrency(place.entry_fee_foreigner) : 'Same as Indian'}</p>
                        </div>

                        <div className="booking-buttons" style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                            {place.booking_url && (
                                <a 
                                    href={place.booking_url} 
                                    target="_blank" 
                                    rel="noreferrer" 
                                    className="btn btn-primary"
                                    style={{ flex: 1 }}
                                >
                                    Book on Official Site
                                </a>
                            )}
                            <button className="btn btn-outline" style={{ flex: 1 }} onClick={handleBookNow}>
                                Book via Monumenta
                            </button>
                        </div>
                        
                        <p className="booking-note">You won't be charged yet</p>
                    </div>
                </div>
            </div>

            {/* Booking Modal */}
            {showBookingModal && (
                <div className="modal-backdrop" onClick={() => setShowBookingModal(false)}>
                    <div className="modal-content card" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2>Book Tickets</h2>
                            <button className="close-btn" onClick={() => setShowBookingModal(false)}>×</button>
                        </div>
                        <div className="modal-body">
                            <h3 className="modal-subtitle">{place.place_name}</h3>
                            
                            {bookingError && <div className="auth-alert error">{bookingError}</div>}
                            
                            <form onSubmit={handleBookingSubmit}>
                                <div className="input-group mb-3">
                                    <label>Visit Date</label>
                                    <input 
                                        type="date" 
                                        className="input-field"
                                        value={bookingData.visit_date}
                                        onChange={e => setBookingData({...bookingData, visit_date: e.target.value})}
                                        min={new Date().toISOString().split('T')[0]}
                                        required
                                    />
                                </div>
                                
                                <div className="input-group mb-4">
                                    <label>Number of Adults</label>
                                    <input 
                                        type="number" 
                                        className="input-field"
                                        min="1" 
                                        max="10"
                                        value={bookingData.adults}
                                        onChange={e => setBookingData({...bookingData, adults: parseInt(e.target.value) || 1})}
                                        required
                                    />
                                </div>

                                <div className="booking-summary">
                                    <div className="summary-row">
                                        <span>{formatCurrency(place.entry_fee_indian || 0)} x {bookingData.adults} adults</span>
                                        <span>{formatCurrency((place.entry_fee_indian || 0) * bookingData.adults)}</span>
                                    </div>
                                    <div className="summary-row total">
                                        <span>Total (INR)</span>
                                        <span>{formatCurrency((place.entry_fee_indian || 0) * bookingData.adults)}</span>
                                    </div>
                                </div>

                                <button 
                                    type="submit" 
                                    className="btn btn-primary btn-full mt-4"
                                    disabled={bookingLoading}
                                >
                                    {bookingLoading ? 'Processing...' : 'Confirm Booking'}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PlaceDetails;
