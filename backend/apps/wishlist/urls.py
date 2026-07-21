from django.urls import path
from . import views

urlpatterns = [
    path('toggle/', views.toggle_wishlist, name='toggle-wishlist'),
    path('', views.list_wishlist, name='list-wishlist'),
    path('check/<int:place_id>/', views.check_wishlist, name='check-wishlist'),
]
