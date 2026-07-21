import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { placeService } from '../../services/placeService';
import { useDebounce } from '../../hooks/useDebounce';
import { INDIAN_STATES } from '../../utils/constants';
import './SearchBar.css';

const SearchBar = ({ onSearch, embedded = false }) => {
    const navigate = useNavigate();
    const [query, setQuery] = useState('');
    const [location, setLocation] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    
    const debouncedQuery = useDebounce(query, 300);
    const wrapperRef = useRef(null);

    useEffect(() => {
        const fetchSuggestions = async () => {
            if (debouncedQuery.length >= 2) {
                try {
                    const data = await placeService.getSearchSuggestions(debouncedQuery);
                    setSuggestions(data);
                    setShowSuggestions(true);
                } catch (error) {
                    console.error("Error fetching suggestions", error);
                }
            } else {
                setSuggestions([]);
                setShowSuggestions(false);
            }
        };

        fetchSuggestions();
    }, [debouncedQuery]);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
                setShowSuggestions(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        
        if (onSearch) {
            onSearch({ query, location });
            return;
        }

        const searchParams = new URLSearchParams();
        if (query) searchParams.set('search', query);
        if (location) searchParams.set('state', location);
        
        navigate(`/explore?${searchParams.toString()}`);
        setShowSuggestions(false);
    };

    const handleSuggestionClick = (slug) => {
        navigate(`/place/${slug}`);
        setShowSuggestions(false);
        setQuery('');
    };

    return (
        <div className={`search-wrapper ${embedded ? 'embedded' : ''}`} ref={wrapperRef}>
            <form className="search-bar glass" onSubmit={handleSubmit}>
                <div className="search-input-group">
                    <label>Where</label>
                    <input 
                        type="text" 
                        placeholder="Search places, categories..." 
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onFocus={() => {if(suggestions.length > 0) setShowSuggestions(true)}}
                        autoComplete="off"
                    />
                </div>
                
                <div className="search-divider"></div>
                
                <div className="search-input-group location-group">
                    <label>Location</label>
                    <select 
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                    >
                        <option value="">All of India</option>
                        {INDIAN_STATES.map(state => (
                            <option key={state} value={state}>{state}</option>
                        ))}
                    </select>
                </div>
                
                <button type="submit" className="search-btn btn-primary btn-icon">
                    🔍
                </button>
            </form>

            {showSuggestions && suggestions.length > 0 && (
                <div className="search-suggestions glass">
                    {suggestions.map((item) => (
                        <div 
                            key={item.id} 
                            className="suggestion-item"
                            onClick={() => handleSuggestionClick(item.slug)}
                        >
                            <div className="suggestion-icon">📍</div>
                            <div className="suggestion-content">
                                <div className="suggestion-title">{item.place_name}</div>
                                <div className="suggestion-subtitle">
                                    {item.category__name} • {item.city__city_name}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SearchBar;
