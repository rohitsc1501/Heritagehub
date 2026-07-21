from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, ExternalTicketViewSet

router = DefaultRouter()
router.register(r'external', ExternalTicketViewSet, basename='external-ticket')
router.register(r'', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]
