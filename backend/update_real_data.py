import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heritagehub.settings')
django.setup()

from apps.core.models import Place

ASI_LINK = "https://asi.payumoney.com/"
RAJASTHAN_LINK = "https://bookrajasthanmonuments.in/"

updates = {
    "taj-mahal": (50, ASI_LINK),
    "qutub-minar": (35, ASI_LINK),
    "red-fort": (35, ASI_LINK),
    "agra-fort": (40, ASI_LINK),
    "sun-temple": (40, ASI_LINK),
    "konark": (40, ASI_LINK),
    "khajuraho": (40, ASI_LINK),
    "hampi": (40, ASI_LINK),
    "ajanta": (40, ASI_LINK),
    "ellora": (40, ASI_LINK),
    "elephanta": (40, ASI_LINK),
    "fatehpur-sikri": (40, ASI_LINK),
    "mahabalipuram": (40, ASI_LINK),
    "sanchi": (40, ASI_LINK),
    
    # State links
    "hawa-mahal": (50, RAJASTHAN_LINK),
    "amer-fort": (100, RAJASTHAN_LINK),
    "kumbhalgarh": (40, RAJASTHAN_LINK),
    "chittorgarh": (40, RAJASTHAN_LINK),
    "jantar-mantar": (50, RAJASTHAN_LINK),
    "mehrangarh": (100, "https://www.mehrangarh.org/"),
    "city-palace-udaipur": (300, "https://citypalacemuseum.org/"),
    "victoria-memorial": (30, "https://www.victoriamemorial-cal.org/"),
    "mysore-palace": (100, "http://mysorepalace.karnataka.gov.in/"),
    "golconda": (25, ASI_LINK),
    "charminar": (25, ASI_LINK),
}

updated_count = 0

for place in Place.objects.all():
    matched = False
    for key, (price, link) in updates.items():
        if key in place.slug:
            place.entry_fee_indian = price
            place.booking_url = link
            place.save()
            updated_count += 1
            print(f"Updated {place.place_name}: Rs {price}, Link: {link}")
            matched = True
            break
            
    # For remaining ASI protected sites, assign standard ASI link and standard ₹35 fee
    if not matched and place.asi_protected == 'Yes':
        place.booking_url = ASI_LINK
        if place.entry_fee_indian == 0 or place.entry_fee_indian is None:
            place.entry_fee_indian = 35 
        place.save()
        updated_count += 1
        print(f"Default ASI update for {place.place_name}")

print(f"\nTotal places updated with official links and prices: {updated_count}")
