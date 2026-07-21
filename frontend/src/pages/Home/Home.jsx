import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import HeroSection from '../../components/HeroSection/HeroSection';
import CategoryCard from '../../components/CategoryCard/CategoryCard';
import PlaceCard from '../../components/PlaceCard/PlaceCard';
import { SkeletonCard } from '../../components/Loader/Loader';
import ScrollReveal from '../../components/ScrollReveal/ScrollReveal';
import { placeService } from '../../services/placeService';
import './Home.css';

const Home = () => {
    const [categories, setCategories] = useState([]);
    const [trendingPlaces, setTrendingPlaces] = useState([]);
    const [unescoPlaces, setUnescoPlaces] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchHomeData = async () => {
            try {
                setLoading(true);
                const [catsRes, trendingRes, unescoRes] = await Promise.all([
                    placeService.getCategories(),
                    placeService.getTrendingPlaces(),
                    placeService.getUnescoPlaces()
                ]);
                
                setCategories(catsRes.results || catsRes);
                setTrendingPlaces(trendingRes.results || trendingRes);
                setUnescoPlaces(unescoRes.results || unescoRes);
            } catch (error) {
                console.error("Error fetching homepage data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchHomeData();
    }, []);

    const renderSkeletons = (count = 4) => {
        return Array(count).fill(0).map((_, i) => <SkeletonCard key={i} />);
    };

    return (
        <div className="home-page page-active">
            <HeroSection />

            {/* Categories Section */}
            <section className="section bg-secondary">
                <div className="container">
                    <ScrollReveal>
                        <div className="section-header">
                            <div>
                                <h2 className="section-title">Explore by Category</h2>
                                <p className="section-subtitle">Find exactly what you're looking for</p>
                            </div>
                        </div>
                    </ScrollReveal>
                    
                    <div className="categories-grid">
                        {loading 
                            ? Array(6).fill(0).map((_, i) => <div key={i} className="skeleton" style={{height: '140px', borderRadius: 'var(--radius-xl)'}}></div>)
                            : categories.slice(0, 12).map((cat, index) => (
                                <ScrollReveal key={cat.id} delay={index * 0.05} direction="up" distance="20px">
                                    <CategoryCard category={cat} />
                                </ScrollReveal>
                            ))
                        }
                    </div>
                </div>
            </section>

            {/* Trending Places Section */}
            <section className="section">
                <div className="container">
                    <ScrollReveal>
                        <div className="section-header">
                            <div>
                                <h2 className="section-title">Trending Destinations</h2>
                                <p className="section-subtitle">Most popular heritage sites this week</p>
                            </div>
                            <Link to="/explore" className="btn btn-outline hide-mobile">View All</Link>
                        </div>
                    </ScrollReveal>

                    <div className="places-grid">
                        {loading 
                            ? renderSkeletons(4)
                            : trendingPlaces.slice(0, 4).map((place, index) => (
                                <ScrollReveal key={place.id} delay={index * 0.1} direction="up" distance="30px">
                                    <PlaceCard place={place} />
                                </ScrollReveal>
                            ))
                        }
                    </div>
                    <div className="mobile-action show-mobile">
                        <Link to="/explore" className="btn btn-outline w-full">View All</Link>
                    </div>
                </div>
            </section>

            {/* UNESCO Section */}
            <section className="section bg-tertiary">
                <div className="container">
                    <ScrollReveal>
                        <div className="section-header">
                            <div>
                                <h2 className="section-title">UNESCO World Heritage</h2>
                                <p className="section-subtitle">Globally recognized wonders of India</p>
                            </div>
                            <Link to="/explore?unesco=Yes" className="btn btn-outline hide-mobile">Explore All</Link>
                        </div>
                    </ScrollReveal>

                    <div className="places-grid">
                        {loading 
                            ? renderSkeletons(4)
                            : unescoPlaces.slice(0, 4).map((place, index) => (
                                <ScrollReveal key={place.id} delay={index * 0.1} direction="up" distance="30px">
                                    <PlaceCard place={place} />
                                </ScrollReveal>
                            ))
                        }
                    </div>
                    <div className="mobile-action show-mobile">
                        <Link to="/explore?unesco=Yes" className="btn btn-outline w-full">Explore All</Link>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Home;
