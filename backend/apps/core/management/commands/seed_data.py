"""
Management command to seed the database from CSV files in datasetfiles/.
Usage: python manage.py seed_data
"""
import csv
import os
from pathlib import Path
from datetime import datetime, time
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.core.models import State, District, City, Category, Place, PlaceImage, TicketPrice, Event
from apps.accounts.models import User
from apps.reviews.models import Review
from apps.bookings.models import Booking
from apps.wishlist.models import Wishlist
from apps.notifications.models import Notification

# Unsplash placeholder images for Indian heritage sites
CATEGORY_IMAGES = {
    'temples': 'https://images.unsplash.com/photo-1564804955013-e02d1f359004?w=800&q=80',
    'forts': 'https://images.unsplash.com/photo-1587474260584-136574528ed5?w=800&q=80',
    'palaces': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800&q=80',
    'museums': 'https://images.unsplash.com/photo-1566127444979-b3d2b654e3d7?w=800&q=80',
    'beaches': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80',
    'waterfalls': 'https://images.unsplash.com/photo-1432405972618-c6b0cfba1842?w=800&q=80',
    'national parks': 'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&q=80',
    'churches': 'https://images.unsplash.com/photo-1543349689-9a4d426bee8e?w=800&q=80',
    'hill stations': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80',
    'caves': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800&q=80',
    'lakes': 'https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=800&q=80',
    'gardens': 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=800&q=80',
    'default': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=80',
}

# Category-specific emoji icons
CATEGORY_ICONS = {
    'UNESCO World Heritage Sites': '🏛️',
    'Museums': '🏛️',
    'Art Galleries': '🎨',
    'Historical Monuments': '🏰',
    'Archaeological Sites': '⛏️',
    'Forts': '🏰',
    'Palaces': '👑',
    'Caves': '🕳️',
    'Temples': '🛕',
    'Mosques': '🕌',
    'Churches': '⛪',
    'Gurudwaras': '🙏',
    'Jain Temples': '🛕',
    'Buddhist Sites': '☸️',
    'Memorials': '🪦',
    'National Parks': '🌿',
    'Wildlife Sanctuaries': '🦁',
    'Tiger Reserves': '🐅',
    'Biosphere Reserves': '🌍',
    'Natural Heritage Sites': '🏞️',
    'Botanical Gardens': '🌺',
    'Science Museums': '🔬',
    'Tribal Museums': '🎭',
    'Planetariums': '🔭',
    'Aquariums': '🐠',
    'Beaches': '🏖️',
    'Waterfalls': '🌊',
    'Lakes': '🏞️',
    'Rivers': '🌊',
    'Hill Stations': '⛰️',
    'Eco Parks': '🌳',
    'Heritage Walks': '🚶',
    'Cultural Festivals': '🎉',
    'Handicraft Villages': '🧶',
    'Heritage Railways': '🚂',
    'Lighthouses': '🗼',
    'Stepwells': '🏗️',
    'Clock Towers': '🕐',
    'Gardens': '🌷',
    'Observatories': '🔭',
    'Zoos': '🦒',
    'Theme Museums': '🖼️',
    'Heritage Hotels': '🏨',
}


def get_image_for_category(category_name):
    """Get a relevant Unsplash image URL based on category."""
    cat_lower = category_name.lower()
    for key, url in CATEGORY_IMAGES.items():
        if key in cat_lower:
            return url
    return CATEGORY_IMAGES['default']


