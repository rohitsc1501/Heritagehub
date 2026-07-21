from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Wishlist
from apps.core.serializers import PlaceListSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_wishlist(request):
    """Toggle a place in the user's wishlist."""
    place_id = request.data.get('place_id')
    if not place_id:
        return Response({'error': 'place_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user, place_id=place_id
    )
    if not created:
        wishlist_item.delete()
        return Response({'message': 'Removed from wishlist.', 'is_wishlisted': False})
    return Response({'message': 'Added to wishlist!', 'is_wishlisted': True},
                    status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_wishlist(request):
    """Get user's wishlist."""
    wishlists = Wishlist.objects.filter(user=request.user).select_related(
        'place__city__district__state', 'place__category'
    )
    places = [w.place for w in wishlists]
    serializer = PlaceListSerializer(places, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_wishlist(request, place_id):
    """Check if a place is in user's wishlist."""
    is_wishlisted = Wishlist.objects.filter(
        user=request.user, place_id=place_id
    ).exists()
    return Response({'is_wishlisted': is_wishlisted})
