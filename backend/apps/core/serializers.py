"""Serializers for core heritage data models."""
from rest_framework import serializers
from .models import State, District, City, Category, Place, PlaceImage, TicketPrice, Event


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'type', 'slug']


class DistrictSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)

    class Meta:
        model = District
        fields = ['id', 'district_name', 'state', 'state_name']


class CitySerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.district_name', read_only=True)
    state_name = serializers.CharField(source='district.state.name', read_only=True)

    class Meta:
        model = City
        fields = ['id', 'city_name', 'district_name', 'state_name']


class CategorySerializer(serializers.ModelSerializer):
    place_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'image', 'place_count']

    def get_place_count(self, obj):
        return obj.places.filter(status='Active').count()


class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = ['id', 'image_url', 'image_file', 'sort_order', 'image_type']


class TicketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPrice
        fields = ['id', 'visitor_type', 'price', 'currency']


class EventSerializer(serializers.ModelSerializer):
    place_name = serializers.CharField(source='place.place_name', read_only=True)
    place_slug = serializers.CharField(source='place.slug', read_only=True)
    place_image = serializers.CharField(source='place.main_image_url', read_only=True)
    state_name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'place', 'place_name', 'place_slug', 'place_image',
                  'event_name', 'event_schedule', 'notes', 'start_date',
                  'end_date', 'is_active', 'state_name', 'created_at']

    def get_state_name(self, obj):
        return obj.place.city.district.state.name


class PlaceListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views (cards)."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    city_name = serializers.CharField(source='city.city_name', read_only=True)
    state_name = serializers.SerializerMethodField()
    entry_fee = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ['id', 'place_name', 'slug', 'description', 'category',
                  'category_name', 'category_slug', 'city_name', 'state_name',
                  'unesco_status', 'asi_protected', 'rating', 'number_of_reviews',
                  'main_image_url', 'entry_fee', 'best_time_to_visit', 'status',
                  'latitude', 'longitude']

    def get_state_name(self, obj):
        return obj.city.district.state.name

    def get_entry_fee(self, obj):
        return obj.entry_fee_indian


class PlaceDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail view."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    city_name = serializers.CharField(source='city.city_name', read_only=True)
    district_name = serializers.SerializerMethodField()
    state_name = serializers.SerializerMethodField()
    images = PlaceImageSerializer(many=True, read_only=True)
    ticket_prices = TicketPriceSerializer(many=True, read_only=True)
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = '__all__'

    def get_state_name(self, obj):
        return obj.city.district.state.name

    def get_district_name(self, obj):
        return obj.city.district.district_name


class StateDetailSerializer(serializers.ModelSerializer):
    """State with nested districts and cities."""
    districts = serializers.SerializerMethodField()
    place_count = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ['id', 'name', 'type', 'slug', 'districts', 'place_count']

    def get_districts(self, obj):
        districts = obj.districts.all()
        result = []
        for d in districts:
            cities = [{'id': c.id, 'city_name': c.city_name} for c in d.cities.all()]
            result.append({
                'id': d.id,
                'district_name': d.district_name,
                'cities': cities,
            })
        return result

    def get_place_count(self, obj):
        return Place.objects.filter(
            city__district__state=obj, status='Active'
        ).count()
