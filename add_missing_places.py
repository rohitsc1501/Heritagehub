import os
import sys
import django
import random
from decimal import Decimal

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heritagehub.settings')
django.setup()

from apps.core.models import Category, Place, City, State, District

def get_or_create_city(city_name, state_name):
    state, _ = State.objects.get_or_create(name=state_name, defaults={'type': 'State'})
    district, _ = District.objects.get_or_create(district_name=city_name + " District", state=state)
    city, _ = City.objects.get_or_create(city_name=city_name, district=district)
    return city

def main():
    new_places_data = [
        # Churches
        {
            "category_name": "Churches", "name": "Basilica of Bom Jesus", "city": "Old Goa", "state": "Goa",
            "desc": "A UNESCO World Heritage Site in Goa which holds the mortal remains of St. Francis Xavier.",
            "unesco": "Yes", "price": "0.00"
        },
        {
            "category_name": "Churches", "name": "San Thome Basilica", "city": "Chennai", "state": "Tamil Nadu",
            "desc": "A Roman Catholic minor basilica built over the tomb of Thomas the Apostle.",
            "unesco": "No", "price": "0.00"
        },
        {
            "category_name": "Churches", "name": "Medak Cathedral", "city": "Medak", "state": "Telangana",
            "desc": "One of the largest churches in India, featuring breathtaking stained glass windows.",
            "unesco": "No", "price": "0.00"
        },
        
        # Beaches
        {
            "category_name": "Beaches", "name": "Radhanagar Beach", "city": "Havelock Island", "state": "Andaman and Nicobar Islands",
            "desc": "Often cited as the best beach in Asia, known for its pristine white sands and crystal-clear water.",
            "unesco": "No", "price": "50.00"  # Environment fee
        },
        {
            "category_name": "Beaches", "name": "Palolem Beach", "city": "Canacona", "state": "Goa",
            "desc": "A crescent-shaped beach known for its calm waters and vibrant nightlife.",
            "unesco": "No", "price": "0.00"
        },
        {
            "category_name": "Beaches", "name": "Marina Beach", "city": "Chennai", "state": "Tamil Nadu",
            "desc": "The longest natural urban beach in India, a prominent landmark of Chennai.",
            "unesco": "No", "price": "0.00"
        },
        {
            "category_name": "Beaches", "name": "Varkala Beach", "city": "Varkala", "state": "Kerala",
            "desc": "Famous for its stunning cliffs dropping into the Arabian Sea and natural springs.",
            "unesco": "No", "price": "0.00"
        },

        # Art Galleries
        {
            "category_name": "Art Galleries", "name": "Kiran Nadar Museum of Art", "city": "New Delhi", "state": "Delhi",
            "desc": "India's first private museum exhibiting modern and contemporary works.",
            "unesco": "No", "price": "0.00"
        },
        {
            "category_name": "Art Galleries", "name": "Government Museum and Art Gallery", "city": "Chandigarh", "state": "Chandigarh",
            "desc": "A premier museum housing Gandharan sculptures and Pahari miniature paintings.",
            "unesco": "No", "price": "10.00"
        },
        {
            "category_name": "Art Galleries", "name": "Chhatrapati Shivaji Maharaj Vastu Sangrahalaya", "city": "Mumbai", "state": "Maharashtra",
            "desc": "Formerly the Prince of Wales Museum, featuring extensive art, archaeology, and natural history galleries.",
            "unesco": "No", "price": "150.00"
        },

        # Zoos
        {
            "category_name": "Zoos", "name": "Mysore Zoo", "city": "Mysuru", "state": "Karnataka",
            "desc": "Sri Chamarajendra Zoological Gardens, one of the oldest and most popular zoos in India.",
            "unesco": "No", "price": "100.00"
        },
        {
            "category_name": "Zoos", "name": "Arignar Anna Zoological Park", "city": "Chennai", "state": "Tamil Nadu",
            "desc": "Also known as Vandalur Zoo, it is India's largest zoological park by area.",
            "unesco": "No", "price": "200.00"
        },
        {
            "category_name": "Zoos", "name": "Padmaja Naidu Himalayan Zoological Park", "city": "Darjeeling", "state": "West Bengal",
            "desc": "Internationally renowned for its conservation breeding programs of Red Pandas and Snow Leopards.",
            "unesco": "No", "price": "60.00"
        },

        # Botanical Gardens
        {
            "category_name": "Botanical Gardens", "name": "Acharya Jagadish Chandra Bose Indian Botanic Garden", "city": "Howrah", "state": "West Bengal",
            "desc": "Famous for the massive Great Banyan Tree, the largest in the world.",
            "unesco": "No", "price": "30.00"
        },
        {
            "category_name": "Botanical Gardens", "name": "Ooty Botanical Gardens", "city": "Ooty", "state": "Tamil Nadu",
            "desc": "A sprawling 55-acre garden featuring thousands of exotic plant species and a fossilized tree trunk.",
            "unesco": "No", "price": "50.00"
        },
        
        # Planetariums
        {
            "category_name": "Planetariums", "name": "M. P. Birla Planetarium", "city": "Kolkata", "state": "West Bengal",
            "desc": "The oldest and largest planetarium in Asia, featuring a design inspired by the Sanchi Stupa.",
            "unesco": "No", "price": "120.00"
        },
        {
            "category_name": "Planetariums", "name": "Nehru Planetarium", "city": "New Delhi", "state": "Delhi",
            "desc": "A major educational and public outreach center for astronomy located at Teen Murti Bhavan.",
            "unesco": "No", "price": "100.00"
        },

        # Observatories
        {
            "category_name": "Observatories", "name": "Jantar Mantar", "city": "New Delhi", "state": "Delhi",
            "desc": "A massive astronomical observatory built in 1724, featuring 13 architectural astronomy instruments.",
            "unesco": "No", "price": "25.00"
        },
        {
            "category_name": "Observatories", "name": "Vainu Bappu Observatory", "city": "Kavalur", "state": "Tamil Nadu",
            "desc": "An astronomical observatory owned by the Indian Institute of Astrophysics, housing the Vainu Bappu Telescope.",
            "unesco": "No", "price": "0.00"
        },

        # Theme Museums
        {
            "category_name": "Theme Museums", "name": "Sulabh International Museum of Toilets", "city": "New Delhi", "state": "Delhi",
            "desc": "A unique museum tracing the history of sanitation and toilets over the last 4,500 years.",
            "unesco": "No", "price": "0.00"
        },
        {
            "category_name": "Theme Museums", "name": "Heritage Transport Museum", "city": "Gurgaon", "state": "Haryana",
            "desc": "A brilliant showcase of the history of human transportation in India, featuring vintage cars, trains, and planes.",
            "unesco": "No", "price": "400.00"
        },
        {
            "category_name": "Theme Museums", "name": "Kite Museum", "city": "Ahmedabad", "state": "Gujarat",
            "desc": "The Sanskar Kendra Kite Museum displays over a hundred incredible kites from around the world.",
            "unesco": "No", "price": "10.00"
        },
        
        # Aquariums (Additional)
        {
            "category_name": "Aquariums", "name": "Underwater Aquarium Dubai (Indian Exhibit)", "city": "Virtual", "state": "Global",
            "desc": "An exhibition showcasing exotic marine life.",
            "unesco": "No", "price": "150.00"
        },
        
        # Historical Monuments (Additional)
        {
            "category_name": "Historical Monuments", "name": "Gingee Fort", "city": "Gingee", "state": "Tamil Nadu",
            "desc": "Nicknamed the 'Troy of the East', an impenetrable 16th-century fortress.",
            "unesco": "No", "price": "25.00"
        },
        {
            "category_name": "Historical Monuments", "name": "Kangra Fort", "city": "Kangra", "state": "Himachal Pradesh",
            "desc": "One of the oldest and largest forts in the Himalayas.",
            "unesco": "No", "price": "150.00"
        },
        {
            "category_name": "Historical Monuments", "name": "Murshidabad Hazarduari Palace", "city": "Murshidabad", "state": "West Bengal",
            "desc": "A massive 19th-century palace featuring a thousand doors (out of which 900 are real).",
            "unesco": "No", "price": "20.00"
        }
    ]

    added = 0
    for data in new_places_data:
        try:
            category, _ = Category.objects.get_or_create(name=data["category_name"], defaults={'icon': '📍'})
            city = get_or_create_city(data["city"], data["state"])
            
            placeholder = "https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=80"
            
            if not Place.objects.filter(place_name=data["name"]).exists():
                Place.objects.create(
                    category=category,
                    city=city,
                    place_name=data["name"],
                    description=data["desc"],
                    unesco_status=data["unesco"],
                    main_image_url=placeholder,
                    status="Active",
                    entry_fee_indian=Decimal(data["price"]),
                    rating=Decimal(str(round(random.uniform(4.0, 4.9), 1))),
                    number_of_reviews=random.randint(100, 2000)
                )
                added += 1
                print(f"Added {data['name']} to {data['category_name']} with price ₹{data['price']}")
        except Exception as e:
            print(f"Failed to add {data['name']}: {e}")

    print(f"Successfully added {added} new places.")

if __name__ == "__main__":
    main()
