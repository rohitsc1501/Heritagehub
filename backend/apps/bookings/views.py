"""Booking API views."""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse
from .models import Booking, ExternalTicket
from .serializers import (
    BookingCreateSerializer, BookingListSerializer, BookingDetailSerializer,
    ExternalTicketSerializer
)
from .utils import generate_ticket_pdf


class BookingViewSet(viewsets.ModelViewSet):
    """CRUD for bookings."""
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        if self.action == 'retrieve':
            return BookingDetailSerializer
        return BookingListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Booking.objects.all().select_related('place', 'user')
        return Booking.objects.filter(user=user).select_related('place')

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """POST /api/bookings/{id}/cancel/"""
        booking = self.get_object()
        if booking.status == 'Cancelled':
            return Response({'error': 'Booking already cancelled.'},
                            status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'Cancelled'
        booking.save()
        return Response({'message': 'Booking cancelled successfully.',
                         'booking': BookingListSerializer(booking).data})

    @action(detail=True, methods=['get'])
    def download_ticket(self, request, pk=None):
        """GET /api/bookings/{id}/download_ticket/"""
        booking = self.get_object()
        if booking.status == 'Cancelled':
            return Response({'error': 'Cannot download ticket for cancelled booking.'},
                            status=status.HTTP_400_BAD_REQUEST)
        pdf_buffer = generate_ticket_pdf(booking)
        response = FileResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_{booking.booking_id}.pdf"'
        return response

class ExternalTicketViewSet(viewsets.ModelViewSet):
    """Upload and manage external tickets."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExternalTicketSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        return ExternalTicket.objects.filter(user=self.request.user)
