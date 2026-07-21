from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'place', 'rating', 'review_date']
    list_filter = ['rating', 'review_date']
    search_fields = ['user__username', 'place__place_name', 'review_text']
