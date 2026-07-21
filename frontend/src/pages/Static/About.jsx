import React from 'react';
import './Pages.css';

const About = () => {
    return (
        <div className="page-active">
            <div className="container section">
                <div className="page-header text-center">
                    <h1 className="section-title">About HeritageHub</h1>
                    <p className="section-subtitle">Discover the story behind our mission to preserve and promote cultural heritage.</p>
                </div>

                <div className="about-content">
                    <div className="about-image card">
                        <img src="https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800&q=80" alt="India Heritage" />
                    </div>
                    
                    <div className="about-text">
                        <h2>Our Mission</h2>
                        <p>
                            HeritageHub was founded with a singular vision: to make the rich, diverse cultural heritage of India accessible to everyone. We believe that by connecting people with historical monuments, UNESCO sites, and cultural landmarks, we can foster a deeper appreciation for our shared history.
                        </p>
                        
                        <h2 className="mt-md">What We Do</h2>
                        <p>
                            We provide a seamless, integrated platform for discovering heritage sites, learning about their history, and booking entry tickets directly. By digitizing access to these monuments, we aim to support conservation efforts and promote sustainable tourism.
                        </p>

                        <div className="stats-row mt-lg">
                            <div className="stat-item">
                                <span className="stat-num">500+</span>
                                <span className="stat-desc">Heritage Sites</span>
                            </div>
                            <div className="stat-item">
                                <span className="stat-num">1M+</span>
                                <span className="stat-desc">Happy Visitors</span>
                            </div>
                            <div className="stat-item">
                                <span className="stat-num">28</span>
                                <span className="stat-desc">States Covered</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default About;
