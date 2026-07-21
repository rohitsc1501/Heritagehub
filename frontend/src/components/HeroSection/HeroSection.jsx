import React, { useState, useEffect } from 'react';
import SearchBar from '../SearchBar/SearchBar';
import './HeroSection.css';

const HERO_IMAGES = [
    'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=1920&q=80', // Taj Mahal
    'https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?w=1920&q=80', // Hawa Mahal
    'https://images.unsplash.com/photo-1548013146-72479768bada?w=1920&q=80', // India Gate
    'https://images.unsplash.com/photo-1514222026131-7b003a7442eb?w=1920&q=80', // Kerala
];

const HeroSection = () => {
    const [currentImgIndex, setCurrentImgIndex] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentImgIndex((prev) => (prev + 1) % HERO_IMAGES.length);
        }, 5000); // Change image every 5 seconds
        return () => clearInterval(interval);
    }, []);

    return (
        <section className="hero-section">
            {/* Background Images */}
            {HERO_IMAGES.map((img, index) => (
                <div 
                    key={index}
                    className={`hero-bg ${index === currentImgIndex ? 'active' : ''}`}
                    style={{ backgroundImage: `url(${img})` }}
                ></div>
            ))}
            
            <div className="hero-overlay"></div>

            <div className="hero-content container">
                <div className="hero-text-area">
                    <h1 className="hero-title animate-fadeInUp stagger-1">
                        Discover India's <br/>
                        <span className="text-highlight">Timeless Heritage</span>
                    </h1>
                    <p className="hero-subtitle animate-fadeInUp stagger-2">
                        Explore magnificent monuments, ancient temples, and breathtaking landscapes.
                        Book your tickets and start your journey through history.
                    </p>
                </div>

                <div className="hero-search-area animate-fadeInUp stagger-3">
                    <SearchBar />
                </div>
            </div>
        </section>
    );
};

export default HeroSection;
