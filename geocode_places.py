import os
import django
import sys
import time
import requests
import urllib.parse

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heritagehub.settings')
django.setup()

from apps.core.models import Place

def geocode(place_name, city_name, state_name):
    # Try specific place first
    query = f"{place_name}, {city_name}, India"
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit=1"
    headers = {'User-Agent': 'HeritageHubBot/1.0'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        pass
    
    # Fallback to city
    query = f"{city_name}, {state_name}, India"
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit=1"
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        if data:
            # Add tiny random jitter to city center so pins don't perfectly overlap
            import random
            lat = float(data[0]['lat']) + random.uniform(-0.01, 0.01)
            lon = float(data[0]['lon']) + random.uniform(-0.01, 0.01)
            return lat, lon
    except Exception:
        pass
        
    return None, None

places = Place.objects.filter(latitude__isnull=True)
print(f"Found {places.count()} places without coordinates.")

updated = 0
for place in places:
    lat, lon = geocode(place.place_name, place.city.city_name, place.city.district.state.name)
    if lat and lon:
        place.latitude = lat
        place.longitude = lon
        place.save()
        print(f"Updated {place.place_name} ({lat}, {lon})")
        updated += 1
    else:
        print(f"Could not geocode {place.place_name}")
    time.sleep(1) # Rate limit for nominatim

print(f"Finished updating {updated} places.")
