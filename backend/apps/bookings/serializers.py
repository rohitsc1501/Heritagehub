"""Booking serializers."""
from rest_framework import serializers
from .models import Booking, ExternalTicket
from apps.core.serializers import PlaceListSerializer


class BookingCreateSerializer(serializers.ModelSerializer):
    """Create a new booking with auto price calculation."""

    class Meta:
        model = Booking
        fields = ['place', 'visit_date', 'time_slot', 'adults', 'children',
                  'senior_citizens', 'students']

    def validate(self, attrs):
        total = attrs.get('adults', 0) + attrs.get('children', 0) + \
                attrs.get('senior_citizens', 0) + attrs.get('students', 0)
        if total < 1:
            raise serializers.ValidationError("At least one ticket is required.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        place = validated_data['place']

        # Get ticket prices
        indian_price = place.entry_fee_indian or 0
        foreigner_price = place.entry_fee_foreigner or indian_price

        # Calculate using Indian citizen rates (default)
        adult_price = float(indian_price)
        child_price = float(indian_price) * 0.5  # 50% for children
        senior_price = float(indian_price) * 0.75  # 25% discount
        student_price = float(indian_price) * 0.5  # 50% for students

        subtotal = (
            validated_data.get('adults', 0) * adult_price +
            validated_data.get('children', 0) * child_price +
            validated_data.get('senior_citizens', 0) * senior_price +
            validated_data.get('students', 0) * student_price
        )

        tax = round(subtotal * 0.18, 2)  # 18% GST
        discount = 0
        total = round(subtotal + tax - discount, 2)

        booking = Booking.objects.create(
            user=user,
            subtotal=subtotal,
            tax=tax,
            discount=discount,
            total_price=total,
            status='Confirmed',
            **validated_data
        )

        # Generate QR code
        from .utils import generate_qr_code
        generate_qr_code(booking)

        return booking


class BookingListSerializer(serializers.ModelSerializer):
    """Booking list serializer."""
    place_name = serializers.CharField(source='place.place_name', read_only=True)
    place_slug = serializers.CharField(source='place.slug', read_only=True)
    place_image = serializers.CharField(source='place.main_image_url', read_only=True)
    place_city = serializers.CharField(source='place.city.city_name', read_only=True)
    place_state = serializers.SerializerMethodField()
    visitor_name = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'booking_id', 'place', 'place_name', 'place_slug',
                  'place_image', 'place_city', 'place_state', 'visit_date',
                  'time_slot', 'adults', 'children', 'senior_citizens',
                  'students', 'total_tickets', 'subtotal', 'tax', 'discount',
                  'total_price', 'status', 'visitor_name', 'created_at']

    def get_place_state(self, obj):
        return obj.place.city.district.state.name

    def get_visitor_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


class BookingDetailSerializer(BookingListSerializer):
    """Full booking detail with QR code URL."""
    qr_code_url = serializers.SerializerMethodField()

    class Meta(BookingListSerializer.Meta):
        fields = BookingListSerializer.Meta.fields + ['qr_code_url', 'updated_at']

    def get_qr_code_url(self, obj):
        if obj.qr_code:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.qr_code.url)
        return None

class ExternalTicketSerializer(serializers.ModelSerializer):
    """Serializer for user uploaded external tickets."""
    class Meta:
        model = ExternalTicket
        fields = ['id', 'place_name', 'visit_date', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
