"""Core data models for heritage places, categories, and locations."""
from django.db import models
from django.utils.text import slugify


class State(models.Model):
    """Indian States and Union Territories."""
    STATE_TYPE_CHOICES = [
        ('State', 'State'),
        ('Union Territory', 'Union Territory'),
    ]
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=STATE_TYPE_CHOICES)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        db_table = 'states'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class District(models.Model):
    """Districts within states."""
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    district_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'districts'
        unique_together = ['state', 'district_name']
        ordering = ['district_name']

    def __str__(self):
        return f"{self.district_name}, {self.state.name}"


class City(models.Model):
    """Cities within districts."""
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='cities')
    city_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'cities'
        unique_together = ['district', 'city_name']
        ordering = ['city_name']
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f"{self.city_name}, {self.district.state.name}"


class Category(models.Model):
    """Heritage place categories."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, null=True,
                            help_text="Emoji or icon class for the category")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Place(models.Model):
    """Heritage places — the core entity."""
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Under Renovation', 'Under Renovation'),
    ]
    UNESCO_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    ASI_CHOICES = [('Yes', 'Yes'), ('No', 'No')]

    # Relationships
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='places')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='places')

    # Basic info
    subcategory = models.CharField(max_length=150, blank=True, null=True)
    place_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    description = models.TextField()
    history = models.TextField(blank=True, null=True)
    year_established = models.CharField(max_length=100, blank=True, null=True)

    # Heritage status
    unesco_status = models.CharField(max_length=3, choices=UNESCO_CHOICES, default='No')
    asi_protected = models.CharField(max_length=3, choices=ASI_CHOICES, default='No')

    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    altitude_m = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    # Timings
    opening_days = models.CharField(max_length=255, blank=True, null=True)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    # Pricing
    entry_fee_indian = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    entry_fee_foreigner = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    student_discount = models.CharField(max_length=100, blank=True, null=True)
    senior_citizen_discount = models.CharField(max_length=100, blank=True, null=True)

    # Facilities
    parking_available = models.CharField(max_length=20, blank=True, null=True)
    wheelchair_accessible = models.CharField(max_length=50, blank=True, null=True)
    guided_tours = models.CharField(max_length=50, blank=True, null=True)
    audio_guide = models.CharField(max_length=100, blank=True, null=True)
    photography_allowed = models.CharField(max_length=20, blank=True, null=True)
    videography_allowed = models.CharField(max_length=100, blank=True, null=True)

    # Visit info
    best_time_to_visit = models.CharField(max_length=100, blank=True, null=True)
    average_visit_duration = models.CharField(max_length=50, blank=True, null=True)

    # Transport
    nearest_airport = models.CharField(max_length=150, blank=True, null=True)
    nearest_railway_station = models.CharField(max_length=150, blank=True, null=True)
    nearest_bus_station = models.CharField(max_length=150, blank=True, null=True)

    # Contact
    official_website = models.URLField(max_length=255, blank=True, null=True)
    booking_url = models.URLField(max_length=500, blank=True, null=True)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)

    # Metrics
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    number_of_reviews = models.IntegerField(default=0)

    # Media
    main_image_url = models.URLField(max_length=500, blank=True, null=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'places'
        ordering = ['-rating', '-number_of_reviews']
        indexes = [
            models.Index(fields=['category'], name='idx_places_category'),
            models.Index(fields=['city'], name='idx_places_city'),
            models.Index(fields=['unesco_status'], name='idx_places_unesco'),
            models.Index(fields=['rating'], name='idx_places_rating'),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.place_name)
            slug = base_slug
            counter = 1
            while Place.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.place_name

    @property
    def state_name(self):
        return self.city.district.state.name

    @property
    def district_name(self):
        return self.city.district.district_name


class PlaceImage(models.Model):
    """Image gallery for places."""
    IMAGE_TYPE_CHOICES = [
        ('Gallery', 'Gallery'),
        ('Cover', 'Cover'),
        ('Panorama', 'Panorama'),
    ]
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500, blank=True, null=True)
    image_file = models.ImageField(upload_to='places/', blank=True, null=True)
    sort_order = models.IntegerField(default=0)
    image_type = models.CharField(max_length=30, choices=IMAGE_TYPE_CHOICES, default='Gallery')

    class Meta:
        db_table = 'place_images'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.place.place_name} - Image {self.sort_order}"


class TicketPrice(models.Model):
    """Ticket pricing per visitor type for each place."""
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='ticket_prices')
    visitor_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')

    class Meta:
        db_table = 'ticket_prices'

    def __str__(self):
        return f"{self.place.place_name} - {self.visitor_type}: ₹{self.price}"


class Event(models.Model):
    """Events at heritage places."""
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='events')
    event_name = models.CharField(max_length=255)
    event_schedule = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'events'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_name} at {self.place.place_name}"
