-- =====================================================================
-- HeritageHub - Cultural Heritage Explorer & Ticket Booking Platform
-- MySQL Schema (3NF normalized)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS heritagehub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE heritagehub;

-- ---------------------------------------------------------------------
-- Reference tables
-- ---------------------------------------------------------------------
CREATE TABLE states (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    type ENUM('State','Union Territory') NOT NULL
) ENGINE=InnoDB;

CREATE TABLE districts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    state_id INT NOT NULL,
    district_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (state_id) REFERENCES states(id) ON DELETE CASCADE,
    UNIQUE KEY uq_state_district (state_id, district_name)
) ENGINE=InnoDB;

CREATE TABLE cities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    district_id INT NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (district_id) REFERENCES districts(id) ON DELETE CASCADE,
    UNIQUE KEY uq_district_city (district_id, city_name)
) ENGINE=InnoDB;

CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Core places table
-- ---------------------------------------------------------------------
CREATE TABLE places (
    id INT PRIMARY KEY AUTO_INCREMENT,
    city_id INT NOT NULL,
    category_id INT NOT NULL,
    subcategory VARCHAR(150),
    place_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    history TEXT,
    year_established VARCHAR(100),
    unesco_status ENUM('Yes','No') DEFAULT 'No',
    asi_protected ENUM('Yes','No') DEFAULT 'No',
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    altitude_m DECIMAL(7,2) NULL,
    address VARCHAR(500),
    pincode VARCHAR(10) NULL,
    opening_days VARCHAR(255),
    opening_time TIME,
    closing_time TIME,
    entry_fee_indian DECIMAL(8,2),
    entry_fee_foreigner DECIMAL(8,2),
    student_discount VARCHAR(100),
    senior_citizen_discount VARCHAR(100),
    parking_available VARCHAR(20),
    wheelchair_accessible VARCHAR(50),
    guided_tours VARCHAR(50),
    audio_guide VARCHAR(100),
    photography_allowed VARCHAR(20),
    videography_allowed VARCHAR(100),
    best_time_to_visit VARCHAR(100),
    average_visit_duration VARCHAR(50),
    nearest_airport VARCHAR(150) NULL,
    nearest_railway_station VARCHAR(150) NULL,
    nearest_bus_station VARCHAR(150) NULL,
    official_website VARCHAR(255) NULL,
    contact_number VARCHAR(50) NULL,
    email VARCHAR(150) NULL,
    rating DECIMAL(2,1),
    number_of_reviews INT DEFAULT 0,
    main_image_url VARCHAR(500) NULL,
    status ENUM('Active','Inactive','Under Renovation') DEFAULT 'Active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
    INDEX idx_places_category (category_id),
    INDEX idx_places_city (city_id),
    INDEX idx_places_unesco (unesco_status),
    INDEX idx_places_rating (rating),
    FULLTEXT INDEX ft_places_search (place_name, description)
) ENGINE=InnoDB;

CREATE TABLE place_images (
    id INT PRIMARY KEY AUTO_INCREMENT,
    place_id INT NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    sort_order INT DEFAULT 0,
    image_type VARCHAR(30) DEFAULT 'Gallery',
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    INDEX idx_placeimages_place (place_id)
) ENGINE=InnoDB;

CREATE TABLE ticket_prices (
    id INT PRIMARY KEY AUTO_INCREMENT,
    place_id INT NOT NULL,
    visitor_type VARCHAR(50) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    currency CHAR(3) DEFAULT 'INR',
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    INDEX idx_tickets_place (place_id)
) ENGINE=InnoDB;

CREATE TABLE events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    place_id INT NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    event_schedule VARCHAR(255),
    notes VARCHAR(500),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    INDEX idx_events_place (place_id)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- User-facing app tables (sample/synthetic data)
-- ---------------------------------------------------------------------
CREATE TABLE users (
    id INT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20),
    signup_date DATE
) ENGINE=InnoDB;

CREATE TABLE reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    place_id INT NOT NULL,
    user_id INT NOT NULL,
    rating DECIMAL(2,1) CHECK (rating BETWEEN 1.0 AND 5.0),
    review_text TEXT,
    review_date DATE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_reviews_place (place_id),
    INDEX idx_reviews_user (user_id)
) ENGINE=InnoDB;

CREATE TABLE bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    place_id INT NOT NULL,
    num_tickets INT NOT NULL DEFAULT 1,
    status ENUM('Confirmed','Cancelled','Pending') DEFAULT 'Pending',
    booking_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    INDEX idx_bookings_user (user_id),
    INDEX idx_bookings_place (place_id)
) ENGINE=InnoDB;

CREATE TABLE wishlists (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    place_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    UNIQUE KEY uq_user_place_wishlist (user_id, place_id)
) ENGINE=InnoDB;

CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    message VARCHAR(255) NOT NULL,
    is_read TINYINT(1) DEFAULT 0,
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_notif_user (user_id)
) ENGINE=InnoDB;

-- =====================================================================
-- Import order for LOAD DATA / Django loaddata:
-- states -> districts -> cities -> categories -> places ->
-- place_images -> ticket_prices -> events -> users -> reviews ->
-- bookings -> wishlists -> notifications
-- =====================================================================
