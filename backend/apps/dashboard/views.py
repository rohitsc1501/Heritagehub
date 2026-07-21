"""Admin dashboard analytics API."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth, TruncDate
from django.utils import timezone
from datetime import timedelta
from apps.accounts.permissions import IsAdmin
from apps.accounts.models import User
from apps.accounts.serializers import UserListSerializer
from apps.core.models import Place, Category
from apps.core.serializers import PlaceListSerializer
from apps.bookings.models import Booking
from apps.bookings.serializers import BookingListSerializer
from apps.reviews.models import Review


@api_view(['GET'])
@permission_classes([IsAdmin])
def dashboard_stats(request):
    """Overall dashboard statistics."""
    today = timezone.now().date()
    total_users = User.objects.filter(role='visitor').count()
    total_bookings = Booking.objects.count()
    confirmed_bookings = Booking.objects.filter(status='Confirmed')
    revenue = confirmed_bookings.aggregate(Sum('total_price'))['total_price__sum'] or 0
    today_bookings = Booking.objects.filter(created_at__date=today).count()
    pending = Booking.objects.filter(status='Pending').count()
    cancelled = Booking.objects.filter(status='Cancelled').count()

    # Most popular place
    popular = Booking.objects.values('place__place_name').annotate(
        count=Count('id')
    ).order_by('-count').first()

    # Top category
    top_cat = Booking.objects.values('place__category__name').annotate(
        count=Count('id')
    ).order_by('-count').first()

    return Response({
        'total_users': total_users,
        'total_bookings': total_bookings,
        'revenue': float(revenue),
        'today_bookings': today_bookings,
        'pending_bookings': pending,
        'cancelled_bookings': cancelled,
        'most_popular_place': popular['place__place_name'] if popular else 'N/A',
        'top_category': top_cat['place__category__name'] if top_cat else 'N/A',
        'total_places': Place.objects.filter(status='Active').count(),
        'total_reviews': Review.objects.count(),
    })


@api_view(['GET'])
@permission_classes([IsAdmin])
def monthly_revenue(request):
    """Monthly revenue chart data."""
    data = Booking.objects.filter(
        status='Confirmed'
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total=Sum('total_price'),
        count=Count('id')
    ).order_by('month')
    return Response(list(data))


@api_view(['GET'])
@permission_classes([IsAdmin])
def category_distribution(request):
    """Place count per category."""
    data = Category.objects.annotate(
        count=Count('places', filter=models.Q(places__status='Active'))
    ).values('name', 'count').order_by('-count')
    from django.db import models
    return Response(list(data))


@api_view(['GET'])
@permission_classes([IsAdmin])
def bookings_per_day(request):
    """Daily booking counts for last 30 days."""
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    data = Booking.objects.filter(
        created_at__date__gte=thirty_days_ago
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    return Response(list(data))


@api_view(['GET'])
@permission_classes([IsAdmin])
def top_places(request):
    """Most booked places."""
    data = Place.objects.annotate(
        booking_count=Count('bookings')
    ).order_by('-booking_count')[:10]
    serializer = PlaceListSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_users(request):
    """List all users for admin management."""
    users = User.objects.all().order_by('-date_joined')
    serializer = UserListSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_bookings(request):
    """List all bookings for admin."""
    bookings = Booking.objects.all().select_related('place', 'user').order_by('-created_at')
    serializer = BookingListSerializer(bookings, many=True)
    return Response(serializer.data)
