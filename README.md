# 🏛️ Monumenta (HeritageHub)

Monumenta is a comprehensive, modern web application designed to help users explore, discover, and experience India's rich cultural heritage. From stunning UNESCO World Heritage sites to ancient temples and magnificent forts, Monumenta serves as a one-stop portal for heritage tourism.

![Monumenta Hero](frontend/public/vite.svg) <!-- Replace with actual screenshot of your hero section -->

## ✨ Features

- **🌍 Interactive Explore Page:** Browse heritage sites with powerful filters (Category, State, UNESCO Status, Rating).
- **🗺️ Interactive Maps:** Built with Leaflet.js to pinpoint exactly where monuments are located across the country.
- **🎟️ Seamless Ticket Booking:** A BookMyShow-style ticket booking experience featuring digital tickets with generated barcodes.
- **⭐ Reviews & Ratings:** Read and write reviews for places you've visited.
- **❤️ Wishlist:** Save your favorite monuments to your personal wishlist for future trips.
- **📱 Responsive & Premium Design:** Buttery smooth scroll animations, glassmorphism UI elements, and a responsive layout that works beautifully on mobile and desktop.
- **🔍 Intelligent Search:** A robust search engine with autocomplete suggestions that splits terms and searches across names, states, and categories.

## 🛠️ Technology Stack

**Frontend:**
- React 19 (built with Vite)
- React Router (Client-side routing)
- Leaflet & React-Leaflet (Interactive Maps)
- Chart.js (Data visualizations)
- Vanilla CSS (Custom design system, animations, and glassmorphism)

**Backend:**
- Django 5.x
- Django Rest Framework (DRF)
- SQLite (Default) / PostgreSQL (Supported)
- Django-Filter (Advanced query filtering)

## 🚀 Getting Started

### Prerequisites
Make sure you have [Node.js](https://nodejs.org/) (v18+) and [Python](https://www.python.org/) (v3.10+) installed.

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/Monumenta.git
cd Monumenta
```

### 2. Backend Setup (Django)
```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations to set up the database
python manage.py migrate

# Create a superuser (for admin access)
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver
```
The backend API will run at `http://127.0.0.1:8000/api/`.

### 3. Frontend Setup (React/Vite)
Open a new terminal window and navigate to the frontend directory:
```bash
cd Monumenta/frontend

# Install Node modules
npm install

# Start the Vite development server
npm run dev
```
The frontend will run at `http://localhost:5173`.

## 📁 Project Structure

```
Monumenta/
├── backend/                 # Django Backend
│   ├── apps/
│   │   ├── core/            # Main app (Places, Categories, Cities)
│   │   ├── bookings/        # Ticket booking logic
│   │   ├── reviews/         # Review & rating system
│   │   └── wishlist/        # User wishlist logic
│   ├── heritagehub/         # Django project settings
│   └── manage.py            # Django CLI
└── frontend/                # React Frontend (Vite)
    ├── src/
    │   ├── components/      # Reusable UI components (SearchBar, ScrollReveal, etc.)
    │   ├── pages/           # Route views (Home, Explore, PlaceDetail, Profile)
    │   ├── services/        # Axios API services
    │   └── utils/           # Helper functions & constants
    └── package.json
```

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
