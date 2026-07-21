import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Link, useLocation } from 'react-router-dom';
import L from 'leaflet';
import api from '../../services/api';
import './Map.css';

// Fix for default marker icons in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const PlacesMap = () => {
    const [places, setPlaces] = useState([]);
    const [loading, setLoading] = useState(true);
    const mapRef = useRef(null);
    const [isFullscreen, setIsFullscreen] = useState(false);
    const location = useLocation();

    useEffect(() => {
        const handleFullscreenChange = () => {
            setIsFullscreen(!!document.fullscreenElement);
        };
        document.addEventListener('fullscreenchange', handleFullscreenChange);
        return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
    }, []);

    const toggleFullscreen = () => {
        if (!document.fullscreenElement) {
            if (mapRef.current?.requestFullscreen) {
                mapRef.current.requestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    };

    useEffect(() => {
        const fetchPlaces = async () => {
            try {
                const response = await api.get('/places/map_data/');
                const results = response.data.results || response.data;
                // Coordinates already filtered by backend, but we'll leave the check
                const validPlaces = results.filter(p => p.latitude && p.longitude);
                setPlaces(validPlaces);
            } catch (err) {
                console.error("Failed to load places for map:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchPlaces();
    }, []);

    // Center roughly on India or focus on selected place
    const focusCoords = location.state?.focusCoords;
    const initialCenter = focusCoords || [22.9734, 78.6569];
    const initialZoom = focusCoords ? 14 : 5;

    if (loading) {
        return (
            <div className="map-page-container loading-container">
                <div className="map-loader">Loading Map...</div>
            </div>
        );
    }

    return (
        <div className={`map-page-container ${isFullscreen ? 'is-fullscreen' : ''}`} ref={mapRef}>
            <button className="fullscreen-btn" onClick={toggleFullscreen} title="Toggle Fullscreen">
                {isFullscreen ? '↙️ Exit Fullscreen' : '↗️ Fullscreen'}
            </button>
            <MapContainer center={initialCenter} zoom={initialZoom} scrollWheelZoom={true} className="full-screen-map">
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                    url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
                />
                {places.map((place) => (
                    <Marker 
                        key={place.id} 
                        position={[parseFloat(place.latitude), parseFloat(place.longitude)]}
                    >
                        <Popup className="custom-popup">
                            <div className="popup-content">
                                <img src={place.main_image_url} alt={place.place_name} className="popup-image" />
                                <h4>{place.place_name}</h4>
                                <p>{place.city_name}, {place.state_name}</p>
                                <Link to={`/place/${place.slug}`} className="btn btn-primary btn-sm popup-link">View Details</Link>
                            </div>
                        </Popup>
                    </Marker>
                ))}
            </MapContainer>
        </div>
    );
};

export default PlacesMap;
