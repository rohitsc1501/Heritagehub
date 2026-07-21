"""API views for core heritage data."""
from rest_framework import viewsets, permissions, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from .models import State, District, City, Category, Place, PlaceImage, TicketPrice, Event
from .serializers import (
    StateSerializer, StateDetailSerializer, CategorySerializer,
    PlaceListSerializer, PlaceDetailSerializer, EventSerializer,
    PlaceImageSerializer, TicketPriceSerializer
)
from .filters import PlaceFilter


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve states with nested districts/cities."""
    queryset = State.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StateDetailSerializer
        return StateSerializer

    def get_queryset(self):
        return State.objects.all().order_by('name')


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve categories with place counts."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def places(self, request, slug=None):
        """GET /api/categories/{slug}/places/ — places in this category."""
        category = self.get_object()
        places = Place.objects.filter(category=category, status='Active')
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data)


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    """List, retrieve, search, and filter heritage places."""
    queryset = Place.objects.filter(status='Active').select_related(
        'city__district__state', 'category'
    )
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PlaceFilter
    search_fields = ['place_name', 'description', 'city__city_name',
                     'city__district__state__name', 'category__name']
    ordering_fields = ['rating', 'number_of_reviews', 'place_name', 'entry_fee_indian']
    ordering = ['-rating']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlaceDetailSerializer
        return PlaceListSerializer

    @action(detail=False, methods=['get'])
    def trending(self, request):
        """GET /api/places/trending/ — Most reviewed places."""
        places = self.get_queryset().order_by('-number_of_reviews')[:12]
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unesco(self, request):
        """GET /api/places/unesco/ — UNESCO World Heritage Sites."""
        places = self.get_queryset().filter(unesco_status='Yes')
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        """GET /api/places/top_rated/ — Highest rated places."""
        places = self.get_queryset().order_by('-rating')[:12]
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search_suggestions(self, request):
        """GET /api/places/search_suggestions/?q=... — Autocomplete."""
        query = request.query_params.get('q', '').strip()
        if len(query) < 2:
            return Response([])
            
        terms = query.split()
        q_objects = Q()
        for term in terms:
            q_objects &= (
                Q(place_name__icontains=term) |
                Q(city__city_name__icontains=term) |
                Q(city__district__state__name__icontains=term) |
                Q(category__name__icontains=term)
            )
            
        places = Place.objects.filter(q_objects, status='Active').values(
            'id', 'place_name', 'slug', 'category__name', 'city__city_name'
        )[:10]
        return Response(list(places))

    @action(detail=True, methods=['get'])
    def nearby(self, request, slug=None):
        """GET /api/places/{slug}/nearby/ — Places in same state."""
        place = self.get_object()
        state = place.city.district.state
        nearby = Place.objects.filter(
            city__district__state=state, status='Active'
        ).exclude(id=place.id).order_by('-rating')[:6]
        serializer = PlaceListSerializer(nearby, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], pagination_class=None)
    def map_data(self, request):
        """GET /api/places/map_data/ — All places with coordinates for the map (unpaginated)."""
        places = self.get_queryset().filter(latitude__isnull=False, longitude__isnull=False)
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve events."""
    queryset = Event.objects.filter(is_active=True).select_related('place')
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