class Command(BaseCommand):
    help = 'Seed the database from CSV files in datasetfiles/'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true',
                            help='Clear existing data before seeding')

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        data_dir = base_dir.parent / 'datasetfiles'

        if not data_dir.exists():
            self.stderr.write(f"Data directory not found: {data_dir}")
            return

        if options['clear']:
            self.stdout.write("Clearing existing data...")
            Notification.objects.all().delete()
            Wishlist.objects.all().delete()
            Booking.objects.all().delete()
            Review.objects.all().delete()
            Event.objects.all().delete()
            TicketPrice.objects.all().delete()
            PlaceImage.objects.all().delete()
            Place.objects.all().delete()
            Category.objects.all().delete()
            City.objects.all().delete()
            District.objects.all().delete()
            State.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self._seed_states(data_dir / 'states.csv')
        self._seed_districts(data_dir / 'districts.csv')
        self._seed_cities(data_dir / 'cities.csv')
        self._seed_categories(data_dir / 'categories.csv')
        self._seed_places(data_dir / 'places.csv')
        self._seed_ticket_prices(data_dir / 'ticket_prices.csv')
        self._seed_place_images(data_dir / 'place_images.csv')
        self._seed_events(data_dir / 'events.csv')
        self._seed_users(data_dir / 'users.csv')
        self._seed_reviews(data_dir / 'reviews.csv')
        self._seed_bookings(data_dir / 'bookings.csv')
        self._seed_wishlists(data_dir / 'wishlists.csv')
        self._seed_notifications(data_dir / 'notifications.csv')
        self._create_admin()

        self.stdout.write(self.style.SUCCESS('✅ Database seeded successfully!'))

    def _read_csv(self, filepath):
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _seed_states(self, filepath):
        rows = self._read_csv(filepath)
        for row in rows:
            State.objects.get_or_create(
                id=int(row['id']),
                defaults={'name': row['name'].strip(), 'type': row['type'].strip()}
            )
        self.stdout.write(f"  ✓ {State.objects.count()} states loaded")

    def _seed_districts(self, filepath):
        rows = self._read_csv(filepath)
        for row in rows:
            District.objects.get_or_create(
                id=int(row['id']),
                defaults={
                    'state_id': int(row['state_id']),
                    'district_name': row['district_name'].strip()
                }
            )
        self.stdout.write(f"  ✓ {District.objects.count()} districts loaded")

    def _seed_cities(self, filepath):
        rows = self._read_csv(filepath)
        for row in rows:
            City.objects.get_or_create(
                id=int(row['id']),
                defaults={
                    'district_id': int(row['district_id']),
                    'city_name': row['city_name'].strip()
                }
            )
        self.stdout.write(f"  ✓ {City.objects.count()} cities loaded")

    def _seed_categories(self, filepath):
        rows = self._read_csv(filepath)
        for row in rows:
            name = row['name'].strip()
            Category.objects.get_or_create(
                id=int(row['id']),
                defaults={
                    'name': name,
                    'icon': CATEGORY_ICONS.get(name, '📍'),
                }
            )
        self.stdout.write(f"  ✓ {Category.objects.count()} categories loaded")

    def _seed_places(self, filepath):
        rows = self._read_csv(filepath)
        # Build city lookup: csv has city name and we need city_id
        city_lookup = {}
        for city in City.objects.select_related('district__state').all():
            key = city.city_name.lower().strip()
            city_lookup[key] = city

        cat_lookup = {}
        for cat in Category.objects.all():
            cat_lookup[cat.name.lower().strip()] = cat

        for row in rows:
            place_id = int(row['id'])
            if Place.objects.filter(id=place_id).exists():
                continue

            city_name = row.get('city', '').strip().lower()
            city = city_lookup.get(city_name)
            if not city:
                # Try matching by place id to city id
                try:
                    city = City.objects.get(id=place_id) if place_id <= City.objects.count() else City.objects.first()
                except City.DoesNotExist:
                    city = City.objects.first()

            cat_name = row.get('category', '').strip().lower()
            category = cat_lookup.get(cat_name, Category.objects.first())

            def clean_null(val):
                if not val or val.startswith('NULL') or val == 'N/A':
                    return None
                return val.strip()

            def parse_time(val):
                val = clean_null(val)
                if not val:
                    return None
                try:
                    parts = val.split(':')
                    return time(int(parts[0]), int(parts[1]))
                except (ValueError, IndexError):
                    return None

            def parse_decimal(val):
                val = clean_null(val)
                if not val:
                    return None
                try:
                    return float(val)
                except ValueError:
                    return None

            # Get image URL based on category
            image_url = get_image_for_category(row.get('category', ''))

            Place.objects.create(
                id=place_id,
                city=city,
                category=category,
                subcategory=clean_null(row.get('subcategory', '')),
                place_name=row.get('place_name', '').strip(),
                description=row.get('description', '').strip(),
                history=clean_null(row.get('history', '')),
                year_established=clean_null(row.get('year_established', '')),
                unesco_status=row.get('unesco_status', 'No').strip(),
                asi_protected=row.get('asi_protected', 'No').strip(),
                latitude=parse_decimal(row.get('latitude', '')),
                longitude=parse_decimal(row.get('longitude', '')),
                altitude_m=parse_decimal(row.get('altitude', '')),
                address=clean_null(row.get('address', '')),
                pincode=clean_null(row.get('pincode', '')),
                opening_days=clean_null(row.get('opening_days', '')),
                opening_time=parse_time(row.get('opening_time', '')),
                closing_time=parse_time(row.get('closing_time', '')),
                entry_fee_indian=parse_decimal(row.get('entry_fee_indian', '')),
                entry_fee_foreigner=parse_decimal(row.get('entry_fee_foreigner', '')),
                student_discount=clean_null(row.get('student_discount', '')),
                senior_citizen_discount=clean_null(row.get('senior_citizen_discount', '')),
                parking_available=clean_null(row.get('parking_available', '')),
                wheelchair_accessible=clean_null(row.get('wheelchair_accessible', '')),
                guided_tours=clean_null(row.get('guided_tours', '')),
                audio_guide=clean_null(row.get('audio_guide', '')),
                photography_allowed=clean_null(row.get('photography_allowed', '')),
                videography_allowed=clean_null(row.get('videography_allowed', '')),
                best_time_to_visit=clean_null(row.get('best_time_to_visit', '')),
                average_visit_duration=clean_null(row.get('average_visit_duration', '')),
                nearest_airport=clean_null(row.get('nearest_airport', '')),
                nearest_railway_station=clean_null(row.get('nearest_railway_station', '')),
                nearest_bus_station=clean_null(row.get('nearest_bus_station', '')),
                official_website=None,  # URLs are NULL in CSV
                contact_number=clean_null(row.get('contact_number', '')),
                email=None,
                rating=parse_decimal(row.get('rating', '0')) or 0,
                number_of_reviews=int(row.get('number_of_reviews', '0') or 0),
                main_image_url=image_url,
                status=row.get('status', 'Active').strip(),
            )
        self.stdout.write(f"  ✓ {Place.objects.count()} places loaded")

    def _seed_ticket_prices(self, filepath):
        rows = self._read_csv(filepath)
        for row in rows:
            tp_id = int(row['id'])
            if TicketPrice.objects.filter(id=tp_id).exists():
                continue
            try:
                TicketPrice.objects.create(
                    id=tp_id,
                    place_id=int(row['place_id']),
                    visitor_type=row['visitor_type'].strip(),
                    price=float(row['price']),
                    currency=row.get('currency', 'INR').strip(),
                )
            except Exception:
                pass
        self.stdout.write(f"  ✓ {TicketPrice.objects.count()} ticket prices loaded")

    def _seed_place_images(self, filepath):
        rows = self._read_csv(filepath)
        for row in rows:
            img_id = int(row['id'])
            if PlaceImage.objects.filter(id=img_id).exists():
                continue
            place_id = int(row['place_id'])
            try:
                place = Place.objects.get(id=place_id)
                # Use category-based image as placeholder
                image_url = get_image_for_category(place.category.name)
                PlaceImage.objects.create(
                    id=img_id,
                    place_id=place_id,
                    image_url=image_url,
                    sort_order=int(row.get('sort_order', 0)),
                    image_type=row.get('image_type', 'Gallery').strip(),
                )
            except Place.DoesNotExist:
                pass
        self.stdout.write(f"  ✓ {PlaceImage.objects.count()} place images loaded")

    def _seed_events(self, filepath):
        rows = self._read_csv(filepath)
        for row in rows:
            event_id = int(row['id'])
            if Event.objects.filter(id=event_id).exists():
                continue
            try:
                Event.objects.create(
                    id=event_id,
                    place_id=int(row['place_id']),
                    event_name=row['event_name'].strip(),
                    event_schedule=row.get('event_schedule', '').strip() or None,
                    notes=row.get('notes', '').strip() or None,
                )
            except Exception:
                pass
        self.stdout.write(f"  ✓ {Event.objects.count()} events loaded")

    def _seed_users(self, filepath):
        rows = self._read_csv(filepath)
        for row in rows:
            user_id = int(row['id'])
            if User.objects.filter(id=user_id).exists():
                continue
            name_parts = row['full_name'].strip().split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            User.objects.create_user(
                id=user_id,
                username=f"user{user_id}",
                email=row['email'].strip(),
                first_name=first_name,
                last_name=last_name,
                phone=row.get('phone', '').strip(),
                password='heritage2024',
                role='visitor',
            )
        self.stdout.write(f"  ✓ {User.objects.filter(role='visitor').count()} visitors loaded")

    def _seed_reviews(self, filepath):
        rows = self._read_csv(filepath)
        created = 0
        for row in rows:
            review_id = int(row['id'])
            if Review.objects.filter(id=review_id).exists():
                continue
            user_id = int(row['user_id'])
            # Map CSV user_ids to actual users (CSV has random IDs)
            user = User.objects.filter(role='visitor').order_by('?').first()
            if not user:
                continue
            try:
                Review.objects.create(
                    id=review_id,
                    place_id=int(row['place_id']),
                    user=user,
                    rating=float(row['rating']),
                    review_text=row.get('review_text', '').strip(),
                )
                created += 1
            except Exception:
                pass
        self.stdout.write(f"  ✓ {created} reviews loaded")

    def _seed_bookings(self, filepath):
        rows = self._read_csv(filepath)
        created = 0
        for row in rows:
            booking_id = int(row['id'])
            if Booking.objects.filter(id=booking_id).exists():
                continue
            csv_user_id = int(row['user_id'])
            try:
                user = User.objects.get(id=csv_user_id)
            except User.DoesNotExist:
                user = User.objects.filter(role='visitor').first()
                if not user:
                    continue
            try:
                place = Place.objects.get(id=int(row['place_id']))
                num_tickets = int(row['num_tickets'])
                price = float(place.entry_fee_indian or 25) * num_tickets
                tax = round(price * 0.18, 2)
                Booking.objects.create(
                    id=booking_id,
                    user=user,
                    place=place,
                    visit_date=row['booking_date'],
                    adults=num_tickets,
                    subtotal=price,
                    tax=tax,
                    total_price=round(price + tax, 2),
                    status=row['status'].strip(),
                )
                created += 1
            except Exception:
                pass
        self.stdout.write(f"  ✓ {created} bookings loaded")

    def _seed_wishlists(self, filepath):
        rows = self._read_csv(filepath)
        created = 0
        for row in rows:
            csv_user_id = int(row['user_id'])
            try:
                user = User.objects.get(id=csv_user_id)
                Wishlist.objects.get_or_create(
                    user=user, place_id=int(row['place_id'])
                )
                created += 1
            except Exception:
                pass
        self.stdout.write(f"  ✓ {created} wishlist items loaded")

    def _seed_notifications(self, filepath):
        rows = self._read_csv(filepath)
        created = 0
        type_map = {
            'Booking confirmed': 'booking',
            'Reminder: upcoming visit': 'reminder',
            'New event near you': 'event',
            'Price drop alert': 'price',
        }
        for row in rows:
            csv_user_id = int(row['user_id'])
            try:
                user = User.objects.get(id=csv_user_id)
                msg = row['message'].strip()
                Notification.objects.create(
                    user=user,
                    message=msg,
                    notification_type=type_map.get(msg, 'system'),
                    is_read=bool(int(row.get('is_read', 0))),
                )
                created += 1
            except Exception:
                pass
        self.stdout.write(f"  ✓ {created} notifications loaded")

    def _create_admin(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@heritagehub.in',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin',
            )
            self.stdout.write("  ✓ Admin user created (admin / admin123)")
        # Also create a demo visitor
        if not User.objects.filter(username='demo').exists():
            User.objects.create_user(
                username='demo',
                email='demo@heritagehub.in',
                password='demo1234',
                first_name='Demo',
                last_name='Visitor',
                role='visitor',
            )
            self.stdout.write("  ✓ Demo visitor created (demo / demo1234)")
