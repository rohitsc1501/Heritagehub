"""URL configuration for core API."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'states', views.StateViewSet, basename='state')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'places', views.PlaceViewSet, basename='place')
router.register(r'events', views.EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]
