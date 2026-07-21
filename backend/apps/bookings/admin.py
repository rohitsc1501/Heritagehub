from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'place', 'visit_date', 'total_tickets',
                    'total_price', 'status', 'created_at']
    list_filter = ['status', 'visit_date', 'created_at']
    search_fields = ['booking_id', 'user__username', 'place__place_name']
    readonly_fields = ['booking_id', 'qr_code']
