from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.dashboard_stats, name='dashboard-stats'),
    path('charts/monthly-revenue/', views.monthly_revenue, name='monthly-revenue'),
    path('charts/category-distribution/', views.category_distribution, name='category-distribution'),
    path('charts/bookings-per-day/', views.bookings_per_day, name='bookings-per-day'),
    path('charts/top-places/', views.top_places, name='top-places'),
    path('users/', views.admin_users, name='admin-users'),
    path('bookings/', views.admin_bookings, name='admin-bookings'),
]
