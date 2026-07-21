import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heritagehub.settings')
django.setup()

from apps.core.models import Place

coords = {
    "Hawa Mahal": (26.9239, 75.8267),
    "India Gate": (28.6129, 77.2295),
    "Lotus Temple": (28.5535, 77.2588),
    "Akshardham Temple": (28.6127, 77.2773),
    "Vivekananda Rock Memorial": (8.0780, 77.5553),
    "Gol Gumbaz": (16.8258, 75.7360),
    "Kumbhalgarh Fort": (25.1528, 73.5870),
    "Chittorgarh Fort": (24.8879, 74.6451),
    "Somnath Temple": (20.8880, 70.4012),
    "Howrah Bridge": (22.5851, 88.3468),
    "Badrinath Temple": (30.7433, 79.4938),
    "Kedarnath Temple": (30.7352, 79.0669)
}

for place_name, (lat, lon) in coords.items():
    try:
        place = Place.objects.get(place_name=place_name)
        place.latitude = lat
        place.longitude = lon
        place.save()
        print(f"Updated {place_name} -> {lat}, {lon}")
    except Place.DoesNotExist:
        print(f"Not found: {place_name}")
