from django.db import models
from django.conf import settings
from apps.core.models import Place

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wishlists'
        unique_together = ['user', 'place']

    def __str__(self):
        return f"{self.user.username} → {self.place.place_name}"
