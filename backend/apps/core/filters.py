"""Django-filter filtersets for Place search and filtering."""
import django_filters
from .models import Place


class PlaceFilter(django_filters.FilterSet):
    """Rich filtering for the Explore page."""
    category = django_filters.NumberFilter(field_name='category__id')
    category_slug = django_filters.CharFilter(field_name='category__slug')
    state = django_filters.CharFilter(method='filter_by_state')
    city = django_filters.CharFilter(field_name='city__city_name', lookup_expr='icontains')
    unesco = django_filters.CharFilter(field_name='unesco_status')
    asi = django_filters.CharFilter(field_name='asi_protected')
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    max_fee = django_filters.NumberFilter(field_name='entry_fee_indian', lookup_expr='lte')
    free_entry = django_filters.BooleanFilter(method='filter_free_entry')
    wheelchair = django_filters.CharFilter(field_name='wheelchair_accessible', lookup_expr='icontains')
    photography = django_filters.CharFilter(field_name='photography_allowed', lookup_expr='icontains')

    class Meta:
        model = Place
        fields = ['category', 'category_slug', 'state', 'city', 'unesco', 'asi',
                  'min_rating', 'max_fee', 'status']

    def filter_by_state(self, queryset, name, value):
        return queryset.filter(city__district__state__name__icontains=value)

    def filter_free_entry(self, queryset, name, value):
        if value:
            return queryset.filter(entry_fee_indian__lte=0)
        return queryset




# Need to import models for Q objects
from django.db import models
