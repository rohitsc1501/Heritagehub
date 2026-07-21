import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heritagehub.settings')
django.setup()

from apps.core.models import Place, Category, State, City, District

places_data = [
    {
        "name": "Hawa Mahal",
        "category": "Palaces",
        "city": "Jaipur",
        "state": "Rajasthan",
        "desc": "The Palace of Winds, known for its intricate honeycomb facade.",
        "fee": 50
    },
    {
        "name": "India Gate",
        "category": "Historical Monuments",
        "city": "New Delhi",
        "state": "Delhi",
        "desc": "A war memorial located astride the Rajpath.",
        "fee": 50
    },
    {
        "name": "Lotus Temple",
        "category": "Temples",
        "city": "New Delhi",
        "state": "Delhi",
        "desc": "A Bahá'í House of Worship notable for its flowerlike shape.",
        "fee": 50
    },
    {
        "name": "Akshardham Temple",
        "category": "Temples",
        "city": "New Delhi",
        "state": "Delhi",
        "desc": "A massive Hindu temple complex displaying millennia of traditional culture.",
        "fee": 250
    },
    {
        "name": "Vivekananda Rock Memorial",
        "category": "Memorials",
        "city": "Kanyakumari",
        "state": "Tamil Nadu",
        "desc": "A monument built on a rock island to honor Swami Vivekananda.",
        "fee": 50
    },
    {
        "name": "Gol Gumbaz",
        "category": "Historical Monuments",
        "city": "Bijapur",
        "state": "Karnataka",
        "desc": "The mausoleum of King Mohammed Adil Shah, featuring one of the largest domes in the world.",
        "fee": 50
    },
    {
        "name": "Kumbhalgarh Fort",
        "category": "Forts",
        "city": "Rajsamand",
        "state": "Rajasthan",
        "desc": "A Mewar fortress known for its massive wall, second longest in the world.",
        "fee": 50
    },
    {
        "name": "Chittorgarh Fort",
        "category": "Forts",
        "city": "Chittorgarh",
        "state": "Rajasthan",
        "desc": "One of the largest forts in India and a UNESCO World Heritage Site.",
        "fee": 50
    },
    {
        "name": "Somnath Temple",
        "category": "Temples",
        "city": "Prabhas Patan",
        "state": "Gujarat",
        "desc": "One of the twelve Jyotirlinga shrines of Shiva.",
        "fee": 50
    },
    {
        "name": "Howrah Bridge",
        "category": "Historical Monuments",
        "city": "Kolkata",
        "state": "West Bengal",
        "desc": "An iconic cantilever bridge over the Hooghly River.",
        "fee": 50
    },
    {
        "name": "Badrinath Temple",
        "category": "Temples",
        "city": "Badrinath",
        "state": "Uttarakhand",
        "desc": "A Hindu temple dedicated to Lord Vishnu, one of the Char Dham pilgrimage sites.",
        "fee": 50
    },
    {
        "name": "Kedarnath Temple",
        "category": "Temples",
        "city": "Kedarnath",
        "state": "Uttarakhand",
        "desc": "A Hindu temple dedicated to Lord Shiva, located in the Garhwal Himalayan range.",
        "fee": 50
    }
]

for item in places_data:
    cat, _ = Category.objects.get_or_create(name=item["category"])
    state, _ = State.objects.get_or_create(name=item["state"])
    district, _ = District.objects.get_or_create(district_name=item["city"], state=state)
    city, _ = City.objects.get_or_create(city_name=item["city"], district=district)
    
    if not Place.objects.filter(place_name=item["name"]).exists():
        p = Place(
            place_name=item["name"],
            category=cat,
            city=city,
            description=item["desc"],
            entry_fee_indian=item["fee"],
            entry_fee_foreigner=item["fee"] * 10,
            latitude=20.0,
            longitude=77.0,
            opening_time="09:00:00",
            closing_time="17:00:00",
            best_time_to_visit="October to March",
            average_visit_duration="2 hours"
        )
        p.save()
        print(f"Added {item['name']}")
    else:
        print(f"Skipped {item['name']}, already exists.")
