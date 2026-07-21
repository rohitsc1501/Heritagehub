import React, { useEffect, useRef, useState } from 'react';
import './ScrollReveal.css';

const ScrollReveal = ({ children, delay = 0, direction = 'up', distance = '30px', duration = '0.8s', threshold = 0.1, className = '' }) => {
    const [isVisible, setIsVisible] = useState(false);
    const ref = useRef(null);

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsVisible(true);
                    observer.unobserve(entry.target);
                }
            },
            {
                root: null,
                rootMargin: '0px',
                threshold: threshold,
            }
        );

        if (ref.current) {
            observer.observe(ref.current);
        }

        return () => {
            if (ref.current) {
                observer.unobserve(ref.current);
            }
        };
    }, [threshold]);

    const getTransform = () => {
        switch (direction) {
            case 'up': return `translateY(${distance})`;
            case 'down': return `translateY(-${distance})`;
            case 'left': return `translateX(${distance})`;
            case 'right': return `translateX(-${distance})`;
            default: return `translateY(${distance})`;
        }
    };

    const style = {
        opacity: isVisible ? 1 : 0,
        transform: isVisible ? 'translate(0)' : getTransform(),
        transition: `all ${duration} cubic-bezier(0.16, 1, 0.3, 1) ${delay}s`,
    };

    return (
        <div ref={ref} style={style} className={`scroll-reveal ${className}`}>
            {children}
        </div>
    );
};

export default ScrollReveal;
