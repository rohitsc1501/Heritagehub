"""Django admin for core models."""
from django.contrib import admin
from .models import State, District, City, Category, Place, PlaceImage, TicketPrice, Event


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']
    search_fields = ['name']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['district_name', 'state']
    list_filter = ['state']
    search_fields = ['district_name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['city_name', 'district']
    search_fields = ['city_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1


class TicketPriceInline(admin.TabularInline):
    model = TicketPrice
    extra = 1


class EventInline(admin.TabularInline):
    model = Event
    extra = 0


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['place_name', 'category', 'city', 'rating', 'unesco_status', 'status']
    list_filter = ['category', 'unesco_status', 'asi_protected', 'status']
    search_fields = ['place_name', 'description']
    prepopulated_fields = {'slug': ('place_name',)}
    inlines = [PlaceImageInline, TicketPriceInline, EventInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'place', 'event_schedule', 'is_active']
    list_filter = ['is_active']
    search_fields = ['event_name']
