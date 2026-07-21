import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heritagehub.settings')
django.setup()

from apps.core.models import Place

updated = 0
for place in Place.objects.all():
    if not place.entry_fee_indian or float(place.entry_fee_indian) == 0:
        place.entry_fee_indian = 50
        place.save()
        updated += 1

print(f"Successfully updated {updated} remaining free places to a default entry fee of Rs 50.")
