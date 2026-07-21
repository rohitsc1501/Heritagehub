"""Review API views."""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Avg
from .models import Review
from .serializers import ReviewSerializer
from apps.core.models import Place


class ReviewViewSet(viewsets.ModelViewSet):
    """CRUD for reviews."""
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = Review.objects.all().select_related('user', 'place')
        place_id = self.request.query_params.get('place')
        if place_id:
            queryset = queryset.filter(place_id=place_id)
        user_only = self.request.query_params.get('my_reviews')
        if user_only and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        # Update place average rating
        place = review.place
        avg = Review.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg']
        count = Review.objects.filter(place=place).count()
        place.rating = round(avg, 1) if avg else 0
        place.number_of_reviews = count
        place.save(update_fields=['rating', 'number_of_reviews'])

    def perform_destroy(self, instance):
        place = instance.place
        instance.delete()
        # Recalculate
        avg = Review.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg']
        count = Review.objects.filter(place=place).count()
        place.rating = round(avg, 1) if avg else 0
        place.number_of_reviews = count
        place.save(update_fields=['rating', 'number_of_reviews'])
