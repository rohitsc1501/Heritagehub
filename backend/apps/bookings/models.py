"""Booking and ticket models."""
import uuid
from django.db import models
from django.conf import settings
from apps.core.models import Place


class Booking(models.Model):
    """Ticket booking for a heritage place."""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    TIME_SLOTS = [
        ('09:00-11:00', '9:00 AM - 11:00 AM'),
        ('11:00-13:00', '11:00 AM - 1:00 PM'),
        ('13:00-15:00', '1:00 PM - 3:00 PM'),
        ('15:00-17:00', '3:00 PM - 5:00 PM'),
        ('17:00-19:00', '5:00 PM - 7:00 PM'),
    ]

    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='bookings')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='bookings')

    # Visit details
    visit_date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS, default='09:00-11:00')

    # Ticket counts
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    senior_citizens = models.PositiveIntegerField(default=0)
    students = models.PositiveIntegerField(default=0)

    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Status & QR
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.booking_id} - {self.place.place_name}"

    @property
    def total_tickets(self):
        return self.adults + self.children + self.senior_citizens + self.students


class ExternalTicket(models.Model):
    """User-uploaded tickets for external bookings."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='external_tickets')
    place_name = models.CharField(max_length=255)
    visit_date = models.DateField()
    file = models.FileField(upload_to='external_tickets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'external_tickets'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"External Ticket - {self.place_name} ({self.user.username})"
