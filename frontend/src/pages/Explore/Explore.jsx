import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import SearchBar from '../../components/SearchBar/SearchBar';
import PlaceCard from '../../components/PlaceCard/PlaceCard';
import { SkeletonCard, Spinner } from '../../components/Loader/Loader';
import { placeService } from '../../services/placeService';
import './Explore.css';

const Explore = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [places, setPlaces] = useState([]);
    const [loading, setLoading] = useState(true);
    const [loadingMore, setLoadingMore] = useState(false);
    const [nextUrl, setNextUrl] = useState(null);
    const [totalCount, setTotalCount] = useState(0);

    // Filter states
    const [categories, setCategories] = useState([]);
    const [filters, setFilters] = useState({
        search: searchParams.get('search') || '',
        state: searchParams.get('state') || '',
        category: searchParams.get('category_slug') || '',
        unesco: searchParams.get('unesco') || '',
        rating: searchParams.get('rating') || '',
        ordering: searchParams.get('ordering') || '-rating',
    });
    
    const [showFilters, setShowFilters] = useState(false);

    useEffect(() => {
        // Fetch categories for filter dropdown
        const fetchCategories = async () => {
            try {
                const data = await placeService.getCategories();
                setCategories(data.results || data);
            } catch (err) {
                console.error("Error fetching categories", err);
            }
        };
        fetchCategories();
    }, []);

    useEffect(() => {
        // Update local state when URL params change
        setFilters({
            search: searchParams.get('search') || '',
            state: searchParams.get('state') || '',
            category: searchParams.get('category_slug') || '',
            unesco: searchParams.get('unesco') || '',
            rating: searchParams.get('rating') || '',
            ordering: searchParams.get('ordering') || '-rating',
        });
    }, [searchParams]);

    useEffect(() => {
        const fetchPlaces = async () => {
            try {
                setLoading(true);
                const params = {};
                if (filters.search) params.search = filters.search;
                if (filters.state) params.state = filters.state;
                if (filters.category) params.category_slug = filters.category;
                if (filters.unesco) params.unesco = filters.unesco;
                if (filters.rating) params.min_rating = filters.rating;
                if (filters.ordering) params.ordering = filters.ordering;

                const data = await placeService.getPlaces(params);
                setPlaces(data.results);
                setTotalCount(data.count);
                setNextUrl(data.next);
            } catch (error) {
                console.error("Error fetching places", error);
            } finally {
                setLoading(false);
            }
        };

        fetchPlaces();
    }, [filters]);

    const handleSearch = ({ query, location }) => {
        const newParams = new URLSearchParams(searchParams);
        if (query) newParams.set('search', query);
        else newParams.delete('search');
        
        if (location) newParams.set('state', location);
        else newParams.delete('state');
        
        setSearchParams(newParams);
    };

    const handleFilterChange = (key, value) => {
        const newParams = new URLSearchParams(searchParams);
        if (value) {
            newParams.set(key, value);
        } else {
            newParams.delete(key);
        }
        setSearchParams(newParams);
    };

    const handleLoadMore = async () => {
        if (!nextUrl || loadingMore) return;
        
        try {
            setLoadingMore(true);
            // Extract query string from nextUrl
            const urlObj = new URL(nextUrl);
            const queryParams = Object.fromEntries(urlObj.searchParams);
            
            const data = await placeService.getPlaces(queryParams);
            setPlaces([...places, ...data.results]);
            setNextUrl(data.next);
        } catch (error) {
            console.error("Error loading more", error);
        } finally {
            setLoadingMore(false);
        }
    };

    return (
        <div className="explore-page page-active">
            <div className="explore-header bg-secondary">
                <div className="container">
                    <h1 className="section-title">Explore Destinations</h1>
                    <p className="section-subtitle">Discover incredible places across India</p>
                    
                    <div className="explore-search">
                        <SearchBar onSearch={handleSearch} embedded={true} />
                    </div>
                </div>
            </div>

            <div className="container explore-content">
                {/* Mobile Filter Toggle */}
                <div className="mobile-filter-toggle hide-desktop">
                    <button 
                        className="btn btn-outline" 
                        onClick={() => setShowFilters(!showFilters)}
                    >
                        {showFilters ? 'Hide Filters' : 'Show Filters'}
                    </button>
                    <div className="results-count">
                        {totalCount} places found
                    </div>
                </div>

                <div className="explore-layout">
                    {/* Filters Sidebar */}
                    <aside className={`explore-sidebar ${showFilters ? 'show' : ''}`}>
                        <div className="filter-group">
                            <h3 className="filter-title">Sort By</h3>
                            <select 
                                className="filter-select"
                                value={filters.ordering}
                                onChange={(e) => handleFilterChange('ordering', e.target.value)}
                            >
                                <option value="-rating">Highest Rated</option>
                                <option value="-number_of_reviews">Most Popular</option>
                                <option value="entry_fee_indian">Lowest Price</option>
                            </select>
                        </div>

                        <div className="filter-group">
                            <h3 className="filter-title">Category</h3>
                            <div className="filter-options">
                                <label className="filter-radio">
                                    <input 
                                        type="radio" 
                                        name="category" 
                                        checked={!filters.category}
                                        onChange={() => handleFilterChange('category_slug', '')} 
                                    />
                                    <span>All Categories</span>
                                </label>
                                {categories.map(cat => (
                                    <label key={cat.id} className="filter-radio">
                                        <input 
                                            type="radio" 
                                            name="category" 
                                            checked={filters.category === cat.slug}
                                            onChange={() => handleFilterChange('category_slug', cat.slug)} 
                                        />
                                        <span>{cat.name}</span>
                                    </label>
                                ))}
                            </div>
                        </div>

                        <div className="filter-group">
                            <h3 className="filter-title">Special Tags</h3>
                            <div className="filter-options">
                                <label className="filter-checkbox">
                                    <input 
                                        type="checkbox" 
                                        checked={filters.unesco === 'Yes'}
                                        onChange={(e) => handleFilterChange('unesco', e.target.checked ? 'Yes' : '')} 
                                    />
                                    <span>UNESCO World Heritage</span>
                                </label>
                            </div>
                        </div>
                        
                        <div className="filter-group">
                            <h3 className="filter-title">Minimum Rating</h3>
                            <div className="filter-options">
                                {[4.5, 4.0, 3.5, 3.0].map(rating => (
                                    <label key={rating} className="filter-radio">
                                        <input 
                                            type="radio" 
                                            name="rating" 
                                            checked={filters.rating === String(rating)}
                                            onChange={() => handleFilterChange('rating', String(rating))} 
                                        />
                                        <span>{rating}+ Stars</span>
                                    </label>
                                ))}
                                <label className="filter-radio">
                                    <input 
                                        type="radio" 
                                        name="rating" 
                                        checked={!filters.rating}
                                        onChange={() => handleFilterChange('rating', '')} 
                                    />
                                    <span>Any Rating</span>
                                </label>
                            </div>
                        </div>
                    </aside>

                    {/* Results Grid */}
                    <div className="explore-results">
                        <div className="results-header hide-mobile">
                            <h2>Results</h2>
                            <span className="results-count">{totalCount} places found</span>
                        </div>

                        {loading ? (
                            <div className="places-grid">
                                {Array(6).fill(0).map((_, i) => <SkeletonCard key={i} />)}
                            </div>
                        ) : places.length > 0 ? (
                            <>
                                <div className="places-grid">
                                    {places.map(place => (
                                        <PlaceCard key={place.id} place={place} />
                                    ))}
                                </div>
                                
                                {nextUrl && (
                                    <div className="load-more-container">
                                        <button 
                                            className="btn btn-outline btn-lg" 
                                            onClick={handleLoadMore}
                                            disabled={loadingMore}
                                        >
                                            {loadingMore ? <><Spinner /> Loading...</> : 'Load More Places'}
                                        </button>
                                    </div>
                                )}
                            </>
                        ) : (
                            <div className="empty-state">
                                <div className="empty-icon">🏜️</div>
                                <h3>No places found</h3>
                                <p>We couldn't find any places matching your criteria. Try adjusting your filters.</p>
                                <button 
                                    className="btn btn-primary mt-4"
                                    onClick={() => setSearchParams(new URLSearchParams())}
                                >
                                    Clear All Filters
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Explore;
