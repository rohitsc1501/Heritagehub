import os
import django
import requests
import time
import urllib.parse

# Setup Django environment
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heritagehub.settings')
django.setup()

from apps.core.models import Place

def get_wikipedia_image(place_name):
    """
    Search Wikipedia for the place name and return the main page image URL.
    """
    # Wikipedia requires a User-Agent header
    headers = {'User-Agent': 'HeritageHubBot/1.0 (contact@heritagehub.in)'}
    
    # 1. Search for the Wikipedia page title
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(place_name)}&utf8=&format=json&srlimit=1"
    try:
        search_res = requests.get(search_url, headers=headers, timeout=5).json()
        if not search_res.get('query', {}).get('search'):
            return None
            
        title = search_res['query']['search'][0]['title']
        
        # 2. Get the page image for that title
        img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&pithumbsize=800"
        img_res = requests.get(img_url, headers=headers, timeout=5).json()
        
        pages = img_res.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'thumbnail' in page_data:
                return page_data['thumbnail']['source']
    except Exception as e:
        print(f"Error fetching for {place_name}: {e}")
    return None

def main():
    places = Place.objects.all()
    total = places.count()
    print(f"Found {total} places to update.")
    
    updated = 0
    for i, place in enumerate(places, 1):
        # Only update if it's still the unsplash placeholder or None
        if not place.main_image_url or 'unsplash.com' in place.main_image_url:
            print(f"[{i}/{total}] Fetching image for {place.place_name}...")
            img = get_wikipedia_image(place.place_name)
            if img:
                place.main_image_url = img
                place.save()
                updated += 1
                print(f"  -> Success: {img}")
            else:
                print("  -> Failed to find Wikipedia image.")
            
            # Be polite to Wikipedia API
            time.sleep(0.1)
        else:
            print(f"[{i}/{total}] Skipping {place.place_name} (already has custom image).")
            
    print(f"\nFinished! Updated {updated} places with Wikipedia images.")

if __name__ == '__main__':
    main()
